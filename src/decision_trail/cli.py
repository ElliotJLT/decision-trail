"""CLI commands for decision-trail."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import click
from rich.console import Console

from . import __version__

console = Console()

DECISIONS_DIR = "decisions"


@click.group()
@click.version_option(version=__version__, prog_name="decision-trail")
def cli():
    """AI fluency is measurable. AI judgment isn't. Capture the difference.

    The primary way to use decision-trail is /marmite in Claude Code.
    This CLI exists for parsing session logs after the fact.
    """
    pass


@cli.command()
@click.argument("session_path", type=click.Path(exists=True, path_type=Path))
@click.option("--path", default=".", help="Project root path")
@click.option("--commit", is_flag=True, help="Auto-commit the digest to git")
def digest(session_path: Path, path: str, commit: bool):
    """Generate a session digest from a Claude Code session log.

    Parses a session and produces a flat list of moments where the human
    directed the AI. No scoring, no vanity metrics.

    SESSION_PATH is the path to a .jsonl session file.
    """
    from .extractor import extract_from_session
    from .digest import generate_digest

    root = Path(path).resolve()
    digest_dir = root / DECISIONS_DIR / "digests"
    digest_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[dim]Parsing session: {session_path}[/dim]\n")
    candidates = extract_from_session(session_path)
    digest_text = generate_digest(session_path, candidates)

    # Write digest file
    today = date.today().isoformat()
    existing = list(digest_dir.glob(f"{today}-*.md"))
    seq = len(existing) + 1
    digest_file = digest_dir / f"{today}-session-{seq}.md"
    digest_file.write_text(digest_text)
    console.print(f"[bold green]Digest written:[/bold green] {digest_file.relative_to(root)}")

    if commit:
        from .git import git_add_and_commit, is_git_repo

        if not is_git_repo(root):
            console.print("[yellow]Not a git repo — skipping commit.[/yellow]")
            return

        commit_msg = f"digest: {today}"
        sha = git_add_and_commit(digest_file, commit_msg)
        if sha:
            console.print(f"[bold green]Committed:[/bold green] {sha}")


@cli.command()
@click.argument("session_path", type=click.Path(exists=True, path_type=Path))
@click.option("--path", default=".", help="Project root path")
def extract(session_path: Path, path: str):
    """Show decision candidates from a Claude Code session log.

    Useful for inspecting what the extractor picks up from a session.

    SESSION_PATH is the path to a .jsonl session file.
    """
    from .extractor import extract_from_session

    console.print(f"[dim]Parsing session: {session_path}[/dim]\n")
    candidates = extract_from_session(session_path)

    if not candidates:
        console.print("[yellow]No decision candidates found in this session.[/yellow]")
        return

    console.print(f"[bold]Found {len(candidates)} candidate(s):[/bold]\n")

    for i, candidate in enumerate(candidates, 1):
        console.print(f"[bold cyan]{i}.[/bold cyan] [{candidate.category}] {candidate.summary}")
        if candidate.ai_suggestion:
            console.print(f"   [blue]AI:[/blue] {candidate.ai_suggestion[:100]}")
        if candidate.human_response:
            console.print(f"   [yellow]Human:[/yellow] {candidate.human_response[:100]}")
        console.print()


@cli.command()
@click.option("--path", default=".", help="Project root path")
@click.option(
    "--format", "fmt",
    type=click.Choice(["md", "html", "both"]),
    default="md",
    help="Output format",
)
def profile(path: str, fmt: str):
    """Generate a shareable decision profile.

    Reads all digests and synthesis files, produces a profile page.
    Markdown goes to decisions/profile.md, HTML to docs/profile/index.html.
    """
    from .profile import build_profile
    from .renderer import write_profile

    root = Path(path).resolve()
    data = build_profile(root)

    if data.total_sessions == 0:
        console.print("[yellow]No digests found. Run /marmite in a session first.[/yellow]")
        return

    written = write_profile(data, root, fmt)

    for p in written:
        console.print(f"[bold green]Written:[/bold green] {p.relative_to(root)}")

    console.print(
        f"\n[dim]{data.total_sessions} session(s) since {data.active_since}. "
        f"{len(data.highlighted_moments)} highlighted moment(s).[/dim]"
    )


@cli.command()
@click.option("--path", default=".", help="Project root path")
@click.option(
    "--from-sessions",
    "session_dir",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Derive metrics from JSONL session logs in this directory instead of digests",
)
def metrics(path: str, session_dir: Path | None):
    """Cognitive engagement dashboard.

    Shows per-session metrics, trends, and coasting alerts derived from
    your digest files. Use --from-sessions to derive metrics directly
    from JSONL session logs instead.
    """
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text

    from .metrics import (
        collect_from_digests,
        collect_from_sessions,
        build_summary,
    )

    root = Path(path).resolve()

    if session_dir:
        session_paths = sorted(session_dir.glob("*.jsonl"))
        if not session_paths:
            console.print("[yellow]No .jsonl files found in that directory.[/yellow]")
            return
        console.print(f"[dim]Parsing {len(session_paths)} session log(s)...[/dim]\n")
        sessions = collect_from_sessions(session_paths)
    else:
        sessions = collect_from_digests(root)

    if not sessions:
        console.print("[yellow]No digests found. Run /marmite in a session first.[/yellow]")
        return

    summary = build_summary(sessions)

    # --- Per-session table ---
    table = Table(title="Session Metrics", show_lines=False, pad_edge=False)
    table.add_column("Date", style="dim", no_wrap=True)
    table.add_column("Topic", max_width=30)
    table.add_column("Redirects", justify="right", style="cyan")
    table.add_column("Unchallenged", justify="right", style="yellow")
    table.add_column("Wrong", justify="right", style="red")
    table.add_column("Override %", justify="right")
    table.add_column("Engagement", justify="right", style="bold")

    for s in sessions:
        # Color-code override rate
        rate_str = f"{s.override_rate:.0%}"
        if s.override_rate >= 0.4:
            rate_style = "green"
        elif s.override_rate >= 0.2:
            rate_style = "yellow"
        else:
            rate_style = "red"

        # Color-code engagement score
        eng_str = f"{s.engagement_score:.0f}"
        if s.engagement_score >= 60:
            eng_style = "bold green"
        elif s.engagement_score >= 35:
            eng_style = "bold yellow"
        else:
            eng_style = "bold red"

        topic_display = s.topic[:30] if s.topic else "—"

        table.add_row(
            s.date or "—",
            topic_display,
            str(s.redirect_count),
            str(s.unchallenged_count),
            str(s.wrong_call_count),
            f"[{rate_style}]{rate_str}[/{rate_style}]",
            f"[{eng_style}]{eng_str}[/{eng_style}]",
        )

    console.print(table)
    console.print()

    # --- Trend sparklines ---
    trend_arrow = {"up": "[green]trending up[/green]", "down": "[red]trending down[/red]", "flat": "[dim]flat[/dim]"}

    or_trend = summary.override_rate_trend
    eng_trend = summary.engagement_trend

    console.print("[bold]Trends[/bold]")
    console.print(
        f"  Override rate:    {or_trend.sparkline}  "
        f"{trend_arrow.get(or_trend.direction, 'flat')}  "
        f"(MA5: {or_trend.moving_avg_5:.0%}  MA10: {or_trend.moving_avg_10:.0%})"
    )
    console.print(
        f"  Engagement score: {eng_trend.sparkline}  "
        f"{trend_arrow.get(eng_trend.direction, 'flat')}  "
        f"(MA5: {eng_trend.moving_avg_5:.0f}  MA10: {eng_trend.moving_avg_10:.0f})"
    )
    console.print()

    # --- Aggregates ---
    console.print("[bold]Aggregate[/bold]")
    console.print(f"  Sessions: {summary.total_sessions}")
    console.print(f"  Avg engagement: {summary.avg_engagement_score:.0f}/100")
    console.print(f"  Avg override rate: {summary.avg_override_rate:.0%}")
    console.print(
        f"  Totals: {summary.total_redirects} redirects, "
        f"{summary.total_unchallenged} unchallenged, "
        f"{summary.total_wrong_calls} wrong calls"
    )
    console.print()

    # --- Coasting alerts ---
    if summary.coasting_alerts:
        for alert in summary.coasting_alerts:
            style = "bold red" if alert.severity == "critical" else "bold yellow"
            icon = "!!" if alert.severity == "critical" else "!"
            console.print(Panel(
                f"[{style}]{icon} {alert.message}[/{style}]",
                title="[bold]Coasting Alert[/bold]",
                border_style="red" if alert.severity == "critical" else "yellow",
            ))


@cli.command()
@click.option("--path", default=".", help="Project root path")
@click.option("--port", default=8000, help="Port for local preview")
def serve(path: str, port: int):
    """Local preview of your HTML profile.

    Generates the HTML profile and serves it at http://localhost:PORT.
    """
    import http.server
    import functools

    from .profile import build_profile
    from .renderer import write_profile

    root = Path(path).resolve()
    data = build_profile(root)

    if data.total_sessions == 0:
        console.print("[yellow]No digests found. Run /marmite in a session first.[/yellow]")
        return

    write_profile(data, root, "html")
    serve_dir = root / "docs" / "profile"

    console.print(f"[bold green]Serving profile at[/bold green] http://localhost:{port}")
    console.print("[dim]Press Ctrl+C to stop.[/dim]\n")

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(serve_dir))
    server = http.server.HTTPServer(("", port), handler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[dim]Stopped.[/dim]")
        server.server_close()


if __name__ == "__main__":
    cli()
