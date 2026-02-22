# DT-001: Python over TypeScript for decision-trail

**Date:** 2026-02-22
**Status:** accepted
**Tags:** #language #architecture
**Model:** claude-opus-4-6
**Confidence:** high

## Context
Building a CLI tool to capture human decisions during AI-assisted development. Needed to choose the implementation language. The tool needs to be pip-installable, work across platforms, and be approachable for contributors.

## Decision
Python 3.9+ with click and rich.

## AI Suggestion
Claude suggested TypeScript/Node.js initially, noting it would align with the JavaScript ecosystem where many AI dev tools live. Also mentioned Rust as a "serious tool" option.

## Human Take
Overrode the TypeScript suggestion. Python is the better fit because: (1) pip install is the simplest distribution story for CLI tools, (2) click + rich give excellent CLI UX with minimal code, (3) the target audience (developers using AI tools) overwhelmingly has Python installed, (4) no build step needed. Rust was overkill for a tool that reads/writes markdown files.

## Alternatives Considered
| Option | Pros | Cons | Source |
|--------|------|------|--------|
| Python + click | Simple distribution, rich ecosystem, fast to build | Slower than compiled, version management | Human proposed |
| TypeScript/Node | Matches JS ecosystem, npm distribution | Heavier runtime, more boilerplate for CLI | AI suggested |
| Rust | Fast, single binary, serious tool vibes | Slow to build, overkill for markdown I/O | AI suggested |
| Go | Single binary, fast | Less rich CLI libraries, less familiar | Human proposed |

## Consequences
Targets Python 3.9+ for broad compatibility. Uses setuptools for packaging. Dependencies limited to click and rich — no heavy frameworks.
