# decision-trail

## Framing

This is a practice tool, not a portfolio. The framing is:

- **"AI fluency is measurable. AI judgment isn't."** — Anthropic's fluency index covers the floor. Decision-trail captures what sits above it.
- The artifact paradox is the hook: polished AI output makes people less critical. There's no feedback loop for collaboration quality. Decision-trail is that feedback loop.
- Practice, not performance. This is a training log (like a runner's log), not a CV or showcase. Primary audience is yourself. Legibility to others is a side effect.
- Never use "This is how I think" or similar personal branding language. The profile is called "Collaboration Log", not "Decision Profile".

## Architecture

- `/marmite` captures session digests — collaboration patterns, not project changelogs
- `/trail` produces monthly synthesis grounded in Anthropic's AI Fluency Index (4D framework + 13 unobservable behaviors)
- `profile` command reads digests + synthesis and renders to markdown + HTML
- Synthesis section headers: "Fluency baseline", "Beyond the index", "Trajectory", "Gaps"

## Rules for all output

- No internal project details, architecture, env vars, column names, file paths, or service names in any public-facing file (digests, synthesis, profile, README)
- Quality bar for digests: "would a senior engineer reading this learn something about how this person thinks? If not, cut it."
- Ground every synthesis observation in evidence from digests. Don't infer what isn't there.
- Watch for multi-session coordination patterns — how the user orchestrates parallel Claude sessions is signal.

## Key references

- [Anthropic AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index) — 4D framework, artifact paradox, 13 unobservable behaviors
- [Victoria Ferrier: AI Is The Wrong Unit of Analysis](https://www.linkedin.com/pulse/ai-wrong-unit-analysis-victoria-ferrier-gbasc/) — human capacity > AI capability
- [Matt Shumer: Something Big Is Happening](https://blog.mattshumer.com/p/something-big-is-happening) — differentiation urgency
