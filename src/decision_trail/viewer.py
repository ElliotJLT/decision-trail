"""Rich terminal renderer for decision records."""

from __future__ import annotations

from typing import List

from rich.columns import Columns
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .models import DecisionRecord

CONFIDENCE_COLORS = {
    "high": "green",
    "medium": "yellow",
    "low": "red",
}

STATUS_COLORS = {
    "accepted": "green",
    "proposed": "blue",
    "superseded": "dim",
    "deprecated": "red",
}


def render_timeline(records: List[DecisionRecord], console: Console | None = None) -> None:
    """Render decisions as a rich timeline in the terminal."""
    if console is None:
        console = Console()

    if not records:
        console.print("[dim]No decisions found.[/dim]")
        return

    console.print()
    console.print(
        Text("Decision Trail", style="bold magenta"),
        Text(f"  ({len(records)} decision{'s' if len(records) != 1 else ''})", style="dim"),
    )
    console.print()

    for record in records:
        _render_decision_panel(record, console)


def _render_decision_panel(record: DecisionRecord, console: Console) -> None:
    """Render a single decision as a rich panel."""
    conf_color = CONFIDENCE_COLORS.get(record.confidence, "white")
    status_color = STATUS_COLORS.get(record.status, "white")

    # Build header badges
    badges = []
    badges.append(f"[{status_color}]{record.status}[/{status_color}]")
    badges.append(f"[{conf_color}]confidence: {record.confidence}[/{conf_color}]")
    if record.model:
        badges.append(f"[cyan]{record.model}[/cyan]")
    if record.tags:
        badges.append(f"[dim]{' '.join(record.tags)}[/dim]")

    header = "  ".join(badges)

    # Build body
    body_parts = []

    if record.context:
        body_parts.append(f"[bold]Context:[/bold] {escape(record.context[:200])}")

    if record.decision:
        body_parts.append(f"[bold]Decision:[/bold] {escape(record.decision[:200])}")

    if record.ai_suggestion:
        body_parts.append(f"[bold blue]AI said:[/bold blue] {escape(record.ai_suggestion[:200])}")

    if record.human_take:
        body_parts.append(f"[bold yellow]Human said:[/bold yellow] {escape(record.human_take[:200])}")

    if record.alternatives:
        table = Table(show_header=True, header_style="bold", box=None, padding=(0, 1))
        table.add_column("Option", style="white")
        table.add_column("Pros", style="green")
        table.add_column("Cons", style="red")
        table.add_column("Source", style="cyan")
        for alt in record.alternatives:
            table.add_row(alt.option, alt.pros, alt.cons, alt.source)
        body_parts.append("")  # spacing before table

    body = "\n".join(body_parts)

    panel = Panel(
        body,
        title=f"[bold]{record.id}: {escape(record.title)}[/bold]",
        subtitle=f"[dim]{record.date}[/dim]  {header}",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print(panel)

    # Print alternatives table outside panel for readability
    if record.alternatives:
        table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
        table.add_column("Option", style="white")
        table.add_column("Pros", style="green")
        table.add_column("Cons", style="red")
        table.add_column("Source", style="cyan")
        for alt in record.alternatives:
            table.add_row(alt.option, alt.pros, alt.cons, alt.source)
        console.print("  ", table)

    console.print()
