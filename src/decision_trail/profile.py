"""Parse digests and synthesis files into a profile data structure."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DigestData:
    """Parsed data from a single session digest."""

    date: str
    topic: str
    summary: str
    bullets: list[str] = field(default_factory=list)
    pattern: str | None = None


@dataclass
class SynthesisData:
    """Parsed data from a monthly synthesis."""

    month: str
    session_count: int | None = None
    recurring_patterns: list[str] = field(default_factory=list)
    evolution: list[str] = field(default_factory=list)
    beyond_fluency: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)


@dataclass
class ProfileData:
    """Aggregated profile data ready for rendering."""

    total_sessions: int
    date_range: str
    active_since: str
    how_i_work: str
    highlighted_moments: list[str]
    evolution_narrative: str
    beyond_fluency_evidence: str
    digests: list[DigestData] = field(default_factory=list)
    synthesis: list[SynthesisData] = field(default_factory=list)


def parse_digest(path: Path) -> DigestData:
    """Parse a single digest markdown file."""
    text = path.read_text().strip()
    lines = text.splitlines()

    # Parse title: "# YYYY-MM-DD — topic"
    date = ""
    topic = ""
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        if " — " in title:
            date, topic = title.split(" — ", 1)
        elif " - " in title:
            date, topic = title.split(" - ", 1)
        else:
            date = title

    # Find summary (first non-empty line after title)
    summary = ""
    bullets = []
    pattern = None
    in_body = False

    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            in_body = True
            continue
        if not in_body:
            continue

        if stripped.startswith("- "):
            bullet_text = stripped[2:].strip()
            # Check if this is a pattern line
            if bullet_text.lower().startswith("pattern:"):
                pattern = bullet_text[len("pattern:"):].strip()
            else:
                bullets.append(bullet_text)
        elif not bullets and not summary:
            summary = stripped

    return DigestData(
        date=date.strip(),
        topic=topic.strip(),
        summary=summary,
        bullets=bullets,
        pattern=pattern,
    )


def parse_synthesis(path: Path) -> SynthesisData:
    """Parse a monthly synthesis markdown file."""
    text = path.read_text().strip()
    lines = text.splitlines()

    # Parse title: "# Synthesis — Month Year (N sessions)"
    month = ""
    session_count = None
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        # Extract month
        m = re.search(r"—\s*(.+?)(?:\s*\(|$)", title)
        if m:
            month = m.group(1).strip()
        # Extract session count
        m = re.search(r"\((\d+)\s+sessions?\)", title)
        if m:
            session_count = int(m.group(1))

    # Parse sections
    current_section = None
    sections: dict[str, list[str]] = {
        "recurring patterns": [],
        "evolution": [],
        "beyond fluency": [],
        "gaps": [],
    }

    for line in lines[1:]:
        stripped = line.strip()

        # Detect section headers
        if stripped.startswith("## "):
            header = stripped[3:].strip().lower()
            if header in sections:
                current_section = header
            continue

        if current_section and stripped.startswith("- "):
            sections[current_section].append(stripped[2:].strip())

    return SynthesisData(
        month=month,
        session_count=session_count,
        recurring_patterns=sections["recurring patterns"],
        evolution=sections["evolution"],
        beyond_fluency=sections["beyond fluency"],
        gaps=sections["gaps"],
    )


def _select_highlighted_moments(digests: list[DigestData], max_count: int = 5) -> list[str]:
    """Pick the best bullets from digests — ones that show thinking style."""
    # Prioritise bullets that demonstrate judgment, not just action
    signal_words = [
        "caught", "refused", "rejected", "challenged", "flagged",
        "stopped", "killed", "resisted", "spotted", "redirected",
        "diagnosed", "held", "chose", "instinct", "quality bar",
        "pressure-tested", "fabricat",
    ]

    scored: list[tuple[int, str]] = []
    for d in digests:
        for bullet in d.bullets:
            lower = bullet.lower()
            score = sum(1 for w in signal_words if w in lower)
            # Bonus for bullets with a quote or specific detail
            if '"' in bullet or "'" in bullet:
                score += 1
            scored.append((score, bullet))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [text for _, text in scored[:max_count]]


def _build_how_i_work(synthesis_list: list[SynthesisData], digests: list[DigestData]) -> str:
    """Build the 'How I Work With AI' narrative from synthesis patterns."""
    if synthesis_list:
        # Use the most recent synthesis recurring patterns
        latest = synthesis_list[-1]
        if latest.recurring_patterns:
            return " ".join(latest.recurring_patterns)

    # Fallback: combine pattern lines from digests
    patterns = [d.pattern for d in digests if d.pattern]
    if patterns:
        # Capitalise first letter of each pattern sentence
        capped = [p[0].upper() + p[1:] if p else p for p in patterns]
        return " ".join(capped)

    return ""


def _build_evolution(synthesis_list: list[SynthesisData]) -> str:
    """Build evolution narrative from synthesis."""
    if not synthesis_list:
        return ""
    latest = synthesis_list[-1]
    if latest.evolution:
        return " ".join(latest.evolution)
    return ""


def _build_beyond_fluency(synthesis_list: list[SynthesisData]) -> str:
    """Build beyond-fluency evidence from synthesis."""
    if not synthesis_list:
        return ""
    latest = synthesis_list[-1]
    if latest.beyond_fluency:
        return " ".join(latest.beyond_fluency)
    return ""


def build_profile(root: Path) -> ProfileData:
    """Read all digests and synthesis files, return a ProfileData."""
    digest_dir = root / "decisions" / "digests"
    synthesis_dir = root / "decisions" / "synthesis"

    # Parse digests
    digests: list[DigestData] = []
    if digest_dir.is_dir():
        for path in sorted(digest_dir.glob("*.md")):
            digests.append(parse_digest(path))

    # Parse synthesis
    synthesis_list: list[SynthesisData] = []
    if synthesis_dir.is_dir():
        for path in sorted(synthesis_dir.glob("*.md")):
            synthesis_list.append(parse_synthesis(path))

    # Compute stats
    total_sessions = len(digests)
    dates = [d.date for d in digests if d.date]
    if dates:
        active_since = min(dates)
        date_range = f"{min(dates)} to {max(dates)}" if len(dates) > 1 else min(dates)
    else:
        active_since = ""
        date_range = ""

    return ProfileData(
        total_sessions=total_sessions,
        date_range=date_range,
        active_since=active_since,
        how_i_work=_build_how_i_work(synthesis_list, digests),
        highlighted_moments=_select_highlighted_moments(digests),
        evolution_narrative=_build_evolution(synthesis_list),
        beyond_fluency_evidence=_build_beyond_fluency(synthesis_list),
        digests=digests,
        synthesis=synthesis_list,
    )
