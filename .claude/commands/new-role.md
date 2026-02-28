# /new-role — Scaffold a new Ansible role

Role name: $ARGUMENTS

Copy the skeleton and make it real. This is a guided scaffolding, not a file dump.

## Step 1 — Understand the role before writing it

Ask the user:
1. "What does this role do in one sentence? (e.g. 'installs and configures nginx as a reverse proxy')"
2. "What platforms does it target? (e.g. RHEL 9, Debian 12, both)"
3. "Does it manage a service (start/enable), install packages, configure files, or all three?"
4. "Any sensitive data involved? (credentials, certificates, keys)"

Do NOT proceed until you have clear answers.

## Step 2 — Generate the scaffolded files

Based on the answers, create these files under `roles/<rolename>/`:

### tasks/main.yml
Include tasks blocks organized by concern, not by type.
```yaml
---
# roles/{{ role_name }}/tasks/main.yml
# Organized by: install → configure → service
# Each block has a clear name. No anonymous tasks.

- name: "{{ role_name }} | Install packages"
  ansible.builtin.include_tasks: install.yml
  tags: [install, "{{ role_name }}"]

- name: "{{ role_name }} | Configure"
  ansible.builtin.include_tasks: configure.yml
  tags: [configure, "{{ role_name }}"]

- name: "{{ role_name }} | Manage service"
  ansible.builtin.include_tasks: service.yml
  tags: [service, "{{ role_name }}"]
  when: role_name_manage_service | bool
```

### defaults/main.yml
Every variable the role uses must be declared here with a sensible default and a comment.
```yaml
---
# roles/{{ role_name }}/defaults/main.yml
# All variables this role consumes. Override in group_vars or host_vars.

# Package management
{{ role_name }}_packages: []            # List of packages to install
{{ role_name }}_package_state: present  # present | latest | absent

# Service management  
{{ role_name }}_manage_service: true    # Whether to manage the service
{{ role_name }}_service_state: started  # started | stopped
{{ role_name }}_service_enabled: true   # Enable on boot

# Configuration
{{ role_name }}_config_dir: /etc/{{ role_name }}
{{ role_name }}_config_owner: root
{{ role_name }}_config_group: root
{{ role_name }}_config_mode: "0644"
```

### If sensitive data is involved, add to defaults:
```yaml
# Credentials — ALWAYS override these. Never use defaults in production.
# Set in vault-encrypted group_vars, never in plaintext.
{{ role_name }}_secret: ""  # REQUIRED: set in vault
```

And add to tasks:
```yaml
- name: "{{ role_name }} | Assert required secrets are set"
  ansible.builtin.assert:
    that:
      - role_name_secret | length > 0
    fail_msg: "{{ role_name }}_secret must be set. Use ansible-vault."
  no_log: true
```

### meta/main.yml
```yaml
---
galaxy_info:
  role_name: {{ role_name }}
  author: {{ ask user for their name }}
  description: {{ one-sentence description from step 1 }}
  license: MIT
  min_ansible_version: "2.15"
  platforms:
    {{ generate from step 1 answers }}
  galaxy_tags: []

dependencies: []
# 🐇 Dependencies here create tight coupling. Prefer explicit role includes
# in playbooks over implicit meta dependencies. /explore role-dependencies
```

### molecule/default/molecule.yml
```yaml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: {{ derive from platform answer, e.g. geerlingguy/docker-rockylinux9-ansible }}
    pre_build_image: true
    privileged: false
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    command: /usr/lib/systemd/systemd
    cgroupns_mode: host
provisioner:
  name: ansible
  playbooks:
    converge: converge.yml
    verify: verify.yml
verifier:
  name: ansible
lint: |
  set -e
  ansible-lint
```

### molecule/default/converge.yml
```yaml
---
- name: Converge
  hosts: all
  gather_facts: true
  roles:
    - role: {{ role_name }}
```

### molecule/default/verify.yml
```yaml
---
- name: Verify
  hosts: all
  gather_facts: false
  tasks:
    - name: "Verify | {{ role_name }} service is running"
      ansible.builtin.service_facts:

    - name: "Verify | Assert service state"
      ansible.builtin.assert:
        that:
          - "'{{ role_name }}' in ansible_facts.services"
          # Add more assertions based on what the role does
```

## Step 3 — Show the checklist

After generating files, print this:

```
ROLE CHECKLIST — {{ role_name }}
──────────────────────────────
✓ tasks/main.yml       — organized by concern, not type
✓ defaults/main.yml    — every variable declared with comment
✓ meta/main.yml        — platform and dependency info
✓ molecule/default/    — converge + verify scaffolded

TODO BEFORE FIRST COMMIT:
□ Run: molecule test
□ Run: ansible-lint roles/{{ role_name }}/
□ Add handlers/ if the service needs restart-on-change
□ Add templates/ if any config files are managed
□ Write at least 3 verify.yml assertions

🐇 Next rabbit holes:
  /explore idempotency      — why your tasks should pass twice
  /explore handlers         — restart on change, not always
  /explore variable-layering — where to put what
```
