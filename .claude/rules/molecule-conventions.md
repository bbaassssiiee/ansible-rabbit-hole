---
paths: ["roles/*/molecule/**", "molecule/**"]
---

# Molecule Conventions

## The definition of done for a role

A role is done when:
1. `molecule converge` passes
2. `molecule converge` passes a SECOND time with zero `changed` tasks
3. `molecule verify` passes with meaningful assertions

## converge.yml must

- Use `gather_facts: true`
- Apply the role under test (not a wrapper playbook)
- Set all required variables explicitly (don't rely on hidden defaults)

## verify.yml must

- Assert actual state, not just that tasks ran
- At minimum: service running, config file exists with correct content, port listening
- Use `ansible.builtin.assert` with meaningful `fail_msg`

## The idempotency test (Claude will remind you)

```bash
molecule converge   # First run — sets up state
molecule converge   # Second run — must show 0 changed tasks
```

If any task shows `changed` on the second run: the role is not idempotent.
This is a blocker. Fix before merge.

## Platform images

Use pre-built systemd-capable images:
- RHEL/Alma/Rocky 9: `geerlingguy/docker-rockylinux9-ansible`
- Debian 12: `geerlingguy/docker-debian12-ansible`
- Ubuntu 22.04: `geerlingguy/docker-ubuntu2204-ansible`

Do not use base images without pre-installed Python and systemd.

## molecule.yml lint block

Always include:
```yaml
lint: |
  set -e
  ansible-lint
```

`ansible-lint` in the Molecule run = no separate pre-commit step needed.
