# A Well-Organized Ansible Project

This is an annotated real-world project structure. Every directory and file
has a comment explaining WHY it exists and what the decision was.

Read this alongside: `/story project-structure`

```
myproject/
│
├── ansible.cfg                  ← Project-scoped config. Always have this.
├── requirements.yml             ← External role/collection dependencies. Pin versions.
├── site.yml                     ← The entry point. Imports environment playbooks.
│
├── inventory/                   ← If splitting staging/prod, this becomes two repos.
│   ├── group_vars/
│   │   ├── all/
│   │   │   ├── vars.yml         ← Applies to every host. Keep minimal.
│   │   │   └── vault.yml        ← Encrypted. References via vault_* prefix.
│   │   ├── webservers/
│   │   │   ├── vars.yml         ← Group-specific vars. Split by concern if large.
│   │   │   └── vault.yml        ← Group-specific secrets (if needed).
│   │   └── databases/
│   │       └── vars.yml
│   ├── host_vars/
│   │   └── web-01.yml           ← Only exists if web-01 needs unique configuration.
│   │                               If all webservers are identical, this is empty.
│   ├── hosts.yml                ← Static inventory. Replace with plugin if dynamic.
│   └── production.yml           ← Alternative: separate host files per environment.
│
├── playbooks/                   ← Functional playbooks. site.yml imports these.
│   ├── webservers.yml
│   ├── databases.yml
│   └── bootstrap.yml            ← First-run playbook (before SSH keys, etc.)
│
├── roles/                       ← Project-specific roles (not reusable elsewhere).
│   │                               Reusable roles belong in a collection.
│   ├── common/                  ← Applied to all hosts. Baseline hardening, users, etc.
│   ├── nginx/
│   └── postgresql/
│
├── collections/                 ← Installed collections (from requirements.yml).
│   └── ansible_collections/     ← git-ignored. Rebuilt from requirements.yml.
│       └── community/
│           └── general/
│
├── filter_plugins/              ← Project-scoped filter plugins.
│   └── README.md                ← Explain what's here and why it's not in a collection.
│
├── library/                     ← Project-scoped custom modules (rare).
│   └── README.md                ← If you have modules here, consider a collection.
│
└── molecule/                    ← Project-level molecule scenarios (vs role-level).
    └── README.md                ← For testing playbook combinations, not single roles.
```

## The decisions behind this structure

### Why `site.yml` imports playbooks instead of having everything in one file

```yaml
# site.yml — thin entry point
- import_playbook: playbooks/webservers.yml
- import_playbook: playbooks/databases.yml
```

vs the anti-pattern:
```yaml
# site.yml — 800 lines of plays mixed together
- name: Configure webservers
  hosts: webservers
  ...
- name: Configure databases  
  hosts: databases
  ...
```

The import approach means:
- `ansible-playbook playbooks/webservers.yml` works standalone
- Playbooks are testable in isolation
- `site.yml` is the orchestration layer, not the implementation

### Why group_vars is split into vars.yml + vault.yml

See: documents/patterns/vault-companion.md

The short version: `grep db_password group_vars/` works without decrypting.
Variable names are always visible. Values are protected.

### Why project roles live in roles/ but reusable roles go in collections

A role in `roles/` is owned by this project. It can have project-specific
assumptions baked in. It doesn't need to work anywhere else.

A role you want to share across projects belongs in a collection.
It needs proper defaults, no hardcoded assumptions, FQCN module names,
and a galaxy.yml. The discipline of making it reusable improves the quality.

### Why requirements.yml pins versions

```yaml
# requirements.yml
collections:
  - name: community.general
    version: ">=8.0.0,<9.0.0"   ← pin the major version
  - name: community.postgresql
    version: "3.4.0"             ← pin exactly for stability
```

Unpinned: `community.general` gets a breaking change next month, your
pipeline breaks on a Friday afternoon. Pinned: you control when to upgrade.

## ansible.cfg for this structure

```ini
[defaults]
inventory          = inventory/
roles_path         = roles/
collections_paths  = collections/
vault_password_file = ~/.vault-myproject    ; or use --vault-password-file per run

[privilege_escalation]
become      = false                          ; default false, enable per-play
become_method = sudo

[ssh_connection]
pipelining  = true                           ; faster, requires requiretty off in sudoers
```

## 🐇 Where to go from here

- `/explore inventory` — static to dynamic, constructed groups
- `/explore requirements-yml` — version pinning strategy
- `/explore ansible-cfg` — every meaningful option explained
- `/explore split-staging` — when one inventory repo isn't enough
