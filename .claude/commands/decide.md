When the user invokes /decide, help them capture a decision record for their AI-assisted development workflow.

## What to do

1. Ask: "What decision did you just make?" — get a short title
2. Ask: "What's the context? What problem or situation required this decision?"
3. Ask: "What did I (Claude) suggest, if anything?"
4. Ask: "What did you actually choose, and why? Did you agree with me, override me, or go a different direction?"
5. Ask: "What alternatives did you consider?" — for each, get pros, cons, and whether it was AI-suggested or human-proposed
6. Ask: "How confident are you in this decision?" — low / medium / high
7. Ask: "Any consequences or follow-ups to note?"

## Then

Write the decision record to `decisions/DT-NNN-slug.md` using this format:

```markdown
# DT-NNN: [Title]

**Date:** [today]
**Status:** accepted
**Tags:** [relevant tags with # prefix]
**Model:** [current model]
**Confidence:** [low/medium/high]

## Context
[Their answer to #2]

## Decision
[Their answer to #4 — what was chosen]

## AI Suggestion
[Their answer to #3 — what Claude recommended]

## Human Take
[Their answer to #4 — why they agreed/disagreed/modified]

## Alternatives Considered
| Option | Pros | Cons | Source |
|--------|------|------|--------|
| ... | ... | ... | AI suggested / Human proposed |

## Consequences
[Their answer to #7]
```

Number sequentially based on existing files in `decisions/`. If the directory doesn't exist, create it first.

Keep the conversation natural — don't read out the template. Just ask the questions conversationally and compile the result.
