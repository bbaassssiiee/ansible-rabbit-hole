# /explore — Go down the rabbit hole on any Ansible concept

Concept to explore: $ARGUMENTS

This command has three depth levels. Always start at level 1 and ask before going deeper.

---

## Level 1 — The Surface (always show this first)

Explain the concept in 3-4 sentences. Assume the user has seen it but hasn't thought hard about it.
Show the simplest correct example. Then show the most common wrong version next to it.

Format:
```
THE CONCEPT
───────────
[plain explanation, no jargon without definition]

✓ RIGHT                          ✗ WRONG (and why)
[correct example]                [incorrect example]
                                 ^ [one-line reason]
```

End with: "🐇 Go deeper? I can show you [specific next level topic]. Just say yes or /explore [next topic]"

---

## Level 2 — The Decision Layer (only if user asks to go deeper)

This is where you explain WHY the pattern exists. What problem does it solve?
What breaks if you ignore it? Reference the pattern catalog:

- If a documented pattern exists: "This is the **[Pattern Name]** pattern → @documents/patterns/[file].md"
- If an anti-pattern exists: "Ignoring this leads to the **[Anti-pattern Name]** → @documents/anti-patterns/[file].md"

Show a real-world scenario where it matters. Not "imagine you have a webserver" but
a concrete situation with named variables, specific errors, and actual consequences.

End with: "🐇 There's a deeper layer here around [specific technical detail]. Want to see it?"

---

## Level 3 — The Deep End (only if user explicitly wants it)

This is where most people stop. You're going to show:

1. The edge cases and failure modes
2. The expert-level nuance (e.g. for variables: precedence order, magic variables, facts caching)
3. The performance implications if relevant
4. What the Ansible source code / docs actually say vs. what practitioners do

Reference the skeleton that demonstrates this in practice:
"See this in action: @skeletons/[relevant-skeleton]/"

End with: "You've reached the bottom of this particular hole.
Related holes worth exploring: /explore [topic1], /explore [topic2]"

---

## Topic map (use this to know what's connected)

- variables → variable-precedence → facts → magic-variables → hostvars
- roles → defaults → meta-dependencies → role-includes → collections
- molecule → idempotency → verify → testinfra → delegation
- inventory → group_vars → host_vars → dynamic-inventory → constructed
- tasks → handlers → blocks → rescue → always
- templates → jinja2-filters → lookups → plugins → custom-modules
- collections → namespacing → dependencies → galaxy → private-automation-hub

## Concept-to-skeleton mapping

If the concept has a skeleton, point to it:
- roles, defaults, handlers, tasks, templates, vars → @skeletons/role-skeleton/
- collections, plugins, modules → @skeletons/collection-skeleton/
- project layout, inventory structure → @skeletons/project-skeleton/
- staging vs production separation → @skeletons/split-staging/
