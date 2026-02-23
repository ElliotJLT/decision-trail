You are now tracking this session for decision-trail.

Silently note moments where the user redirects you, reframes a problem, makes a judgment call between viable options, sets a quality bar, or kills a direction. Don't categorise them. Don't interrupt the flow. Just remember.

## When the user says "wrap", "done", "ship it", or invokes /marmite again:

Write a digest to `decisions/digests/YYYY-MM-DD-session-N.md`. Check existing files in that directory to get the right sequence number.

Format:

```markdown
# YYYY-MM-DD — [what the session was about in 2-5 words]

- [one line per moment. quote their words where possible. keep it tight.]
- [no categories, no headers, no explanations unless essential]
- [if something got killed, say what and why in one line]
- [if they reframed something, show the reframe, not the backstory]
```

That's it. A flat list. Skimmable in 10 seconds. No metadata block, no raw numbers, no "what happened" section.

After writing, commit:
```bash
git add decisions/digests/YYYY-MM-DD-session-N.md
git commit -m "digest: [2-3 word summary]"
```

## Rules

- Quote actual words. Their language is the data.
- One line per moment. If it needs two lines, you're over-explaining.
- If nothing notable happened, write "Nothing notable." and commit that. Honest > padded.
- Never editorialize. Never score. Never count.

## On activation

Respond with just: "Tracking. Say **wrap** when you're done."
