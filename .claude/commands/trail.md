Read all digests in `decisions/digests/` and produce a synthesis.

## What to do

1. Read every file in `decisions/digests/` in chronological order.
2. Look for patterns **across** sessions, not within them. Individual digests capture moments — the synthesis captures trajectories.
3. Write the output to `decisions/synthesis/YYYY-MM.md` (one per month, overwrite if it exists).

## The framework

Anthropic's AI Fluency Index measures 11 observable behaviors in conversations, grouped under four competencies (the "4Ds"). Use these as a baseline lens — note where they show up, but don't label or score them.

**Delegation** — task breakdown, knowing what to give the AI vs keep
**Description** — clear articulation of goals, iterative refinement, specifying constraints
**Discernment** — questioning AI reasoning, checking facts, evaluating output quality
**Diligence** — considering consequences of AI-generated output, verifying before sharing

The fluency index also identifies **13 behaviors it cannot measure** because they happen outside the conversation. These are where decision-trail adds signal that aggregate measurement misses. Look for evidence of:

- Honest assessment of AI's role in the work (not overclaiming, not hiding it)
- Considering downstream consequences of AI-generated output before sharing
- Recognising when AI output needs human verification vs when it can be trusted
- Adapting collaboration style based on task type (not one-size-fits-all)
- Reflecting on the collaboration process itself (meta-cognition)
- Making deliberate choices about what to automate vs what to keep human

## What to surface

### Observable fluency (the 4Ds)
Note which behaviors are consistently present across sessions. Don't list all four every time — only flag what's notable. Strong discernment across 5 sessions is worth noting. Baseline delegation in every session is not.

### What the fluency index can't see
This is the unique value of decision-trail. Surface evidence of:

- **Trust calibration** — are they calibrating trust by task type? (e.g. autonomous on execution, checking on narrative). Is this consistent or evolving?
- **Artifact paradox resistance** — are they actively challenging polished output? Or is there evidence of coasting? The fluency index found that polished output makes people less critical — look for whether this is happening or being resisted.
- **Meta-cognition** — are they correcting the AI's process, not just its output? Redirecting approach, not just fixing results?
- **Strategic killing** — are they killing directions early? Or showing sunk-cost attachment?
- **Interaction style communication** — are they explicitly shaping how the AI works with them? (setting quality bars, defining what's acceptable, reframing how output should look)

### Trajectory
- What's changed since earlier sessions? More trust? Less? Different kinds?
- Are they catching things they previously missed?
- Is the artifact paradox creeping in (accepting more, challenging less)?
- Are the unobservable behaviors getting stronger or weaker?

### Gaps (honest)
- Which of the 4D behaviors are absent or weak?
- Which unobservable behaviors have no evidence?
- Are sessions getting shorter without explanation? (possible coasting signal)
- Only flag genuine gaps. Don't manufacture them.

## Format

```markdown
# Synthesis — [Month Year] ([N] sessions)

## Fluency baseline
- [Which 4D behaviors are consistently present. Brief — this is the floor.]

## Beyond the index
- [Evidence of behaviors the fluency index can't measure. This is the signal.
  Trust calibration, artifact paradox resistance, meta-cognition, strategic
  killing, interaction style shaping. Tie to specific sessions.]

## Trajectory
- [How the collaboration style is evolving across sessions. What's sharpening,
  what's drifting, what's new.]

## Gaps
- [Honest observations. Which behaviors — observable or unobservable — are
  absent. "Nothing notable" if nothing is missing.]
```

## After writing

```bash
git add decisions/synthesis/YYYY-MM.md
git commit -m "synthesis: [month year]"
git push
```

## Rules

- This is longitudinal analysis grounded in a real framework, not a report card.
- The 4Ds are the baseline. The unobservable behaviors are the differentiator. Weight accordingly.
- Ground every observation in evidence from the digests. Don't infer what isn't there.
- Narrative voice. Tight. Skimmable.
- No internal project details, architecture, or code specifics. Keep it public-safe.
- If there aren't enough sessions to synthesize meaningfully (< 3), say so and commit that.
