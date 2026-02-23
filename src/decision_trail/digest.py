"""Session digest generator.

Produces a raw, readable summary of human direction during a Claude Code session.
No scoring. No vanity metrics. Just evidence of how you worked.
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import List

from .extractor import DecisionCandidate, _load_session


def generate_digest(session_path: Path, candidates: List[DecisionCandidate]) -> str:
    """Generate a markdown digest from session data and extracted candidates."""
    messages = _load_session(session_path)

    human_msgs = [m for m in messages if m["role"] == "human"]
    ai_msgs = [m for m in messages if m["role"] == "assistant"]

    redirects = [c for c in candidates if c.category == "redirect"]
    choices = [c for c in candidates if c.category == "choice"]
    changes = [c for c in candidates if c.category == "significant_change"]

    lines = []
    lines.append(f"# Session Digest — {date.today().isoformat()}")
    lines.append("")
    lines.append(f"**Source:** `{session_path.name}`")
    lines.append(f"**Turns:** {len(human_msgs)} human, {len(ai_msgs)} assistant")
    lines.append("")

    # Redirections — the moments the human overrode the AI
    if redirects:
        lines.append("## Redirections")
        lines.append("")
        for r in redirects:
            lines.append(f"- **{_truncate(r.summary, 80)}**")
            if r.ai_suggestion:
                lines.append(f"  - AI was doing: {_truncate(r.ai_suggestion, 120)}")
            if r.human_response:
                lines.append(f"  - Human said: {_truncate(r.human_response, 120)}")
            lines.append("")

    # Choices — where the AI presented options and the human picked
    if choices:
        lines.append("## Choices Made")
        lines.append("")
        for c in choices:
            lines.append(f"- **{_truncate(c.summary, 80)}**")
            if c.context:
                lines.append(f"  - Context: {_truncate(c.context, 120)}")
            lines.append("")

    # Significant changes — large file operations the human initiated
    if changes:
        lines.append("## Significant Changes")
        lines.append("")
        for ch in changes:
            lines.append(f"- {_truncate(ch.summary, 100)}")
        lines.append("")

    # If nothing was detected
    if not candidates:
        lines.append("## Session Summary")
        lines.append("")
        lines.append("No redirections, choices, or significant changes detected in this session.")
        lines.append("This may mean the session was exploratory, or the detection heuristics missed something.")
        lines.append("")

    # Raw stats — just the numbers, no interpretation
    lines.append("## Raw Numbers")
    lines.append("")
    lines.append(f"- Human messages: {len(human_msgs)}")
    lines.append(f"- AI responses: {len(ai_msgs)}")
    lines.append(f"- Redirections detected: {len(redirects)}")
    lines.append(f"- Choices detected: {len(choices)}")
    lines.append(f"- Significant changes: {len(changes)}")
    lines.append("")

    return "\n".join(lines)


def _truncate(text: str, max_len: int) -> str:
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."
