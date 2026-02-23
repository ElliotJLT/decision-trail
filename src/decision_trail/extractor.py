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
    "no,", "no.", "nah", "actually", "instead", "don't", "not that", "wrong",
    "i'd rather", "i prefer", "let's go with", "change that to",
    "that's not", "i disagree", "disagree", "override", "ignore that",
    "scratch that", "wait,", "hold on", "stop", "leave as is",
    "bit weird", "not clear", "not quite", "weak", "superweak",
    "too fluffy", "that's fluffy", "kill that", "dead",
]

# Patterns that indicate the AI is presenting options
CHOICE_SIGNALS = [
    "option 1", "option 2", "approach 1", "approach 2",
    "we could either", "two approaches", "alternatives:",
    "which would you prefer", "should i", "do you want",
    "there are a few ways", "a few options",
    "here are", "pick one", "pick 1",
]


@dataclass
class Turn:
    """A grouped conversation turn — one human or one assistant (possibly multi-line)."""
    role: str  # "human" | "assistant"
    content: str  # merged text from all entries in this turn
    raw_entries: list  # original JSONL entries
    files_changed: set  # files written/edited during this turn


def extract_from_session(session_path: Path) -> List[DecisionCandidate]:
    """Parse a Claude Code JSONL session and identify decision moments."""
    turns = _load_session_grouped(session_path)
    if not turns:
        return []

    candidates = []

    for i, turn in enumerate(turns):
        if turn.role != "human" or i == 0:
            continue

        # Find the preceding assistant turn
        prev_assistant = None
        for j in range(i - 1, -1, -1):
            if turns[j].role == "assistant":
                prev_assistant = turns[j]
                break

        if not prev_assistant:
            continue

        human_text = turn.content

        # Skip empty or system messages
        if not human_text.strip() or human_text.startswith("[Request interrupted"):
            continue

        # Check for redirections
        if _check_redirect(human_text, prev_assistant.content):
            candidates.append(DecisionCandidate(
                summary=_summarize(human_text, 80),
                context=_summarize(prev_assistant.content, 200),
                ai_suggestion=_summarize(prev_assistant.content, 200),
                human_response=_summarize(human_text, 200),
                category="redirect",
                turn_index=i,
            ))

        # Check for choices (AI presented options, human picked)
        elif _check_choice(prev_assistant.content, human_text):
            candidates.append(DecisionCandidate(
                summary=f"Chose: {_summarize(human_text, 60)}",
                context=_summarize(prev_assistant.content, 200),
                ai_suggestion=_summarize(prev_assistant.content, 200),
                human_response=_summarize(human_text, 200),
                category="choice",
                turn_index=i,
            ))

        # Check for significant file changes in the assistant turn
        if prev_assistant.files_changed and len(prev_assistant.files_changed) >= 3:
            files_str = ", ".join(sorted(prev_assistant.files_changed)[:5])
            candidates.append(DecisionCandidate(
                summary=f"Significant changes: {files_str}",
                context=_summarize(human_text, 200),
                ai_suggestion=_summarize(prev_assistant.content, 200),
                human_response="",
                category="significant_change",
                turn_index=i,
            ))

    return candidates


def _load_session_grouped(session_path: Path) -> List[Turn]:
    """Load JSONL session and group consecutive same-role entries into turns.

    Claude Code writes multiple JSONL lines per assistant turn (thinking, text,
    tool_use as separate entries). This groups them so we get clean human→assistant
    turn pairs.
    """
    raw_entries = _load_raw_entries(session_path)
    if not raw_entries:
        return []

    turns: List[Turn] = []
    current_role = None
    current_texts: list[str] = []
    current_raw: list = []
    current_files: set = set()

    for entry in raw_entries:
        role = entry.get("_role")
        text = entry.get("_text", "")
        files = entry.get("_files", set())

        if role != current_role and current_role is not None:
            # Flush current turn
            merged = " ".join(t for t in current_texts if t.strip())
            if merged.strip():
                turns.append(Turn(
                    role=current_role,
                    content=merged,
                    raw_entries=current_raw,
                    files_changed=current_files,
                ))
            current_texts = []
            current_raw = []
            current_files = set()

        current_role = role
        if text.strip():
            current_texts.append(text)
        current_raw.append(entry)
        current_files.update(files)

    # Flush final turn
    if current_role and current_texts:
        merged = " ".join(t for t in current_texts if t.strip())
        if merged.strip():
            turns.append(Turn(
                role=current_role,
                content=merged,
                raw_entries=current_raw,
                files_changed=current_files,
            ))

    return turns


def _load_raw_entries(session_path: Path) -> List[dict]:
    """Load JSONL entries and normalize them with _role, _text, _files fields."""
    entries = []
    with open(session_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if not isinstance(entry, dict):
                continue

            entry_type = entry.get("type", "")
            msg = entry.get("message", {})

            if not isinstance(msg, dict):
                continue

            role = None
            text = ""
            files: set = set()

            if entry_type == "user":
                role = "human"
                text = _extract_text(msg)
            elif entry_type == "assistant":
                role = "assistant"
                text = _extract_text(msg)
                files = _extract_files(msg)

            if role:
                entry["_role"] = role
                entry["_text"] = text
                entry["_files"] = files
                entries.append(entry)

    return entries


# Keep this alias for the digest module
def _load_session(session_path: Path) -> List[dict]:
    """Load session as flat list of messages (for backward compat)."""
    turns = _load_session_grouped(session_path)
    return [{"role": t.role, "content": t.content, "raw": {}} for t in turns]


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
                # Skip thinking blocks — they're internal
        return " ".join(parts)
    return str(content)


def _extract_files(msg: dict) -> set:
    """Extract file paths from tool_use blocks in a message."""
    content = msg.get("content", "")
    if not isinstance(content, list):
        return set()

    files = set()
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            name = block.get("name", "")
            inp = block.get("input", {})
            if isinstance(inp, dict) and name in ("Write", "Edit", "NotebookEdit"):
                path = inp.get("file_path", "")
                if path:
                    files.add(Path(path).name)
    return files


def _check_redirect(human_text: str, ai_text: str) -> bool:
    """Check if the human message is redirecting/overriding the AI."""
    lower = human_text.lower()
    return any(signal in lower for signal in REDIRECT_SIGNALS)


def _check_choice(ai_text: str, human_text: str) -> bool:
    """Check if the AI presented options and the human made a choice."""
    lower = ai_text.lower()
    return any(signal in lower for signal in CHOICE_SIGNALS)


def _summarize(text: str, max_len: int) -> str:
    """Truncate text to max_len, adding ellipsis if needed."""
    text = " ".join(text.split())  # normalize whitespace
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
