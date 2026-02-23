# decision-trail

**Coding is solved. Thinking isn't. Capture the human layer.**

---

## The Shift

AI writes the code now. [Boris Cherny](https://x.com/lennysan/status/2024896611818897438), creator of Claude Code, hasn't written a line by hand since November. Claude Code accounts for 4% of public GitHub commits. Anthropic has seen a 200% increase in engineer productivity.

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
# 2026-02-23 — decision-trail product direction

- Killed Chez Claude. Not differentiated.
- "article ideas are superweak" → past stories don't land, AI trends do
- "be a second brain not an echo" → stop mirroring my recent work back at me
- "I don't want a vanity metric" → raw capture, no scoring
- Chose decision-trail over bets. Clarity > cleverness.
- /marmite over manual CLI. One word in, one word out.
```

Flat list. One line per moment. Skimmable in 10 seconds. No categories, no scores, no self-assessment.

## Who This Is For

- **Engineers** who want proof they can think, not just type. Your GitHub contributions graph doesn't distinguish between you and your AI.
- **PMs and operators** who build with AI tools and need to show the direction was theirs.
- **Hiring managers** looking for a signal beyond code tests. [Competence is now defined by how well you think, not what you type.](https://gritdaily.com/software-dev-hiring-shifting-from-syntax-to-judgment/)
- **Teams** where tacit knowledge is being lost. The digest is a [knowledge transfer mechanism](https://aijourn.com/are-we-automating-professional-services-into-a-knowledge-crisis/) — juniors can read how seniors think.

## Setup

Copy the `/marmite` skill to your global Claude commands:

```bash
mkdir -p ~/.claude/commands
curl -o ~/.claude/commands/marmite.md https://raw.githubusercontent.com/ElliotJLT/decision-trail/main/.claude/commands/marmite.md
```

Now `/marmite` works in every project. No init, no config, no dependencies.

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

When everyone builds with AI, the only remaining signal is the human direction layer — taste, judgment, and the willingness to override, reframe, or kill. decision-trail makes that layer visible.

This isn't about proving you're better than the AI. It's about proving you made the AI better.

## Reading

- [Taste Is the New Bottleneck](https://www.designative.info/2026/02/01/taste-is-the-new-bottleneck-design-strategy-and-judgment-in-the-age-of-agents-and-vibe-coding/) — Why judgment can no longer remain tacit
- [Addy Osmani: The Next Two Years of Software Engineering](https://addyosmani.com/blog/next-two-years/) — What makes engineers valuable when AI codes
- [Hiring Is Shifting From Syntax to Judgment](https://gritdaily.com/software-dev-hiring-shifting-from-syntax-to-judgment/) — 54x increase in aptitude assessments
- [Are We Automating Into a Knowledge Crisis?](https://aijourn.com/are-we-automating-professional-services-into-a-knowledge-crisis/) — The tacit knowledge gap
- [Boris Cherny: What Happens After Coding Is Solved](https://www.lennysnewsletter.com/p/head-of-claude-code-what-happens) — Head of Claude Code on the builder role
- [AI vs Gen Z: The Junior Developer Crisis](https://stackoverflow.blog/2025/12/26/ai-vs-gen-z/) — How stepping-stone tasks are disappearing

## License

MIT
