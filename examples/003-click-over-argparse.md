# DT-003: Click over argparse for CLI framework

**Date:** 2026-02-22
**Status:** accepted
**Tags:** #tooling #architecture
**Model:** claude-opus-4-6
**Confidence:** high

## Context
Needed a CLI framework for the `decision-trail` command with subcommands (init, new, view, extract). Python's stdlib has argparse, but there are third-party options.

## Decision
Use Click as the CLI framework.

## AI Suggestion
Claude defaulted to Click without much discussion, which is the common pattern in AI-assisted coding — the AI picks the popular choice. This is often fine but can lead to dependency bloat if not checked.

## Human Take
Agreed with Click, but for specific reasons the AI didn't articulate: (1) Click's decorator-based API means each command is a clean function — good for a tool that might get contributed to, (2) Click handles interactive prompts natively (`click.prompt`, `click.confirm`) which the `new` command needs heavily, (3) argparse subcommand syntax is verbose and error-prone. The decision was "agree with AI but for better reasons."

## Alternatives Considered
| Option | Pros | Cons | Source |
|--------|------|------|--------|
| Click | Clean decorators, built-in prompts, well-documented | External dependency | AI suggested |
| argparse | Stdlib, no dependency | Verbose, no built-in prompts, ugly subcommand API | Human proposed |
| Typer | Modern, type-hint based, built on Click | Another layer of abstraction, less mature | AI suggested |
| Fire | Automatic CLI from functions | Too magical, poor help text control | Human proposed |

## Consequences
Click is a runtime dependency alongside Rich. Commands are defined as decorated functions in cli.py. Interactive prompts use Click's built-in prompt utilities rather than raw input().
