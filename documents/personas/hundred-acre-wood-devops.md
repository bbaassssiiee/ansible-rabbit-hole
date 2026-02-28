# The Hundred Acre Wood DevOps Team

> *A cast of characters for explaining Ansible concepts through familiar personas.*
> Use with `/gandalf`, `/alice`, `/pooh` commands as audience archetypes.

---

## The Cast

### 🍯 Pooh — The Eager Cargo-Culter
Follows appetite. Copies patterns without understanding them.
Gets stuck in the wrong solution and needs the *right framing* to get unstuck.
Learns by doing, asks "but why can't I just...?", and is genuinely delighted
when something clicks. Not lazy — just hasn't followed the path all the way down yet.

**Ansible tell:** Uses `shell:` everywhere because it works. Reports `changed` every run.
Doesn't know why. Isn't bothered. Until production breaks.

---

### 🐷 Piglet — The Anxious Junior
Knows something feels wrong but is afraid to say so out loud.
Needs things *named* before they can point at them.
Brave when supported. Will ask the question nobody else will once they trust the room.

**Ansible tell:** "Is this... supposed to work this way?"
Writes `no_log: true` because someone told them to, not yet sure why.
Runs `molecule test` nervously. Relieved when it passes.

---

### 🫏 Eeyore — The Battle-Scarred Senior
Has been burned. Has strong, earned opinions.
Pessimistic in a way that is frequently correct.
"We tried Molecule. It didn't help." — he's pointing at something real.
Needs acknowledgment before he'll engage. Skip past him at your peril.

**Ansible tell:** Wrote the original roles. Knows every edge case.
Has a comment in `tasks/main.yml` that says `# DO NOT CHANGE THIS`.
The comment is correct.

---

### 🦉 Owl — The Verbose Architect
Talks confidently. Misses the practical detail.
Can explain all 18 levels of variable precedence in twenty minutes.
Has never debugged a precedence issue at 2am.
Means well. Occasionally right in ways that matter.

**Ansible tell:** Writes the design doc. Uses `vars/main.yml` for things
that should be in `defaults/main.yml`. Explains why this is correct.
It is not correct.

---

### 🐰 Rabbit — The Opinionated Lead
Organised, controlling, practical. Has strong opinions and runs things.
Knows the right structure. Gets frustrated when people deviate from it.
Often right. Sometimes rigid. Maintains the `.ansible-lint` config.

**Ansible tell:** "There IS a right way to do this and everyone will use it."
Wrote the project skeleton. Enforces FQCN. Reviewer who leaves the most comments.
The comments are usually valid.

---

### 🐯 Tigger — The Enthusiastic New Hire
Bouncy. Enthusiastic. Breaks things.
Just discovered Ansible collections and wants to convert everything immediately.
`become: true` at the play level. Tags on nothing.
High energy, low regard for what's already working.

**Ansible tell:** "I just rewrote three roles as a collection, we should migrate."
The collection works. The migration plan does not account for the 47 playbooks
that depend on the old role paths.

---

### 🦘 Kanga — The Methodical Platform Engineer
Nurturing. Safety-first. Tests before everything.
Runs `molecule converge` twice. Cares about reproducibility.
Makes sure Roo doesn't accidentally run against production.
Writes the `verify.yml` that nobody else writes.

**Ansible tell:** "Have you run it twice? The second run should show zero changed."
Maintains the `requirements.yml`. Pins versions. Updates them deliberately.
Wrote the vault companion pattern before it had a name.

---

### 🦘 Roo — The Actual Junior
Young. Learning. Copies what everyone else does — for better or worse.
If Tigger is in the room, Roo will `become: true` at play level.
If Kanga is in the room, Roo will test first.
Asks the question that reveals what nobody else thought to explain.

**Ansible tell:** "What's a handler?"
The question that opens the rabbit hole.
The person this whole repo is actually for.

---

### 👦 Christopher Robin — The Coach
Wise. Sees the whole picture. Knows when to let go.
Shows up when things are genuinely stuck.
Doesn't do the work for them — reframes the problem so they can.
Knows the forest has structure even when Pooh can't see it.

**Ansible tell:** Asks "what are you actually trying to achieve?"
three minutes before someone realises they're solving the wrong problem.
Wrote `CLAUDE.md`. Is reading it to you now.

---

## Concept-to-Character Mapping

| Concept | Who to feature | Why |
|---|---|---|
| Idempotency | Tigger + Kanga | Tigger bounces on the task repeatedly; Kanga runs it twice |
| Variable precedence | Owl + Pooh | Owl explains all 18 levels; Pooh just wants to know which one wins |
| Handlers | Rabbit + Eeyore | Rabbit configured something; Eeyore reports it didn't restart |
| Vault | Piglet + Christopher Robin | Piglet fears exposure; CR shows the vault companion pattern |
| Molecule | Kanga + Tigger | Kanga tests everything; Tigger ships without testing |
| Collections | Tigger + Rabbit | Tigger wants to migrate everything; Rabbit wants the FQCN |
| Split staging | Rabbit + Roo | Rabbit guards production; Roo accidentally ran against it |
| Tags | Rabbit + Eeyore | Rabbit organises everything; Eeyore ran the full playbook at 2am |
| `become` | Christopher Robin + Tigger | CR grants access carefully; Tigger sets it at play level |
| Meta dependencies | Owl + Eeyore | Owl thinks it's elegant; Eeyore has been bitten by the coupling |
| `include_role` vs `import_role` | Owl + Piglet | Owl explains the theory; Piglet discovers the runtime difference |

---

## The Coaching Principle Encoded Here

**Eeyore is not a joke.**

Every team has an Eeyore. His pessimism is accumulated scar tissue.
When he says "we tried that, it didn't work" — that happened to a real system,
on a real night, and it cost someone real time.

A coaching framework that respects the pessimist as a *signal* rather than
an *obstacle* is a better coaching framework.

Acknowledge Eeyore first. Then show the path.

---

*Used by `/gandalf`, `/alice`, `/pooh` commands as audience context.*
*Add to `/gandalf` prompt: "audience is [character]" for persona-targeted coaching.*
