"""Render ProfileData to markdown and HTML via Jinja2 templates."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .profile import ProfileData

TEMPLATE_DIR = Path(__file__).parent / "templates"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(enabled_extensions=("html",), default=False),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_markdown(profile: ProfileData) -> str:
    """Render profile to markdown."""
    env = _env()
    template = env.get_template("profile.md.j2")
    return template.render(profile=profile)


def render_html(profile: ProfileData) -> str:
    """Render profile to a standalone HTML page."""
    env = _env()
    css = (TEMPLATE_DIR / "base.css").read_text()
    template = env.get_template("profile.html.j2")
    return template.render(profile=profile, css=css)


def write_profile(profile: ProfileData, root: Path, fmt: str = "md") -> list[Path]:
    """Write profile files. fmt: 'md', 'html', or 'both'. Returns written paths."""
    written: list[Path] = []

    if fmt in ("md", "both"):
        md_path = root / "decisions" / "profile.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_markdown(profile))
        written.append(md_path)

    if fmt in ("html", "both"):
        html_dir = root / "docs" / "profile"
        html_dir.mkdir(parents=True, exist_ok=True)
        html_path = html_dir / "index.html"
        html_path.write_text(render_html(profile))
        written.append(html_path)

    return written
