"""CLI commands for decision-trail."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import click
from rich.console import Console

from . import __version__
from .models import Alternative, DecisionRecord, load_decisions, next_decision_number
from .templates import SKILL_TEMPLATE

console = Console()

DECISIONS_DIR = "decisions"


@click.group()
@click.version_option(version=__version__, prog_name="decision-trail")
def cli():
    """Show your thinking, not just your code.

    Capture human decisions during AI-assisted development.
    """
    pass


@cli.command()
@click.option("--path", default=".", help="Project root path")
def init(path: str):
    """Initialize decision-trail in a project."""
    root = Path(path).resolve()
    decisions_dir = root / DECISIONS_DIR
    skill_dir = root / ".claude" / "commands"

    # Create decisions directory
    decisions_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]Created[/green] {decisions_dir.relative_to(root)}/")

    # Drop in Claude Code skill
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "decide.md"
    skill_file.write_text(SKILL_TEMPLATE)
    console.print(f"[green]Created[/green] {skill_file.relative_to(root)}")

    console.print()
    console.print("[bold green]decision-trail initialized.[/bold green]")
    console.print()
    console.print("Next steps:")
    console.print("  decision-trail new \"Your first decision\"")
    console.print("  Or use [bold]/decide[/bold] in Claude Code")


@cli.command()
@click.argument("title")
@click.option("--path", default=".", help="Project root path")
@click.option("--non-interactive", is_flag=True, help="Skip prompts, write template")
def new(title: str, path: str, non_interactive: bool):
    """Create a new decision record interactively."""
    root = Path(path).resolve()
    decisions_dir = root / DECISIONS_DIR

    if not decisions_dir.exists():
        console.print("[red]No decisions/ directory found. Run 'decision-trail init' first.[/red]")
        raise SystemExit(1)

    number = next_decision_number(decisions_dir)

    if non_interactive:
        record = DecisionRecord(
            number=number,
            title=title,
            date=date.today().isoformat(),
            status="accepted",
            confidence="medium",
        )
    else:
        console.print(f"\n[bold]Recording decision DT-{number:03d}: {title}[/bold]\n")

        context = click.prompt("What situation required this decision?", default="")
        decision_text = click.prompt("What did you choose?", default="")
        ai_suggestion = click.prompt("What did the AI suggest? (leave blank if N/A)", default="")
        human_take = click.prompt("Why did you agree/disagree/modify the AI's suggestion?", default="")

        confidence = click.prompt(
            "Confidence in this decision",
            type=click.Choice(["low", "medium", "high"]),
            default="medium",
        )

        model = click.prompt("Which AI model? (leave blank to skip)", default="")
        tags_raw = click.prompt("Tags (space-separated, e.g. #arch #tooling)", default="")
        tags = [t.strip() for t in tags_raw.split() if t.startswith("#")] if tags_raw else []

        # Alternatives
        alternatives = []
        if click.confirm("Add alternatives considered?", default=False):
            while True:
                opt = click.prompt("  Option name (blank to finish)", default="")
                if not opt:
                    break
                pros = click.prompt("  Pros", default="")
                cons = click.prompt("  Cons", default="")
                source = click.prompt(
                    "  Source",
                    type=click.Choice(["AI suggested", "Human proposed", "Team discussed"]),
                    default="Human proposed",
                )
                alternatives.append(Alternative(opt, pros, cons, source))

        consequences = click.prompt("Any consequences or follow-ups?", default="")

        record = DecisionRecord(
            number=number,
            title=title,
            date=date.today().isoformat(),
            status="accepted",
            tags=tags,
            model=model,
            confidence=confidence,
            context=context,
            decision=decision_text,
            ai_suggestion=ai_suggestion,
            human_take=human_take,
            alternatives=alternatives,
            consequences=consequences,
        )

    # Write file
    filepath = decisions_dir / record.filename
    filepath.write_text(record.to_markdown())
    console.print(f"\n[bold green]Written:[/bold green] {filepath.relative_to(root)}")


@cli.command()
@click.option("--path", default=".", help="Project root path")
def view(path: str):
    """View all decisions as a timeline."""
    from .viewer import render_timeline

    root = Path(path).resolve()
    decisions_dir = root / DECISIONS_DIR

    if not decisions_dir.exists():
        console.print("[red]No decisions/ directory found. Run 'decision-trail init' first.[/red]")
        raise SystemExit(1)

    records = load_decisions(decisions_dir)
    render_timeline(records, console)


@cli.command()
@click.argument("session_path", type=click.Path(exists=True, path_type=Path))
@click.option("--path", default=".", help="Project root path")
def extract(session_path: Path, path: str):
    """Extract decision candidates from a Claude Code session log.

    SESSION_PATH is the path to a .jsonl session file.
    """
    from .extractor import extract_from_session

    root = Path(path).resolve()
    decisions_dir = root / DECISIONS_DIR

    if not decisions_dir.exists():
        console.print("[red]No decisions/ directory found. Run 'decision-trail init' first.[/red]")
        raise SystemExit(1)

    console.print(f"[dim]Parsing session: {session_path}[/dim]\n")
    candidates = extract_from_session(session_path)

    if not candidates:
        console.print("[yellow]No decision candidates found in this session.[/yellow]")
        return

    console.print(f"[bold]Found {len(candidates)} decision candidate(s):[/bold]\n")

    for i, candidate in enumerate(candidates, 1):
        console.print(f"[bold cyan]{i}.[/bold cyan] [{candidate.category}] {candidate.summary}")
        if candidate.ai_suggestion:
            console.print(f"   [blue]AI:[/blue] {candidate.ai_suggestion[:100]}")
        if candidate.human_response:
            console.print(f"   [yellow]Human:[/yellow] {candidate.human_response[:100]}")
        console.print()

    # Ask which to save
    console.print("[dim]Enter numbers to save (comma-separated), or 'all', or 'none':[/dim]")
    selection = click.prompt("Save", default="none")

    if selection.lower() == "none":
        return

    if selection.lower() == "all":
        indices = list(range(len(candidates)))
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(",")]
        except ValueError:
            console.print("[red]Invalid selection.[/red]")
            return

    for idx in indices:
        if 0 <= idx < len(candidates):
            candidate = candidates[idx]
            number = next_decision_number(decisions_dir)
            title = click.prompt(f"  Title for candidate {idx + 1}", default=candidate.summary[:60])

            record = DecisionRecord(
                number=number,
                title=title,
                date=date.today().isoformat(),
                status="accepted",
                context=candidate.context,
                decision=candidate.human_response or candidate.summary,
                ai_suggestion=candidate.ai_suggestion,
                human_take=candidate.human_response,
                confidence=candidate.confidence,
                session_ref=str(session_path),
            )

            filepath = decisions_dir / record.filename
            filepath.write_text(record.to_markdown())
            console.print(f"  [green]Saved:[/green] {filepath.name}")


if __name__ == "__main__":
    cli()
