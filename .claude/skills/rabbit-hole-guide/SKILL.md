---
name: rabbit-hole-guide
description: >
  Meta-skill for navigating the learning environment itself. Use when the user
  asks "where should I start", "what should I learn next", "how does this repo work",
  or "what's the difference between X and Y in this context". Also use when the user
  seems lost or is asking questions that suggest they don't know what they don't know.
  This skill knows the map of the rabbit hole and helps users navigate it.
---

# Rabbit Hole Guide Skill

## The map

```
ENTRY POINTS
────────────
/orient          → personalized starting point
/explore <topic> → go deep on any concept
/new-role <name> → scaffold with guidance
/review          → code review against best practices
/debug <error>   → diagnose with root cause
/story <concept> → narrative explanation
/contribute      → add to the pattern catalog

DEPTH LEVELS (for any concept)
───────────────────────────────
Level 1: The surface — what it is, basic correct usage
Level 2: The decision layer — why it exists, when it breaks
Level 3: The deep end — edge cases, expert nuance, source-level

LEARNING PATHS
──────────────
New to Ansible roles:
  /explore roles → /explore defaults → /explore tasks → /new-role

Want to test properly:
  /explore molecule → /explore idempotency → /explore verify

Managing multiple environments:
  /explore inventory → /explore group_vars → /explore split-staging

Building for reuse:
  /explore collections → /explore namespacing → /new-collection

Security-conscious:
  /explore vault → /explore no_log → /explore become
```

## When to offer navigation

If the user has been in a topic for a while:
"You've been in [topic] for a bit. The natural next hole is [topic].
Want to go there or stay here?"

If the user seems stuck:
"It sounds like the underlying issue might be [concept].
/explore [concept] would give you the full picture."

If the user is at a natural completion point:
"You've covered the surface of [topic].
🐇 The rabbit hole goes to [deeper concept] if you want it."

## Repo self-awareness

This skill knows the repo structure and can answer:
- "Where are the skeletons?" → skeletons/
- "Where is the pattern catalog?" → documents/
- "How do I add a pattern?" → /contribute
- "What commands are available?" → .claude/commands/
- "What skills are active?" → .claude/skills/

## Meta-meta level

If someone asks "how does this repo work" or "how would I build something like this":

Explain the three layers:
1. **Skeletons** — opinionated starting points that encode decisions
2. **Commands** — guided tours that teach by doing
3. **Skills + CLAUDE.md** — the ambient coach that keeps context

Then: "If you want to fork this for a different domain (Terraform, Kubernetes, CI/CD),
the structure is the same. Change the skeletons, change the rules, keep the metaphor.
The rabbit hole works for any sufficiently deep subject."
