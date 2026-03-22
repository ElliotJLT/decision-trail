"""Measurement layer for decision-trail.

Parses digest files (and optionally raw JSONL session logs) to extract
quantified metrics from qualitative session data. Tracks trends across
sessions and flags coasting.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class SessionMetrics:
    """Quantified metrics for a single session."""

    date: str
    topic: str
    redirect_count: int = 0
    unchallenged_count: int = 0
    wrong_call_count: int = 0
    override_rate: float = 0.0  # redirects / (redirects + unchallenged)
    session_duration_estimate: str = ""
    engagement_score: float = 0.0  # 0-100 composite

    @property
    def total_moments(self) -> int:
        return self.redirect_count + self.unchallenged_count + self.wrong_call_count


@dataclass
class TrendData:
    """Trend analysis across sessions."""

    direction: str = "flat"  # "up", "down", "flat"
    moving_avg_5: float = 0.0
    moving_avg_10: float = 0.0
    values: list[float] = field(default_factory=list)
    sparkline: str = ""


@dataclass
class CoastingAlert:
    """Warning when engagement drops."""

    message: str
    severity: str  # "warning" | "critical"
    sessions_involved: list[str] = field(default_factory=list)


@dataclass
class MetricsSummary:
    """Aggregate metrics across all sessions."""

    sessions: list[SessionMetrics] = field(default_factory=list)
    total_sessions: int = 0
    avg_engagement_score: float = 0.0
    avg_override_rate: float = 0.0
    total_redirects: int = 0
    total_unchallenged: int = 0
    total_wrong_calls: int = 0
    override_rate_trend: TrendData = field(default_factory=TrendData)
    engagement_trend: TrendData = field(default_factory=TrendData)
    coasting_alerts: list[CoastingAlert] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Digest parsing
# ---------------------------------------------------------------------------

def _count_bullets(text: str, section_name: str) -> int:
    """Count bullet points under a given ## section in markdown."""
    lines = text.splitlines()
    in_section = False
    count = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## "):
            header = stripped[3:].strip().lower()
            in_section = header == section_name.lower()
            continue

        if in_section:
            # A new section or end of file stops counting
            if stripped.startswith("# "):
                break
            # Count actual bullets, skip empty lines and non-bullet text
            if stripped.startswith("- ") or stripped.startswith("* "):
                # Skip sub-bullets (indented bullets under a parent)
                if line.startswith("  ") and (line.strip().startswith("- ") or line.strip().startswith("* ")):
                    continue
                count += 1

    return count


def _extract_duration(text: str) -> str:
    """Extract session duration estimate from digest header/summary.

    Looks for patterns like '~4h research session', '2-hour session',
    'short session', 'long session'.
    """
    # Match patterns like ~4h, ~2h, 3h, 1.5h, 2-hour, etc.
    m = re.search(r"~?(\d+\.?\d*)\s*h(?:our)?s?\b", text[:500], re.IGNORECASE)
    if m:
        return f"~{m.group(1)}h"

    # Match descriptive durations
    for label in ("short", "quick", "brief"):
        if label in text[:500].lower():
            return "short"
    for label in ("long", "extended", "marathon"):
        if label in text[:500].lower():
            return "long"

    return ""


def _compute_engagement_score(
    redirect_count: int,
    unchallenged_count: int,
    wrong_call_count: int,
    has_pattern: bool,
) -> float:
    """Compute a 0-100 engagement score.

    Components:
    - Override balance (0-40): healthy ratio of redirects to unchallenged.
      Pure coasting (all unchallenged) scores 0. Pure override scores ~30.
      A balanced mix scores highest.
    - Activity volume (0-25): more notable moments = more engaged.
    - Self-awareness bonus (0-20): wrong calls section populated = honest.
    - Pattern emergence (0-15): identifying patterns = meta-cognition.
    """
    total = redirect_count + unchallenged_count
    score = 0.0

    # Override balance (0-40)
    if total > 0:
        ratio = redirect_count / total
        # Peak engagement is around 40-70% override rate — you're steering
        # but also trusting when appropriate
        if 0.3 <= ratio <= 0.8:
            score += 35 + (5 * (1 - abs(ratio - 0.55) / 0.25))
        elif ratio > 0.8:
            # All override, no trust — still engaged but less balanced
            score += 25
        else:
            # Low override — mostly coasting
            score += 15 * ratio / 0.3
    elif redirect_count == 0 and unchallenged_count == 0:
        # No data — neutral
        score += 15

    # Activity volume (0-25)
    total_moments = redirect_count + unchallenged_count + wrong_call_count
    if total_moments >= 6:
        score += 25
    elif total_moments >= 3:
        score += 15 + (10 * (total_moments - 3) / 3)
    elif total_moments > 0:
        score += 5 * total_moments

    # Self-awareness bonus (0-20)
    if wrong_call_count > 0:
        score += min(20, 10 + (wrong_call_count * 5))

    # Pattern emergence (0-15)
    if has_pattern:
        score += 15

    return min(100.0, round(score, 1))


def parse_digest_metrics(path: Path) -> SessionMetrics:
    """Parse a single digest file and extract quantified metrics."""
    text = path.read_text().strip()
    lines = text.splitlines()

    # Parse header: "# YYYY-MM-DD — topic"
    date = ""
    topic = ""
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        # Handle both "Session Digest — YYYY-MM-DD" and "YYYY-MM-DD — topic"
        if " — " in title:
            parts = title.split(" — ", 1)
            # Check which part looks like a date
            if re.match(r"\d{4}-\d{2}-\d{2}", parts[0].strip()):
                date = parts[0].strip()
                topic = parts[1].strip()
            elif re.match(r"\d{4}-\d{2}-\d{2}", parts[1].strip()):
                date = parts[1].strip()
                topic = parts[0].strip()
            else:
                date = parts[0].strip()
                topic = parts[1].strip()
        elif " - " in title:
            parts = title.split(" - ", 1)
            date = parts[0].strip()
            topic = parts[1].strip() if len(parts) > 1 else ""
        else:
            date = title

    # Fall back to filename for date if not found in header
    if not date:
        m = re.match(r"(\d{4}-\d{2}-\d{2})", path.stem)
        if m:
            date = m.group(1)

    # Count bullets in each section
    # /marmite format: "Redirects", "Unchallenged", "Wrong calls", "Pattern"
    # digest.py format: "Redirections", "Choices Made", "Significant Changes", "Raw Numbers"
    redirect_count = _count_bullets(text, "Redirects") + _count_bullets(text, "Redirections")
    unchallenged_count = _count_bullets(text, "Unchallenged") + _count_bullets(text, "Choices Made")
    wrong_call_count = _count_bullets(text, "Wrong calls")

    # Check for pattern section content (not "No new pattern.")
    has_pattern = False
    pattern_text = _get_section_text(text, "Pattern")
    if pattern_text and "no new pattern" not in pattern_text.lower():
        has_pattern = True

    # Extract duration from the summary (lines after header, before first ##)
    summary_text = ""
    for line in lines[1:]:
        if line.strip().startswith("## "):
            break
        summary_text += line + "\n"
    duration = _extract_duration(summary_text)

    # For auto-generated digests, try to get counts from Raw Numbers section
    raw_numbers = _get_section_text(text, "Raw Numbers")
    if raw_numbers and redirect_count == 0:
        m = re.search(r"Redirections detected:\s*(\d+)", raw_numbers)
        if m:
            redirect_count = int(m.group(1))

    # Compute derived metrics
    total = redirect_count + unchallenged_count
    override_rate = redirect_count / total if total > 0 else 0.0

    engagement = _compute_engagement_score(
        redirect_count, unchallenged_count, wrong_call_count, has_pattern,
    )

    return SessionMetrics(
        date=date,
        topic=topic,
        redirect_count=redirect_count,
        unchallenged_count=unchallenged_count,
        wrong_call_count=wrong_call_count,
        override_rate=round(override_rate, 3),
        session_duration_estimate=duration,
        engagement_score=engagement,
    )


def _get_section_text(text: str, section_name: str) -> str:
    """Get the raw text content of a named ## section."""
    lines = text.splitlines()
    in_section = False
    section_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if in_section:
                break
            header = stripped[3:].strip().lower()
            if header == section_name.lower():
                in_section = True
            continue
        if in_section:
            section_lines.append(line)

    return "\n".join(section_lines).strip()


# ---------------------------------------------------------------------------
# Session log parsing (--from-sessions)
# ---------------------------------------------------------------------------

def metrics_from_session_log(session_path: Path) -> SessionMetrics:
    """Derive metrics directly from a JSONL session log using the extractor."""
    from .extractor import extract_from_session

    candidates = extract_from_session(session_path)

    redirect_count = sum(1 for c in candidates if c.category == "redirect")
    choice_count = sum(1 for c in candidates if c.category == "choice")
    # Choices are roughly analogous to unchallenged — the AI presented options,
    # the human picked one without fundamentally redirecting
    unchallenged_count = choice_count
    # Can't detect wrong calls from raw logs — that requires human reflection
    wrong_call_count = 0

    total = redirect_count + unchallenged_count
    override_rate = redirect_count / total if total > 0 else 0.0

    # Extract date from filename
    date = ""
    m = re.match(r"(\d{4}-\d{2}-\d{2})", session_path.stem)
    if m:
        date = m.group(1)

    engagement = _compute_engagement_score(
        redirect_count, unchallenged_count, wrong_call_count, has_pattern=False,
    )

    return SessionMetrics(
        date=date,
        topic=session_path.stem,
        redirect_count=redirect_count,
        unchallenged_count=unchallenged_count,
        wrong_call_count=wrong_call_count,
        override_rate=round(override_rate, 3),
        engagement_score=engagement,
    )


# ---------------------------------------------------------------------------
# Trend analysis
# ---------------------------------------------------------------------------

SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"


def _sparkline(values: list[float]) -> str:
    """Render a list of values as a sparkline string."""
    if not values:
        return ""
    mn, mx = min(values), max(values)
    rng = mx - mn
    if rng == 0:
        idx = 4  # middle
        return SPARKLINE_CHARS[idx] * len(values)
    return "".join(
        SPARKLINE_CHARS[min(len(SPARKLINE_CHARS) - 1, int((v - mn) / rng * (len(SPARKLINE_CHARS) - 1)))]
        for v in values
    )


def _moving_average(values: list[float], window: int) -> float:
    """Compute moving average over the last `window` values."""
    if not values:
        return 0.0
    tail = values[-window:]
    return round(sum(tail) / len(tail), 2)


def _trend_direction(values: list[float], window: int = 3) -> str:
    """Determine if recent values are trending up, down, or flat.

    Compares the average of the last `window` values against the
    average of the preceding `window` values.
    """
    if len(values) < window + 1:
        return "flat"
    recent = values[-window:]
    prior = values[-(window * 2):-window] if len(values) >= window * 2 else values[:-window]
    if not prior:
        return "flat"

    recent_avg = sum(recent) / len(recent)
    prior_avg = sum(prior) / len(prior)

    # Threshold: 10% relative change to count as a trend
    if prior_avg == 0:
        return "up" if recent_avg > 0 else "flat"
    pct_change = (recent_avg - prior_avg) / prior_avg
    if pct_change > 0.10:
        return "up"
    elif pct_change < -0.10:
        return "down"
    return "flat"


def _build_trend(values: list[float]) -> TrendData:
    """Build full trend data from a list of per-session values."""
    return TrendData(
        direction=_trend_direction(values),
        moving_avg_5=_moving_average(values, 5),
        moving_avg_10=_moving_average(values, 10),
        values=values,
        sparkline=_sparkline(values),
    )


def _detect_coasting(sessions: list[SessionMetrics]) -> list[CoastingAlert]:
    """Detect coasting patterns and generate alerts."""
    alerts: list[CoastingAlert] = []

    if len(sessions) < 3:
        return alerts

    # Check: override_rate drop >30% over last 3 sessions
    recent_3 = sessions[-3:]
    rates = [s.override_rate for s in recent_3]

    if len(sessions) >= 6:
        prior_3 = sessions[-6:-3]
        prior_avg = sum(s.override_rate for s in prior_3) / len(prior_3)
        recent_avg = sum(rates) / len(rates)

        if prior_avg > 0 and (prior_avg - recent_avg) / prior_avg > 0.30:
            alerts.append(CoastingAlert(
                message=(
                    f"Override rate dropped {((prior_avg - recent_avg) / prior_avg * 100):.0f}% "
                    f"over last 3 sessions ({prior_avg:.0%} -> {recent_avg:.0%}). "
                    f"Are you coasting?"
                ),
                severity="warning",
                sessions_involved=[s.date for s in recent_3],
            ))

    # Check: 3 consecutive sessions with zero redirects
    if all(s.redirect_count == 0 for s in recent_3):
        alerts.append(CoastingAlert(
            message="Zero redirects in last 3 sessions. No steering at all.",
            severity="critical",
            sessions_involved=[s.date for s in recent_3],
        ))

    # Check: engagement score dropping steadily
    if len(sessions) >= 3:
        scores = [s.engagement_score for s in sessions[-3:]]
        if scores == sorted(scores, reverse=True) and scores[0] - scores[-1] > 15:
            alerts.append(CoastingAlert(
                message=(
                    f"Engagement score declining: "
                    f"{scores[0]:.0f} -> {scores[1]:.0f} -> {scores[2]:.0f}"
                ),
                severity="warning",
                sessions_involved=[s.date for s in sessions[-3:]],
            ))

    return alerts


# ---------------------------------------------------------------------------
# Main entry points
# ---------------------------------------------------------------------------

def collect_from_digests(root: Path) -> list[SessionMetrics]:
    """Parse all digest files and return per-session metrics."""
    digest_dir = root / "decisions" / "digests"
    if not digest_dir.is_dir():
        return []

    sessions: list[SessionMetrics] = []
    for path in sorted(digest_dir.glob("*.md")):
        sessions.append(parse_digest_metrics(path))

    return sessions


def collect_from_sessions(session_paths: list[Path]) -> list[SessionMetrics]:
    """Derive metrics from JSONL session logs."""
    return [metrics_from_session_log(p) for p in sorted(session_paths)]


def build_summary(sessions: list[SessionMetrics]) -> MetricsSummary:
    """Build aggregate metrics summary from per-session data."""
    if not sessions:
        return MetricsSummary()

    total = len(sessions)
    avg_engagement = round(sum(s.engagement_score for s in sessions) / total, 1)
    avg_override = round(sum(s.override_rate for s in sessions) / total, 3)

    override_values = [s.override_rate for s in sessions]
    engagement_values = [s.engagement_score for s in sessions]

    return MetricsSummary(
        sessions=sessions,
        total_sessions=total,
        avg_engagement_score=avg_engagement,
        avg_override_rate=avg_override,
        total_redirects=sum(s.redirect_count for s in sessions),
        total_unchallenged=sum(s.unchallenged_count for s in sessions),
        total_wrong_calls=sum(s.wrong_call_count for s in sessions),
        override_rate_trend=_build_trend(override_values),
        engagement_trend=_build_trend(engagement_values),
        coasting_alerts=_detect_coasting(sessions),
    )
