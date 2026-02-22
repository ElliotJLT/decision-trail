# DT-002: Rich library over custom terminal renderer

**Date:** 2026-02-22
**Status:** accepted
**Tags:** #tooling #dependencies
**Model:** claude-opus-4-6
**Confidence:** high

## Context
The `decision-trail view` command needs to render decisions as a colorful, readable timeline in the terminal. Options were building a custom renderer with ANSI codes or using an existing library.

## Decision
Use the Rich library for all terminal rendering.

## AI Suggestion
Claude suggested Rich immediately and didn't seriously consider alternatives. The suggestion was correct but the human wanted to verify it wasn't over-engineered for the use case.

## Human Take
Agreed with Claude after checking that Rich's install size (~3MB) was acceptable for a CLI tool. The panel, table, and color features are exactly what's needed. Building custom ANSI rendering would have been fun but pointless when Rich exists. Sometimes the AI's first suggestion is just right — the value is in the human verifying it, not always overriding it.

## Alternatives Considered
| Option | Pros | Cons | Source |
|--------|------|------|--------|
| Rich | Battle-tested, beautiful output, tables + panels built in | ~3MB dependency | AI suggested |
| Custom ANSI | Zero dependencies, full control | Reinventing the wheel, cross-platform pain | Human proposed |
| Textualize/Textual | TUI framework, interactive | Way too heavy for a simple viewer | AI suggested |

## Consequences
Rich is a runtime dependency. Terminal output will be consistently styled. Future features (interactive selection, progress bars) are easy to add.
