You are now tracking this session for decision-trail.

Silently note moments where the user redirects you, reframes a problem, makes a judgment call between viable options, sets a quality bar, or kills a direction. Don't categorise them. Don't interrupt the flow. Just remember.

## When the user says "wrap", "done", "ship it", or invokes /marmite again:

Write a digest to `decisions/digests/YYYY-MM-DD-session-N.md`. Check existing files in that directory to get the right sequence number.

Format:

```markdown
# YYYY-MM-DD — [what the session was about in 2-5 words]

[1-2 sentence summary of what was attempted and the outcome.]

- [tight narrative bullets. what happened, what was decided, why.]
- [capture trade-offs, killed directions, and quality bars.]
- [quote the user sparingly — only when their exact words carry meaning a paraphrase would lose.]
- [no architecture details, env vars, column names, or implementation specifics.]
- [if nothing notable happened, just write "Nothing notable."]
```

Think teammate's standup note, not forensic log. Someone should be able to skim it in 15 seconds and know what mattered. Focus on the *why* behind decisions — code review already captures the *what*.

After writing, commit:
```bash
git add decisions/digests/YYYY-MM-DD-session-N.md
git commit -m "digest: [2-3 word summary]"
```

## Rules

- Narrative over bullet-quotes. Tell the story tight.
- One bullet per decision or moment. If it needs two, you're over-explaining.
- No internal details (API keys, model names, table columns, file paths). Keep it safe for a public repo.
- If nothing notable happened, write "Nothing notable." and commit that. Honest > padded.
- Never editorialize. Never score. Never count.

## On activation

Respond with just: "Tracking. Say **wrap** when you're done."
