# 🐇 Ansible Rabbit Hole

> *"The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down."*
> — Lewis Carroll

A Claude Code-powered learning environment for Ansible practitioners who want to go deep.
Not a tutorial. Not a reference. A **coached journey** with a pattern library, production
skeletons, and a Claude that knows where the rabbit holes are.

Brought to you by Bas Meijer @bbaassssiiee, Author of Ansible Up & Running 3E, O'Reilly
[https://www.ansiblebook.com](https://www.ansiblebook.com)

## Who this is for

You already know what a playbook is. You've written roles. You've broken production at least once.
Now you want to understand *why* the patterns exist, where they break down, and how to build
Ansible codebases that your future self will thank you for.

## Quick start

```bash
# Clone as your new project scaffold
git clone https://github.com/yourname/ansible-rabbit-hole myproject
cd myproject

# Open in Claude Code
claude .

# Ask Claude where to start
/orient
```

## What's inside

```
.
├── CLAUDE.md                    ← Coach instructions (Claude reads this always)
├── .claude/
│   ├── commands/                ← /orient, /explore, /new-role, /review, /debug, /story,
│   ├── skills/                  ← ansible-coach, storyteller, rabbit-hole-guide
│   ├── rules/                   ← always-on best practice rules
│   └── agents/                  ← specialized subagents (linter, tester, reviewer)
├── documents/
│   ├── patterns/                ← what works and why
│   ├── anti-patterns/           ← what breaks and how
│   └── obstacles/               ← inherent limitations to know about
├── skeletons/
│   ├── role-skeleton/           ← production-ready role template with Molecule
│   ├── collection-skeleton/     ← full collection structure
│   ├── project-skeleton/        ← a real project layout with split inventory
│   └── split-staging/           ← separate inventory repos for prod/staging
└── examples/
    ├── well-organized-project/  ← annotated real-world project structure
    └── monorepo-vs-split/       ← the decision explained with both options
```

## The rabbit hole metaphor

Each topic has a surface and a depth. The commands guide you:

- `/explore variables` — starts at "what are variables" and goes as deep as you want
- Every explanation ends with "🐇 go deeper?" so you control the descent
- The pattern catalog maps what you discover to named, reusable concepts


##  Hear it in another voice.

- /pooh  — Explain it simply, from appetite to understanding
- /alice — Follow the concept down the rabbit hole
- /gandalf — The deep path; what lies beneath


All three accept $ARGUMENTS or infer from context.

## Contributing

Found a pattern? Burned by an anti-pattern? Hit an obstacle that nobody warned you about?

```
/contribute
```

The `/contribute` command walks you through adding it to the catalog in the right format.

## Meta-meta level

This repo is itself an example of an augmented coding pattern: **coached scaffolding**.
The CLAUDE.md encodes the coach persona. The commands encode the curriculum.
The skeletons encode the opinions. The pattern catalog is the living memory.

If you fork this for your own domain (Terraform? Kubernetes? CI/CD?), the structure
works the same way. Change the skeletons, change the rules, keep the metaphor.
