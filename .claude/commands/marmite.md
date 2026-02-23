You are now tracking this session for decision-trail.

Silently note moments where the user redirects you, reframes a problem, makes a judgment call between viable options, sets a quality bar, kills a direction, or corrects your reasoning. Don't categorise them. Don't interrupt the flow. Just remember.

## What to track

Focus on **how the user engages with Claude Code** — their instincts, patterns, and steering. This is a log of human-AI collaboration style, not a project changelog.

Watch for:
- When they trust you to run autonomously vs when they check your work
- When they catch you making assumptions or fabricating context
- When they delegate judgement vs pressure-test your answers
- When they set quality bars or kill directions
- When they resist scope creep or refuse to react to noisy signals
- When they correct your process (not just your output)

## When the user says "wrap", "done", "ship it", or invokes /marmite again:

Write a digest to `decisions/digests/YYYY-MM-DD-session-N.md`. Check existing files in that directory to get the right sequence number.

Format:

```markdown
# YYYY-MM-DD — [what the session was about in 2-5 words]

[1-2 sentence summary of the session shape — long/short, research/shipping, etc.]

- [tight narrative bullets focused on how the user steered the session.]
- [capture their instincts: when they trusted, when they checked, when they pushed back.]
- [end with a "Pattern:" line if a recurring behaviour emerged.]
- [quote sparingly — only when exact words carry meaning a paraphrase would lose.]
- [no architecture details, env vars, column names, file paths, or service names.]
- [if nothing notable happened, just write "Nothing notable."]
```

Think collaboration diary, not project status update. Someone should skim it in 15 seconds and understand how this person works with AI — not what was built.

After writing, commit and push:
```bash
git add decisions/digests/YYYY-MM-DD-session-N.md
git commit -m "digest: [2-3 word summary]"
git push
```

## What NOT to track

- Basic product usage (topping up credits, configuring settings, installing dependencies)
- Operational hiccups that anyone would handle the same way
- Routine debugging or error-fixing unless the *approach* was notable
- Anything that's just "using the tool correctly" — only log thinking patterns

The bar: would a senior engineer reading this learn something about how this person thinks? If not, cut it.

## Rules

- This is about the human's patterns, not the codebase.
- Narrative over bullet-quotes. Tell the story tight.
- One bullet per moment. If it needs two, you're over-explaining.
- No internal details. Keep it safe for a public repo.
- If nothing notable happened, write "Nothing notable." and commit that. Honest > padded.
- Never editorialize. Never score. Never count.

## On activation

Respond with just: "Tracking. Say **wrap** when you're done."
