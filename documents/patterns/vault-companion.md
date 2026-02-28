---
name: Vault Companion
type: pattern
tags: [vault, variables, security, group_vars]
related_anti_patterns: [Vault Bypass, Opaque Vault]
---

# Vault Companion

## Problem

You need to encrypt secrets in group_vars but you still want `grep` to work.
If everything sensitive is inside an encrypted vault file, you can't see
variable names without decrypting. In a codebase with 50+ variables, this
creates operational friction — especially at 2am.

## Wrong way

```yaml
# group_vars/production/vault.yml (encrypted)
db_password: "supersecret"
api_key: "abc123"
smtp_password: "hunter2"
```

When someone new joins the team: "Where is `db_password` defined?"
Answer: "Decrypt the vault and grep." Not great.

## Right way

```yaml
# group_vars/production/vars.yml (plaintext — safe to grep)
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
smtp_password: "{{ vault_smtp_password }}"

# group_vars/production/vault.yml (encrypted with ansible-vault)
vault_db_password: "supersecret"
vault_api_key: "abc123"
vault_smtp_password: "hunter2"
```

Convention: vault variables are prefixed with `vault_`.
Plaintext variables are the public API. Vault variables are the implementation.

## Why this works

```bash
grep -r "db_password" group_vars/    # Works without decrypting
grep -r "vault_" group_vars/         # Shows you what's encrypted
ansible-vault view group_vars/production/vault.yml  # Only when you need values
```

The variable names are discoverable. The values are protected.

## When to use

Every environment that uses `ansible-vault`. Always.

## When NOT to use

Purely development environments with no real secrets (test values only).
Even then — it's a good habit. The pattern costs nothing.

## In the wild

A new engineer needs to add a variable. They open `group_vars/production/vars.yml`,
see the pattern, and know exactly what to do — add the plaintext reference,
add the vault_ prefixed secret to the vault. No documentation needed.

## Related

- 🐇 `/explore vault` — multi-password vaults, vault-id, per-environment keys
- ⚠️ Anti-pattern: Vault Bypass → `documents/anti-patterns/vault-bypass.md`
- ⚠️ Anti-pattern: Opaque Vault → `documents/anti-patterns/opaque-vault.md`
- 📁 See skeleton: `skeletons/project-skeleton/inventory/group_vars/`
