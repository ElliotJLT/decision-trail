# decision-trail

**Show your thinking, not just your code.**

A CLI tool that captures human decisions during AI-assisted development. GitHub shows what you built. decision-trail shows *why* — and where the human overrode the AI.

---

## The Problem

In AI-assisted development ("vibe coding"), the code is increasingly AI-generated. Your commit history shows *what* changed, but not:

- **What the AI suggested** that you rejected
- **Why you chose** one approach over another
- **Where your judgment** overrode the AI's recommendation
- **How confident** you were in each call

ADR (Architecture Decision Record) tools exist, but they're manual, post-hoc, and don't capture the human/AI dynamic.

## What decision-trail Does

| Standard ADR | decision-trail |
|-------------|----------------|
| Documents decisions after the fact | Captures decisions as you work |
| Who decided = always the team | Who decided = human, AI, or human overriding AI |
| No tooling integration | Claude Code `/decide` skill built in |
| Manual creation | Auto-extraction from session logs |

## Quick Start

```bash
pip install decision-trail
```

### Initialize in your project

```bash
cd your-project
decision-trail init
```

This creates a `decisions/` directory and installs the Claude Code `/decide` skill.

### Record a decision

**Option A: CLI**
```bash
decision-trail new "Use PostgreSQL over SQLite"
```

Interactive prompts walk you through context, AI suggestion, your take, alternatives, and consequences.

**Option B: Claude Code skill**

In a Claude Code session, type `/decide`. Claude will conversationally capture the decision and write it to `decisions/`.

### View your decision trail

```bash
decision-trail view
```

Renders a colorful timeline of all decisions in your terminal.

### Extract decisions from a session

```bash
decision-trail extract ~/.claude/projects/.../session.jsonl
```

Parses a Claude Code session log, finds moments where you redirected the AI or made explicit choices, and suggests decision records to create.

## Decision Record Format

```markdown
# DT-001: Use PostgreSQL over SQLite

**Date:** 2026-02-22
**Status:** accepted
**Tags:** #database #architecture
**Model:** claude-opus-4-6
**Confidence:** high

## Context
Need a database for the user service. Expected 10k+ concurrent users.

## Decision
PostgreSQL with connection pooling via pgbouncer.

## AI Suggestion
Claude suggested SQLite initially — "simpler, no separate server process,
good enough for most use cases."

## Human Take
Overrode the AI. SQLite can't handle our concurrency requirements.
The AI defaulted to the simplest option without considering our scale.
This is a case where the human's domain knowledge (knowing our traffic
projections) led to a better decision.

## Alternatives Considered
| Option | Pros | Cons | Source |
|--------|------|------|--------|
| PostgreSQL | Handles concurrency, mature, great tooling | Operational overhead | Human proposed |
| SQLite | Simple, zero config, embedded | Single-writer, no concurrent writes | AI suggested |
| MySQL | Widely used, good performance | Less feature-rich than Postgres | Human proposed |

## Consequences
Need to set up PostgreSQL in Docker for local dev.
Add pgbouncer for connection pooling in production.
```

### Fields unique to decision-trail (vs standard ADRs)

- **`AI Suggestion`** — What the AI recommended
- **`Human Take`** — Why the human agreed, disagreed, or modified
- **`Model`** — Which AI model was involved
- **`Confidence`** — How sure the human was (low/medium/high)

## Why This Matters

Your code contributions are visible on GitHub. But the *thinking* behind them isn't. In a world where AI writes most of the code, the human value is in:

1. **Knowing what to build** — product sense, user empathy
2. **Knowing when the AI is wrong** — domain expertise, judgment
3. **Making trade-offs** — speed vs quality, simple vs scalable
4. **Owning the outcome** — the human decided, not the AI

decision-trail makes this visible. It's your proof of work for the thinking, not just the typing.

## Commands

| Command | Description |
|---------|-------------|
| `decision-trail init` | Initialize in a project (creates `decisions/`, installs skill) |
| `decision-trail new "title"` | Create a new decision record interactively |
| `decision-trail view` | Render all decisions as a terminal timeline |
| `decision-trail extract <session.jsonl>` | Parse a Claude Code session for decision candidates |

## Examples

See the [`examples/`](examples/) directory for real decision records — the decisions made while building decision-trail itself (dogfooding).

## License

MIT
