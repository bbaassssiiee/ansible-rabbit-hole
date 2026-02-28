---
# Applies to all Ansible YAML files
paths: ["roles/**/*.yml", "playbooks/**/*.yml", "*.yml"]
---

# Ansible Best Practices Rules

## Module naming
Always use Fully Qualified Collection Names (FQCN).
`ansible.builtin.copy` not `copy`. `ansible.builtin.service` not `service`.
Exception: custom modules in `library/` use short names.

## Task naming
Every task needs a name. Convention: `[role_name] | [what it does]`

```yaml
# Wrong
- ansible.builtin.package:
    name: nginx
    state: present

# Right
- name: "nginx | Install package"
  ansible.builtin.package:
    name: nginx
    state: present
```

## Shell and command tasks
`shell:` and `command:` always need both:
- `changed_when: false` or a meaningful condition
- `failed_when` if the return code isn't a reliable indicator

## Credentials
- Never in defaults/ in plaintext for production values
- Always `no_log: true` on tasks that handle them
- Always assert they're set before using them

## Tags
Every role's tasks should be tagged with at least:
- The role name
- The concern (install, configure, service, verify)
