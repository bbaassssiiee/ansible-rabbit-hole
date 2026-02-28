# /contribute — Add to the pattern catalog

Add a pattern, anti-pattern, or obstacle you've discovered.

## Step 1 — Classify what you have

Ask:
"What are you contributing? (pattern = what works, anti-pattern = what breaks, obstacle = inherent limitation)"

## Step 2 — Interview for the pattern

For a **pattern**:
1. "What's the name? (e.g. 'Variable Layering', 'Handler Isolation')"
2. "What problem does it solve? One sentence."
3. "What does the wrong version look like? Show me the code."
4. "What does the right version look like? Show me the code."
5. "When would you NOT use this pattern? (edge cases / exceptions)"

For an **anti-pattern**:
1. "What's the name? (e.g. 'Idempotency Pretense', 'Vault Bypass')"
2. "What does it look like in the wild? Show me the code."
3. "What breaks? Be specific — what error, what symptom, what production incident."
4. "What's the correct pattern that replaces it?"

For an **obstacle**:
1. "What's the name? (e.g. 'Facts Caching Staleness', 'Serial Execution Bottleneck')"
2. "What is the inherent limitation — i.e. NOT a bug, not a mistake, just a constraint?"
3. "What are the known workarounds? (even partial ones)"
4. "What does knowing about this change in how you design?"

## Step 3 — Generate the document

Use this template and write the file to the right directory:

### Pattern template → documents/patterns/<name>.md
```markdown
---
name: [Pattern Name]
type: pattern
tags: [variables | roles | inventory | molecule | collections | tasks | ...]
related_anti_patterns: [anti-pattern names if any]
---

# [Pattern Name]

## Problem

[One paragraph: what situation does this pattern address?]

## Wrong way

```yaml
# This is what people do before they know the pattern
[code example]
```

Why this breaks: [specific consequence]

## Right way

```yaml
# This is the pattern
[code example]
```

Why this works: [specific reason]

## When to use

[Specific conditions where this pattern applies]

## When NOT to use

[Exceptions — don't pretend patterns are universal]

## In the wild

[A concrete scenario where you'd apply this]

## Related

- 🐇 `/explore [deeper concept]`
- ⚠️ Anti-pattern: [name] → `documents/anti-patterns/[file].md`
- 📁 See skeleton: `skeletons/[relevant-skeleton]/`
```

### Anti-pattern template → documents/anti-patterns/<name>.md
```markdown
---
name: [Anti-pattern Name]
type: anti-pattern
tags: [...]
correct_pattern: [pattern name that replaces this]
---

# [Anti-pattern Name]

## What it looks like

```yaml
# This is the anti-pattern in the wild
[code example]
```

## What breaks

[Specific failure: error message, symptom, or production incident description]

## Why people do it

[The reasoning that seems valid until it isn't — show empathy]

## The fix

```yaml
# The correct pattern
[code example]
```

## Detection

How to find this in existing code:
```bash
# ansible-lint rule or grep pattern
grep -r "pattern" roles/
```

## Related

- ✓ Pattern: [correct pattern name]
- 🐇 `/explore [concept]`
```

## Step 4 — Confirm and write

Show the generated document to the user, ask for confirmation, then write it to the correct path.

After writing, say:
"Added to the catalog. It's now part of the rabbit hole — /explore will reference it,
/review will check for it, and future contributors will build on it."
