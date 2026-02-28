---
name: Idempotency Pretense
type: anti-pattern
tags: [tasks, command, shell, idempotency, changed_when]
correct_pattern: Guarded Command
---

# Idempotency Pretense

## What it looks like

```yaml
# This looks fine. It is not fine.
- name: Initialize the database
  ansible.builtin.command: /usr/bin/myapp --init-db
```

Or worse:
```yaml
- name: Do the thing
  ansible.builtin.shell: |
    thing --setup
    thing --configure
    thing --start
```

## What breaks

Every time you run the playbook: **changed**. Every time.

The `command` and `shell` modules have no way to know if they changed anything.
They report `changed: true` by default because they don't know better.

This breaks two things:

1. **Handlers fire every run.** Your service restarts every time you run the playbook,
   even if nothing changed. On 40 servers. Every deploy.

2. **Idempotency is a lie.** You think you know the state of your infrastructure.
   You don't. Your "idempotent" playbook mutates the system every run.

The production incident: A deployment pipeline runs every 15 minutes.
The playbook has three `command:` tasks without `changed_when`.
Three handlers fire. The web service restarts three times every 15 minutes.
Monitoring shows intermittent 502s. Nobody connects it to the deploys for two days.

## Why people do it

`command:` and `shell:` are easy. They do the thing. The task name says what it does.
It's not obvious that "changed" means something specific in Ansible.

## The fix

**Option 1: Use the right module**

```yaml
# If there's a module for it, use the module.
# Modules know when they changed something.
- name: Initialize the database
  community.postgresql.postgresql_db:
    name: myapp
    state: present
```

**Option 2: Guard the command with creates:**

```yaml
# Run only if this file doesn't exist
- name: Initialize the database
  ansible.builtin.command: /usr/bin/myapp --init-db
  args:
    creates: /var/lib/myapp/.initialized
    # Ansible checks: if this file exists, skip the task and report 'ok'
```

**Option 3: Explicit changed_when**

```yaml
# Run always, but only report changed if the output says so
- name: Initialize the database  
  ansible.builtin.command: /usr/bin/myapp --init-db
  register: init_result
  changed_when: "'already initialized' not in init_result.stdout"
  failed_when: init_result.rc != 0 and 'already initialized' not in init_result.stdout
```

## Detection

Find this in existing roles:
```bash
# Tasks using command or shell without changed_when
grep -B5 -A10 "ansible.builtin.command\|ansible.builtin.shell" roles/*/tasks/*.yml \
  | grep -L "changed_when"

# ansible-lint catches this too:
ansible-lint --rules-dir rules/ roles/
# Rule: no-changed-when
```

## Related

- ✓ Pattern: Guarded Command (the `creates:` and `changed_when:` patterns)
- 🐇 `/explore idempotency` — what it means and how to prove it with Molecule
- 🐇 `/explore molecule` — run converge twice, the diff should be empty
