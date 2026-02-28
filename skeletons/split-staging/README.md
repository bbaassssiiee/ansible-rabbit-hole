# Split Inventory Repositories

## The problem this solves

When staging and production share the same inventory repository, a bad commit
can affect production before anyone notices. You can't give a junior engineer
write access to staging without giving them write access to production.
And "I accidentally ran the playbook against production" becomes possible.

## The structure

```
infrastructure-staging/      ← separate git repo, separate access control
├── inventory/
│   ├── group_vars/
│   │   ├── all/
│   │   │   ├── vars.yml
│   │   │   └── vault.yml   ← encrypted with STAGING vault password
│   │   └── webservers/
│   │       └── vars.yml
│   ├── host_vars/
│   │   └── staging-web-01.yml
│   └── hosts.yml
└── README.md

infrastructure-production/   ← separate git repo, restricted access
├── inventory/
│   ├── group_vars/
│   │   ├── all/
│   │   │   ├── vars.yml
│   │   │   └── vault.yml   ← encrypted with PRODUCTION vault password (different key)
│   │   └── webservers/
│   │       └── vars.yml
│   ├── host_vars/
│   │   └── prod-web-01.yml
│   └── hosts.yml
└── README.md

infrastructure-playbooks/    ← shared playbooks repo (no secrets)
├── site.yml
├── webservers.yml
└── roles/                   ← or use requirements.yml + collections
```

## How to run

```bash
# Staging
ansible-playbook -i ../infrastructure-staging/inventory/ site.yml

# Production — requires production vault password
ansible-playbook -i ../infrastructure-production/inventory/ site.yml \
  --vault-password-file ~/.vault-production
```

## Access control model

| Repo | Who can write | Who can read |
|------|---------------|--------------|
| infrastructure-staging | all engineers | all engineers |
| infrastructure-production | senior engineers only | all engineers |
| infrastructure-playbooks | all engineers | all engineers |

## The vault key split

Staging and production use DIFFERENT vault passwords.
A junior engineer with the staging vault key cannot decrypt production secrets.
This is not paranoia — this is defence in depth.

Store vault passwords in separate locations:
- Staging: password manager, shared with the team
- Production: password manager, restricted to senior engineers + break-glass procedure

## 🐇 Rabbit holes from here

- `/explore vault-id` — named vault passwords, multiple vaults in one run
- `/explore dynamic-inventory` — replace hosts.yml with real dynamic sources
- `/explore constructed-inventory` — build groups from facts dynamically
