# decision-trail

[![Decision Profile](https://img.shields.io/badge/profile-live-blue)](https://elliotjlt.github.io/decision-trail/)

**AI fluency is a solved problem. AI judgment isn't.**

---

## The Artifact Paradox

Anthropic studied [nearly 10,000 conversations](https://www.anthropic.com/research/AI-fluency-index) to measure how effectively people work with AI. The headline finding: iteration makes you better. Obviously.

The buried finding is the one that matters: when AI produces polished, professional-looking output, users become *less* critical. They give better upfront direction but stop questioning, stop fact-checking, stop pushing back. Anthropic calls it the **artifact paradox**. The better the AI gets, the more humans coast.

There's no feedback loop. Tests catch bad code. Editors catch bad writing. Nothing catches bad judgment in AI-assisted work. You can't improve what you can't see.

## Fluency Is the Floor

Anthropic's [4D framework](https://www.anthropic.com/ai-fluency/overview) — Delegation, Description, Discernment, Diligence — defines baseline AI competency. It's real and it's useful. It'll also be universal within 18 months. Courses will teach it. Everyone will pass.

Victoria Ferrier [argues](https://victoriaferrier.substack.com/p/ai-is-the-wrong-unit-of-analysis) this is solving the wrong problem. AI readiness isn't a technology problem — it's a human capacity problem. Organizations training people to prompt better are treating an adaptive challenge as a technical one. The real question is whether people have the judgment to navigate complexity when the AI is confidently wrong.

Matt Shumer [puts a clock on it](https://shumer.dev/something-big-is-happening): task completion capacity is doubling every 4-7 months. Models are helping build the next generation of models. When everyone builds with AI, the only differentiator is the human direction layer — taste, judgment, and the willingness to override.

**The window where judgment differentiates you is narrow and open now.**

## What Sits Above Fluency

These aren't skills you learn in a course. They're dispositions you develop through practice:

- **Trust calibration** — knowing when to let the AI run vs when to check its work. Not blanket trust. Calibrated, task-by-task.
- **Resistance to the artifact paradox** — challenging output that looks polished. The more professional it seems, the harder you look.
- **Meta-cognition** — correcting the AI's process, not just its output.
- **Strategic killing** — deciding what not to build, even when the AI builds it beautifully.
- **Pattern recognition** — seeing your own habits across sessions, not just within them.

The problem: none of this leaves a trace. Your GitHub shows what got committed. It doesn't show what you rejected, redirected, or killed.

## decision-trail

A practice for developing AI judgment. Like a training log for a runner — the primary value is to you.

**One command. Zero friction.**

1. Start any Claude Code session
2. Type `/marmite`
3. Work normally
4. Say "wrap" when you're done

Claude silently tracks the moments where you redirect, reframe, set a quality bar, or kill a direction. On "wrap", it compiles a digest. No manual logging. No forms. No interruptions.

### What a digest looks like

```markdown
# 2026-02-23 — eval scoring diagnosis

~4h research session. Suspected a generation problem, investigated before fixing.

- Instinct to diagnose before treating — scores looked bad but the question
  was whether the answers were wrong or the measurement was wrong. Chose to
  investigate the scorer first.
- Conservative fix philosophy: built targeted matchers with guards that would
  rather miss a match than fabricate one. Precision over recall.
- Refused to chase a low score when the test conditions were unreliable.
  Flagged it as bad data instead of reacting to the number.
- Held the fix as research rather than shipping immediately. Won't merge
  until re-validated under correct conditions.
- Pattern: diagnose root cause before touching anything, don't ship under
  uncertainty, resist the urge to fix what isn't broken.
```

Skimmable in 15 seconds. No scores. No self-assessment. Just a record of how someone actually thinks when building with AI.

### Surfacing patterns over time

Individual digests capture sessions. The real signal is in the trajectory across them.

Run `/trail` periodically to generate a synthesis:

```markdown
# Synthesis — February 2026 (3 sessions)

## Recurring patterns
- Consistently diagnoses root cause before fixing. Two sessions where the
  obvious fix was wrong and investigation saved significant rework.
- Delegates mechanical execution freely but always verifies judgement calls.
  Trust is calibrated by task type, not blanket.

## Evolution
- First session: accepted AI-generated digests at face value. By third
  session: caught the digest leaking architecture and rewrote the skill.
  Meta-awareness of AI output quality is increasing.

## Beyond fluency
- Artifact paradox resistance: actively challenges polished output in 2/3
  sessions. This is the behaviour Anthropic's research shows most users
  stop doing.
```

The synthesis surfaces whether your collaboration instincts are sharpening, plateauing, or eroding. You can't course-correct a disposition you can't see.

## Who This Is For

- **Engineers** already building with AI who want a feedback loop for judgment, not just code.
- **Tech leads** who need to develop their team's AI collaboration instincts, not just their prompt skills.
- **Hiring managers** looking for a signal beyond code tests — [aptitude assessments are up 54x since 2024](https://gritdaily.com/software-dev-hiring-shifting-from-syntax-to-judgment/) because nothing else exists.
- **Teams** where [tacit knowledge is disappearing](https://aijourn.com/are-we-automating-professional-services-into-a-knowledge-crisis/) — digests are a knowledge transfer mechanism. Juniors can read how seniors think.

## Setup

```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/marmite.md \
  https://raw.githubusercontent.com/ElliotJLT/decision-trail/main/.claude/commands/marmite.md
curl -o ~/.claude/commands/trail.md \
  https://raw.githubusercontent.com/ElliotJLT/decision-trail/main/.claude/commands/trail.md
```

`/marmite` (session tracking) and `/trail` (synthesis) now work in every project. No init, no config, no dependencies.

### CLI (optional)

```bash
pip install decision-trail

# Generate your shareable profile
decision-trail profile --format both

# Preview locally
decision-trail serve

# Parse old session logs
decision-trail digest ~/.claude/projects/.../session.jsonl --commit
```

## The Thesis

Everyone will be fluent. [Anthropic can measure it](https://www.anthropic.com/research/AI-fluency-index), courses can teach it, and the floor is rising fast enough that it stops being a differentiator.

What can't be taught is the layer above fluency: the instinct to challenge, the discipline to kill, the judgment to know when the AI is confidently wrong. [Ferrier calls it Learning Power](https://victoriaferrier.substack.com/p/ai-is-the-wrong-unit-of-analysis). [Shumer calls it the thing that makes you irreplaceable](https://shumer.dev/something-big-is-happening). [Osmani calls it taste](https://addyosmani.com/blog/next-two-years/).

decision-trail doesn't measure that layer. It develops it — by making it visible to the person who needs to see it most: you.

## Reading

- [Anthropic: The AI Fluency Index](https://www.anthropic.com/research/AI-fluency-index) — Why polished output makes people less critical
- [Victoria Ferrier: AI Is The Wrong Unit of Analysis](https://victoriaferrier.substack.com/p/ai-is-the-wrong-unit-of-analysis) — Human capacity, not AI capability, determines success
- [Matt Shumer: Something Big Is Happening](https://shumer.dev/something-big-is-happening) — The inflection point and why differentiation matters now
- [Taste Is the New Bottleneck](https://www.designative.info/2026/02/01/taste-is-the-new-bottleneck-design-strategy-and-judgment-in-the-age-of-agents-and-vibe-coding/) — Why judgment can no longer remain tacit
- [Addy Osmani: The Next Two Years](https://addyosmani.com/blog/next-two-years/) — What makes engineers valuable when AI codes
- [Hiring Is Shifting From Syntax to Judgment](https://gritdaily.com/software-dev-hiring-shifting-from-syntax-to-judgment/) — 54x increase in aptitude assessments
- [Are We Automating Into a Knowledge Crisis?](https://aijourn.com/are-we-automating-professional-services-into-a-knowledge-crisis/) — The tacit knowledge gap
- [Boris Cherny: What Happens After Coding Is Solved](https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens) — Head of Claude Code on the builder role
- [AI vs Gen Z: The Junior Developer Crisis](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/) — How stepping-stone tasks are disappearing

## License

MIT
