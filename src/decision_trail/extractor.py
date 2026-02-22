"""Claude Code JSONL session parser for extracting decision candidates."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class DecisionCandidate:
    """A potential decision moment found in a session log."""
    summary: str
    context: str
    ai_suggestion: str
    human_response: str
    category: str  # "redirect" | "choice" | "significant_change"
    turn_index: int
    confidence: str = "medium"

    def display(self) -> str:
        lines = [
            f"  [{self.category}] {self.summary}",
            f"  AI: {self.ai_suggestion[:120]}",
            f"  Human: {self.human_response[:120]}",
        ]
        return "\n".join(lines)


# Patterns that indicate the user is redirecting the AI
REDIRECT_SIGNALS = [
    "no,", "no.", "actually", "instead", "don't", "not that", "wrong",
    "i'd rather", "i prefer", "let's go with", "change that to",
    "that's not", "i disagree", "override", "ignore that",
    "scratch that", "wait,", "hold on", "stop",
]

# Patterns that indicate the AI is presenting options
CHOICE_SIGNALS = [
    "option 1", "option 2", "approach 1", "approach 2",
    "we could either", "two approaches", "alternatives:",
    "which would you prefer", "should i", "do you want",
    "there are a few ways", "a few options",
]


def extract_from_session(session_path: Path) -> List[DecisionCandidate]:
    """Parse a Claude Code JSONL session and identify decision moments."""
    messages = _load_session(session_path)
    if not messages:
        return []

    candidates = []

    for i, msg in enumerate(messages):
        # Check for user redirections
        if msg["role"] == "human" and i > 0:
            prev = messages[i - 1] if i > 0 else None
            if prev and prev["role"] == "assistant":
                redirect = _check_redirect(msg["content"], prev["content"])
                if redirect:
                    candidates.append(DecisionCandidate(
                        summary=_summarize(msg["content"], 80),
                        context=_summarize(prev["content"], 200),
                        ai_suggestion=_summarize(prev["content"], 200),
                        human_response=_summarize(msg["content"], 200),
                        category="redirect",
                        turn_index=i,
                    ))

        # Check for AI presenting choices that the user then selected
        if msg["role"] == "assistant":
            next_msg = messages[i + 1] if i + 1 < len(messages) else None
            if next_msg and next_msg["role"] == "human":
                choice = _check_choice(msg["content"], next_msg["content"])
                if choice:
                    candidates.append(DecisionCandidate(
                        summary=f"Chose: {_summarize(next_msg['content'], 60)}",
                        context=_summarize(msg["content"], 200),
                        ai_suggestion=_summarize(msg["content"], 200),
                        human_response=_summarize(next_msg["content"], 200),
                        category="choice",
                        turn_index=i,
                    ))

        # Check for significant file operations
        if msg["role"] == "assistant":
            changes = _check_significant_changes(msg)
            if changes:
                human_context = messages[i - 1]["content"] if i > 0 else ""
                candidates.append(DecisionCandidate(
                    summary=f"Significant changes: {changes}",
                    context=_summarize(human_context, 200) if human_context else "",
                    ai_suggestion=_summarize(msg["content"], 200),
                    human_response="",
                    category="significant_change",
                    turn_index=i,
                ))

    return candidates


def _load_session(session_path: Path) -> List[dict]:
    """Load and normalize messages from a JSONL session file."""
    messages = []
    with open(session_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Normalize different session formats
            role = None
            content = ""

            if isinstance(entry, dict):
                # Claude Code session format: {message: {role, content}, type: "user"|...}
                msg = entry.get("message", {})
                if isinstance(msg, dict) and "role" in msg:
                    msg_role = msg["role"]
                    if msg_role == "user":
                        role = "human"
                        content = _extract_text(msg)
                    elif msg_role == "assistant":
                        role = "assistant"
                        content = _extract_text(msg)
                elif "type" in entry:
                    if entry["type"] in ("human", "user"):
                        role = "human"
                        content = _extract_text(entry.get("message", entry))
                    elif entry["type"] == "assistant":
                        role = "assistant"
                        content = _extract_text(entry.get("message", entry))
                elif "role" in entry:
                    role = entry["role"]
                    content = _extract_text(entry)

            if role and content:
                messages.append({"role": role, "content": content, "raw": entry})

    return messages


def _extract_text(msg: dict) -> str:
    """Extract plain text from a message, handling various content formats."""
    content = msg.get("content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "tool_use":
                    name = block.get("name", "")
                    inp = block.get("input", {})
                    if name in ("Write", "Edit"):
                        path = inp.get("file_path", "")
                        parts.append(f"[{name}: {path}]")
                    else:
                        parts.append(f"[{name}]")
        return " ".join(parts)
    return str(content)


def _check_redirect(human_text: str, ai_text: str) -> bool:
    """Check if the human message is redirecting/overriding the AI."""
    lower = human_text.lower()
    return any(signal in lower for signal in REDIRECT_SIGNALS)


def _check_choice(ai_text: str, human_text: str) -> bool:
    """Check if the AI presented options and the human made a choice."""
    lower = ai_text.lower()
    return any(signal in lower for signal in CHOICE_SIGNALS)


def _check_significant_changes(msg: dict) -> Optional[str]:
    """Check if the message contains significant file changes."""
    raw = msg.get("raw", {})
    content = raw.get("content", raw.get("message", {}).get("content", ""))

    if not isinstance(content, list):
        return None

    files_changed = set()
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            name = block.get("name", "")
            inp = block.get("input", {})
            if name in ("Write", "Edit"):
                path = inp.get("file_path", "")
                if path:
                    files_changed.add(Path(path).name)

    if len(files_changed) >= 3:
        return ", ".join(sorted(files_changed)[:5])
    return None


def _summarize(text: str, max_len: int) -> str:
    """Truncate text to max_len, adding ellipsis if needed."""
    text = " ".join(text.split())  # normalize whitespace
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
