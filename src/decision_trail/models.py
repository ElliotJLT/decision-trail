"""Decision record data model and parsing."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import List, Optional


@dataclass
class Alternative:
    option: str
    pros: str
    cons: str
    source: str  # "AI suggested" | "Human proposed" | "Team discussed"


@dataclass
class DecisionRecord:
    number: int
    title: str
    date: str
    status: str  # accepted | superseded | deprecated | proposed
    tags: List[str] = field(default_factory=list)
    model: str = ""
    confidence: str = "medium"  # low | medium | high
    context: str = ""
    decision: str = ""
    ai_suggestion: str = ""
    human_take: str = ""
    alternatives: List[Alternative] = field(default_factory=list)
    consequences: str = ""
    session_ref: str = ""

    @property
    def id(self) -> str:
        return f"DT-{self.number:03d}"

    @property
    def filename(self) -> str:
        slug = re.sub(r"[^a-z0-9]+", "-", self.title.lower()).strip("-")
        return f"{self.number:03d}-{slug}.md"

    def to_markdown(self) -> str:
        from .templates import render_decision
        return render_decision(self)

    @classmethod
    def from_markdown(cls, text: str, filepath: Optional[Path] = None) -> DecisionRecord:
        """Parse a decision record from markdown text."""
        # Extract number and title from heading
        heading = re.search(r"^#\s+DT-(\d+):\s*(.+)$", text, re.MULTILINE)
        if not heading:
            raise ValueError("Could not parse decision heading (expected '# DT-NNN: Title')")
        number = int(heading.group(1))
        title = heading.group(2).strip()

        def extract_field(name: str) -> str:
            pattern = rf"\*\*{name}:\*\*\s*(.+)"
            match = re.search(pattern, text)
            return match.group(1).strip() if match else ""

        def extract_section(name: str) -> str:
            pattern = rf"^##\s+{name}\s*\n(.*?)(?=^##\s|\Z)"
            match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
            return match.group(1).strip() if match else ""

        tags_raw = extract_field("Tags")
        tags = [t.strip() for t in tags_raw.split() if t.startswith("#")] if tags_raw else []

        # Parse alternatives table
        alternatives = []
        alt_section = extract_section("Alternatives Considered")
        if alt_section:
            rows = re.findall(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|", alt_section, re.MULTILINE)
            for row in rows:
                cells = [c.strip() for c in row]
                if cells[0].startswith("-") or cells[0].lower() == "option":
                    continue
                alternatives.append(Alternative(*cells))

        return cls(
            number=number,
            title=title,
            date=extract_field("Date"),
            status=extract_field("Status"),
            tags=tags,
            model=extract_field("Model"),
            confidence=extract_field("Confidence"),
            context=extract_section("Context"),
            decision=extract_section("Decision"),
            ai_suggestion=extract_section("AI Suggestion"),
            human_take=extract_section("Human Take"),
            alternatives=alternatives,
            consequences=extract_section("Consequences"),
            session_ref=extract_field("Session"),
        )


def next_decision_number(decisions_dir: Path) -> int:
    """Get the next decision number based on existing files."""
    existing = list(decisions_dir.glob("*.md"))
    numbers = []
    for f in existing:
        match = re.match(r"(\d+)-", f.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def load_decisions(decisions_dir: Path) -> List[DecisionRecord]:
    """Load all decision records from a directory."""
    records = []
    for f in sorted(decisions_dir.glob("*.md")):
        try:
            text = f.read_text()
            records.append(DecisionRecord.from_markdown(text, f))
        except (ValueError, IndexError):
            continue
    return records
