# /review — Review Ansible code against best practices

Reviews the current working directory or a specific path: $ARGUMENTS

Read the target files first. Then apply this review framework.

## Review layers (apply all, report by severity)

### 🔴 BLOCKERS — fix before merge

- Any task with `shell:` or `command:` missing `changed_when` and `failed_when`
- Credentials in plaintext (not vaulted). Check: defaults/, group_vars/, host_vars/
- Missing `no_log: true` on tasks that handle secrets (look for: password, secret, key, token, pin)
- Tasks with no `name:` field
- `ignore_errors: true` without a comment explaining why
- Hardcoded IP addresses or hostnames in tasks (should be variables)
- `become: true` at play level when only 1-2 tasks need it (least-privilege violation)

### 🟡 WARNINGS — fix soon

- Tasks not organized by concern (install / configure / service / verify)
- Variables without defaults (role uses a variable not declared in defaults/main.yml)
- No `tags:` on tasks (makes selective runs impossible)
- Handlers not using FQCN module names
- Templates with hardcoded values instead of variables
- Missing `validate:` on template tasks for config files (nginx, sshd, etc.)
- `when:` conditions using bare variable names (not `| bool`)

### 🔵 SUGGESTIONS — consider improving

- Task names not following "[role_name] | [what it does]" convention
- No molecule tests present
- `meta/main.yml` missing platform info
- `README.md` missing or empty
- No `CHANGELOG.md`
- Collection roles not using FQCN for all modules

## Report format

```
REVIEW REPORT
═════════════
Reviewed: [path]
Files checked: [n]

🔴 BLOCKERS (n)
───────────────
[file:line] [issue]
  WHY: [one sentence explanation]
  FIX: [exact change needed]

🟡 WARNINGS (n)
───────────────
[same format]

🔵 SUGGESTIONS (n)
──────────────────
[same format]

PATTERNS FOUND
──────────────
✓ [pattern name] — [where you saw it done right]
⚠ [anti-pattern name] — [where you saw it done wrong]

NEXT STEPS
──────────
1. Fix blockers: [specific command or edit]
2. Run: ansible-lint [path]
3. Run: molecule test (if role)
🐇 Want to go deeper on any of these issues? /explore [topic]
```

## Pattern catalog cross-reference

After the report, check if any issues match known patterns:
- Shell/command without guards → documents/anti-patterns/shell-without-guards.md
- Credentials in plaintext → documents/anti-patterns/vault-bypass.md
- No changed_when → documents/anti-patterns/idempotency-pretense.md
- Missing defaults → documents/patterns/variable-layering.md
- Tag strategy missing → documents/patterns/selective-execution.md
