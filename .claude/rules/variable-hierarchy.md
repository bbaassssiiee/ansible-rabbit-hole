---
# Always active — applies everywhere
---

# Variable Hierarchy Rules

## Where variables live (and why)

```
defaults/main.yml        ← role defaults, lowest precedence, always declare here
vars/main.yml            ← role constants, not meant to be overridden
inventory/group_vars/all/     ← applies to every host
inventory/group_vars/<env>/   ← environment-specific (production, staging)
inventory/host_vars/<host>/   ← host-specific overrides
playbook vars:           ← highest precedence, use sparingly
```

## Rules Claude enforces

1. Every variable a role uses must be declared in `defaults/main.yml` with a comment
2. `vars/main.yml` is for constants — if it should be overridable, it belongs in defaults
3. `group_vars/all/` files should be split by concern (not one giant all.yml)
   - `group_vars/all/packages.yml`
   - `group_vars/all/users.yml`
   - `group_vars/all/network.yml`
4. Vault-encrypted variables live in `group_vars/<env>/vault.yml`
   - Plaintext companion: `group_vars/<env>/vars.yml` with `var: "{{ vault_var }}"`
   - This pattern allows grep without decrypting vault

## The vault companion pattern

```
group_vars/production/
├── vars.yml          ← db_password: "{{ vault_db_password }}"
└── vault.yml         ← vault_db_password: "actual secret" (encrypted)
```

Why: `grep db_password` works. Only the vault_ prefixed var is encrypted.

🐇 /explore variable-precedence for the full 18-level chart
