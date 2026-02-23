# decision-trail

**Coding is solved. Thinking isn't. Capture the human layer.**

---

## The Shift

AI writes the code now. [Boris Cherny](https://x.com/lennysan/status/2024896611818897438), creator of Claude Code, hasn't written a line by hand since November. Claude Code accounts for 4% of public GitHub commits. Anthropic has seen a 200% increase in engineer productivity.

Matt Shumer [describes the inflection](https://shumer.dev/something-big-is-happening): "I describe what I want built...and it just...appears." Task completion capacity is doubling every 4-7 months. Models are helping build the next generation of models. This is accelerating.

So what's left?

> *"The best software engineers won't be the fastest coders, but those who know when to distrust AI."*
> — [Addy Osmani](https://addyosmani.com/blog/next-two-years/), Google Chrome

The answer is converging from every direction:

- **Taste** — knowing what to build, what to delete, and [what not to ship](https://addyosmani.com/blog/next-two-years/)
- **Judgment** — knowing when the AI is wrong and why
- **Direction** — framing the problem before any system takes action

These skills are now the bottleneck. And they're invisible.

## The Problem

Your GitHub shows what got committed. It doesn't show:

- What the AI suggested that you rejected
- Where your judgment overrode the default
- Why you chose one approach when both were viable
- What you killed before it wasted a week

There's no artefact for thinking. Hiring managers [test for judgment now](https://gritdaily.com/software-dev-hiring-shifting-from-syntax-to-judgment/) (54x increase in aptitude-style assessments since 2024), but they're doing it in 45-minute interviews because nothing else exists.

Meanwhile, [tacit knowledge is disappearing](https://aijourn.com/are-we-automating-professional-services-into-a-knowledge-crisis/). Juniors used to learn by watching seniors think. Remote work + AI broke that pipeline. Employment for 22-25 year olds in AI-exposed roles [fell 6%](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/) between 2022 and 2025. The stepping-stone tasks that built judgment are being automated away.

## Beyond Fluency

Anthropic's [AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index) measures baseline human-AI competency across four dimensions: Delegation, Description, Discernment, and Diligence. It's a useful floor. But their own research reveals the ceiling problem: when AI produces polished output, people become *less* critical — not more. They call it the artifact paradox. Users provide better upfront direction but ask fewer questions and do less fact-checking on complex tasks. Fluency without vigilance.

Victoria Ferrier [goes further](https://victoriaferrier.substack.com/p/ai-is-the-wrong-unit-of-analysis): AI readiness isn't a technology problem, it's a human capacity problem. Organizations asking "how do we become AI-ready?" are treating an adaptive challenge as a technical one. The real question is whether people have the judgment infrastructure to navigate complexity — what she calls Learning Power: mindful agency, sense-making, curiosity, and the ability to hold uncertainty without flinching.

**Fluency is knowing how to use AI. What matters now is knowing how to think alongside it.**

The decision trail captures what sits above fluency:

- **Trust calibration** — when you let the AI run vs when you check its work
- **Resistance to the artifact paradox** — challenging polished output, not accepting it
- **Meta-cognition** — correcting the AI's process, not just its output
- **Strategic killing** — knowing what not to build, even when the AI builds it beautifully
- **Pattern recognition** — seeing across sessions, not just within them

These aren't skills you learn in a course. They're dispositions you develop through practice. The decision trail makes them visible.

## How It Works

**One command. Zero friction.**

1. Start any Claude Code session
2. Type `/marmite`
3. Work normally
4. Say "wrap" when you're done

That's it. Claude silently tracks the moments where you redirect, reframe, make a judgment call, or kill a direction. On "wrap", it compiles a digest and commits it to your repo.

No manual logging. No forms. No interruptions. You build, it watches.

## What a Digest Looks Like

```markdown
# 2026-02-23 — GCSE + IB paper ingestion

Long session — download scripts, parsers, bulk extraction across three new
exam boards. Heavy use of background tasks running in parallel.

- Set a clear quality bar early: "happy with the past 2,3 years of papers"
  — stopped Claude from chasing diminishing returns on older data.
- Delegated eng judgement on PR strategy but pressure-tested the answer by
  checking Claude understood the dependency chain before approving.
- Caught Claude fabricating context — challenged a summary that didn't match
  what the open PRs had done. Made Claude reconcile before moving on.
- API credits ran out three times. No frustration, just reset and re-run.
  Treated infrastructure hiccups as infrastructure, not blockers.
- Caught the session digest itself leaking internal architecture. Redirected
  the format and updated the skill — meta-decision about what's safe to share.
- Pattern: trusts Claude to run autonomously on mechanical work, but checks
  in on anything involving judgement or narrative.
```

Narrative, not forensic. Someone should skim it in 15 seconds and understand how this person works with AI — not what was built.

## Surfacing Patterns

Individual digests capture sessions. Over time, the real signal is in the patterns across them.

Run `/trail` periodically to generate a synthesis:

```markdown
# Synthesis — February 2026 (3 sessions)

## Recurring patterns
- Consistently diagnoses root cause before fixing. Two sessions where the
  obvious fix was wrong and investigation saved significant rework.
- Delegates mechanical execution freely but always verifies narrative and
  judgement calls. Trust is calibrated by task type, not blanket.
- Kills directions quickly when evidence doesn't support them. No sunk
  cost attachment.

## Evolution
- First session: accepted AI-generated digests at face value. By third
  session: caught the digest leaking architecture and rewrote the skill.
  Meta-awareness of AI output quality is increasing.

## Beyond fluency
- Artifact paradox resistance: actively challenges polished output in 2/3
  sessions. This is the exact behavior Anthropic's research shows most
  users stop doing.
```

The synthesis surfaces what you can't see from any single session — whether your collaboration instincts are sharpening, plateauing, or eroding.

## Who This Is For

- **Engineers** who want proof they can think, not just type. Your GitHub contributions graph doesn't distinguish between you and your AI.
- **PMs and operators** who build with AI tools and need to show the direction was theirs.
- **Hiring managers** looking for a signal beyond code tests. [Competence is now defined by how well you think, not what you type.](https://gritdaily.com/software-dev-hiring-shifting-from-syntax-to-judgment/)
- **Teams** where tacit knowledge is being lost. The digest is a [knowledge transfer mechanism](https://aijourn.com/are-we-automating-professional-services-into-a-knowledge-crisis/) — juniors can read how seniors think.

## Setup

Copy the skills to your global Claude commands:

```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/marmite.md \
  https://raw.githubusercontent.com/ElliotJLT/decision-trail/main/.claude/commands/marmite.md
curl -o ~/.claude/commands/trail.md \
  https://raw.githubusercontent.com/ElliotJLT/decision-trail/main/.claude/commands/trail.md
```

Now `/marmite` (session tracking) and `/trail` (synthesis) work in every project. No init, no config, no dependencies.

### CLI (optional)

If you want to parse old session logs from the command line:

```bash
pip install decision-trail

# Generate a digest from a past session
decision-trail digest ~/.claude/projects/.../session.jsonl --commit

# Inspect what the extractor picks up
decision-trail extract ~/.claude/projects/.../session.jsonl
```

## The Thesis

Fluency is table stakes. Everyone will be fluent. [Anthropic can measure it](https://www.anthropic.com/research/AI-fluency-index), courses can teach it, and within a year the floor will be high enough that it stops being a differentiator.

What can't be taught — and can't be faked — is the human layer above fluency: the instinct to challenge, the discipline to kill, the judgment to know when the AI is confidently wrong. [Victoria Ferrier calls it Learning Power](https://victoriaferrier.substack.com/p/ai-is-the-wrong-unit-of-analysis). [Matt Shumer calls it the thing that makes you irreplaceable](https://shumer.dev/something-big-is-happening). Addy Osmani calls it taste.

decision-trail makes that layer visible. Not as a score. Not as a self-assessment. As a timestamped, public record of how you actually think when you're building with AI.

This isn't about proving you're better than the AI. It's about proving you made the AI better.

## Reading

- [Anthropic: The AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index) — Measuring human-AI collaboration, and why polished output makes people less critical
- [Victoria Ferrier: AI Is The Wrong Unit of Analysis](https://victoriaferrier.substack.com/p/ai-is-the-wrong-unit-of-analysis) — Human capacity, not AI capability, determines success
- [Matt Shumer: Something Big Is Happening](https://shumer.dev/something-big-is-happening) — The inflection point and why differentiation matters now
- [Taste Is the New Bottleneck](https://www.designative.info/2026/02/01/taste-is-the-new-bottleneck-design-strategy-and-judgment-in-the-age-of-agents-and-vibe-coding/) — Why judgment can no longer remain tacit
- [Addy Osmani: The Next Two Years of Software Engineering](https://addyosmani.com/blog/next-two-years/) — What makes engineers valuable when AI codes
- [Hiring Is Shifting From Syntax to Judgment](https://gritdaily.com/software-dev-hiring-shifting-from-syntax-to-judgment/) — 54x increase in aptitude assessments
- [Are We Automating Into a Knowledge Crisis?](https://aijourn.com/are-we-automating-professional-services-into-a-knowledge-crisis/) — The tacit knowledge gap
- [Boris Cherny: What Happens After Coding Is Solved](https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens) — Head of Claude Code on the builder role
- [AI vs Gen Z: The Junior Developer Crisis](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/) — How stepping-stone tasks are disappearing

## License

MIT
