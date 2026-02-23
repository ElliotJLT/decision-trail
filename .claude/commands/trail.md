Read all digests in `decisions/digests/` and produce a synthesis.

## What to do

1. Read every file in `decisions/digests/` in chronological order.
2. Look for patterns **across** sessions, not within them. Individual digests capture moments — the synthesis captures trajectories.
3. Write the output to `decisions/synthesis/YYYY-MM.md` (one per month, overwrite if it exists).

## What to surface

Focus on the human side of the collaboration. This is about how the person works with AI over time.

**Recurring patterns:**
- Behaviors that show up in multiple sessions (e.g. always diagnoses before fixing, delegates mechanical work but checks judgement calls)
- Consistent instincts — what do they reliably catch, kill, or correct?

**Evolution:**
- What's changed since earlier sessions? More trust? Less? Different kinds of trust?
- Are they catching things they previously missed?
- Is the artifact paradox creeping in (accepting more, challenging less)?

**Beyond fluency:**
- Where do they go beyond baseline AI competency (Delegation, Description, Discernment, Diligence)?
- Specific evidence of: trust calibration, meta-cognition about the AI's process, resistance to polished-but-wrong output, strategic killing of directions

**Gaps (honest):**
- What isn't showing up that could be? (e.g. no evidence of questioning AI reasoning, or sessions getting shorter without clear reason)
- Only flag genuine gaps. Don't manufacture them.

## Format

```markdown
# Synthesis — [Month Year] ([N] sessions)

## Recurring patterns
- [2-4 bullets. Observable, evidence-based, referencing specific sessions where useful.]

## Evolution
- [How has the collaboration style changed? What's sharpening? What's drifting?]

## Beyond fluency
- [Specific evidence of above-baseline behaviors. Tie to the artifact paradox,
  trust calibration, or meta-cognition where relevant.]

## Gaps
- [Honest observations. "Nothing notable" if nothing is missing.]
```

## After writing

```bash
git add decisions/synthesis/YYYY-MM.md
git commit -m "synthesis: [month year]"
git push
```

## Rules

- This is longitudinal analysis, not a report card. No scores, no grades.
- Ground every observation in evidence from the digests. Don't infer what isn't there.
- Narrative voice. Tight. Skimmable.
- No internal project details, architecture, or code specifics. Keep it public-safe.
- If there aren't enough sessions to synthesize meaningfully (< 3), say so and commit that.
