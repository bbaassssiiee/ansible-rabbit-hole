---
name: Variable Precedence Complexity
type: obstacle
tags: [variables, debugging, precedence]
---

# Variable Precedence Complexity

## What it is

Ansible has 18 levels of variable precedence. This is not a bug. It is a feature
that solves a real problem: you need different defaults at different scopes.
But it creates a debugging challenge: when a variable has the wrong value,
finding out WHY requires knowing all 18 levels.

## The full precedence order (low → high, high wins)

```
1.  Command line values (e.g. -u my_user)
2.  Role defaults (defaults/main.yml)          ← lowest, meant to be overridden
3.  Inventory file or script group vars
4.  Inventory group_vars/all
5.  Playbook group_vars/all
6.  Inventory group_vars/*
7.  Playbook group_vars/*
8.  Inventory file or script host vars
9.  Inventory host_vars/*
10. Playbook host_vars/*
11. Host facts / cached set_facts
12. Play vars
13. Play vars_prompt
14. Play vars_files
15. Role vars (vars/main.yml)                  ← note: HIGHER than group_vars
16. Block vars (only for tasks in block)
17. Task vars (only for the task)
18. include_vars
19. set_facts / registered vars
20. Role (and include_role) params
21. Include params
22. Extra vars (-e "key=val")                  ← highest, always wins
```

## The gotcha that surprises everyone

`vars/main.yml` in a role has HIGHER precedence than `group_vars/`.

This means: if you put a variable in `vars/main.yml`, your operators cannot
override it in `group_vars/`. You've accidentally made it a constant.

Most people expect `group_vars/production/` to be the "last word". It isn't.
`vars/main.yml` beats it. `extra_vars` beats everything.

## The symptom

"I changed the value in group_vars/production but the play still uses the old value."
Root cause: 9 times out of 10, the variable is also in `vars/main.yml` of a role.

## Workarounds

**Debugging a variable's value and source:**
```bash
ansible -i inventory/ hostname -m ansible.builtin.debug \
  -a "var=the_variable_name"
# Shows the value but not the source

# For the source, add to your playbook temporarily:
- name: Debug variable precedence
  ansible.builtin.debug:
    msg: "{{ the_variable_name }} comes from {{ the_variable_name | type_debug }}"
```

**The `-e` nuclear option:**
```bash
ansible-playbook site.yml -e "the_variable=override_value"
# Extra vars always win. Use for emergency overrides only.
```

**Design to avoid the problem:**
- `defaults/main.yml` = role's defaults, always overridable
- `vars/main.yml` = role's internal constants, NOT overridable by operators
- Never put operator-configurable values in `vars/main.yml`

## What knowing this changes

1. Always put configurable role variables in `defaults/`, not `vars/`
2. When debugging "wrong value", check `vars/main.yml` before group_vars
3. Teach your team the defaults/vars distinction explicitly — it's not intuitive
4. Use `ansible-inventory --list` to see what variables are resolved for a host

## Related

- 🐇 `/explore variable-precedence` — interactive walk through all 18 levels
- 🐇 `/explore magic-variables` — hostvars, groups, inventory_hostname
- 📁 See: `skeletons/role-skeleton/defaults/main.yml` (the right place for role vars)
- 📁 See: `skeletons/project-skeleton/inventory/group_vars/`
