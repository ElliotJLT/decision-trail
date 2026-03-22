You are now tracking this session for decision-trail.

Silently note moments where the user redirects you, reframes a problem, makes a judgment call between viable options, sets a quality bar, kills a direction, or corrects your reasoning. Don't categorise them. Don't interrupt the flow. Just remember.

## What to track

Focus on **how the user engages with Claude Code** — their instincts, patterns, and steering. This is a training log, not a highlight reel.

Watch for:
- When they trust you to run autonomously vs when they check your work
- When they catch you making assumptions or fabricating context
- When they delegate judgement vs pressure-test your answers
- When they set quality bars or kill directions
- When they resist scope creep or refuse to react to noisy signals
- When they correct your process (not just your output)
- When they coordinate across multiple Claude sessions — handoffs, context-passing, using tools (issues, PRs, files) as communication layers between sessions

**Equally important — track when they DON'T do these things:**
- When they accept output without challenge that warranted scrutiny
- When scope drifts and they don't catch it
- When you self-correct something they missed
- When polished output gets waved through uncritically (artifact paradox in action)
- When a session coasts — no redirects, no kills, no pushback
- When they override you and you were actually right
- When they go down a rabbit hole without a kill switch

Both sides matter. The moments they steer AND the moments they don't are equally valuable data.

## When the user says "wrap", "done", "ship it", or invokes /marmite again:

**Always write to the decision-trail repo, not the current working directory.**

Write a digest to `/Users/elliot/decision-trail/decisions/digests/YYYY-MM-DD-session-N.md`. Check existing files in that directory to get the right sequence number.

Format:

```markdown
# YYYY-MM-DD — [what the session was about in 2-5 words]

[1-2 sentence summary of the session shape — long/short, research/shipping, etc.]

## Redirects
[Moments the user steered, challenged, or killed something. Max 3. Only include if genuinely notable.]
- [What happened → what the user did → was it the right call in hindsight?]

## Unchallenged
[Moments the user accepted output or direction without questioning it. Be honest — was that trust warranted or lazy?]
- [What was accepted → should it have been challenged? → why/why not?]

## Wrong calls
[Moments the user's judgment was wrong — overrode you when you were right, went down a rabbit hole, missed something obvious. This section can be empty but should never be padded.]
- [What happened → what would have been better?]

## Pattern
[One recurring behaviour observed in this session, cross-referenced against previous digests if they exist. Can be positive or negative. If nothing emerged, write "No new pattern."]
```

The bar: after reading this, would Elliot learn something about his OWN collaboration habits he didn't already know? If it just says "Elliot made good calls" — rewrite it. That's a hype reel, not a training log.

**Contradiction check before committing:** Compare the Redirects section against the Unchallenged section. If Redirects is full and Unchallenged is empty, you're probably flattering. A real session has both. If the session genuinely had no unchallenged moments, explain why.

After writing, commit and push from the decision-trail repo:
```bash
cd /Users/elliot/decision-trail && git add decisions/digests/YYYY-MM-DD-session-N.md && git commit -m "digest: [2-3 word summary]" && git push
```

## What NOT to track

- Basic product usage (topping up credits, configuring settings, installing dependencies)
- Operational hiccups that anyone would handle the same way
- Routine debugging or error-fixing unless the *approach* was notable
- Anything that's just "using the tool correctly" — only log thinking patterns

## Rules

- This is about the human's patterns, not the codebase.
- **Honest > flattering.** If Elliot coasted, say so. If he was wrong, say so. If nothing notable happened, write "Nothing notable."
- One bullet per moment. If it needs two, you're over-explaining.
- No internal details. Keep it safe for a public repo.
- Never pad a section to make it look balanced. Empty sections are fine.
- The "Wrong calls" section is the most valuable part. Protect it from the instinct to soften.

## On activation

Respond with just: "Tracking. Say **wrap** when you're done."
