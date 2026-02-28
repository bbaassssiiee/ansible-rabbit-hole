# Monorepo vs Split Repositories

The question comes up on every team that scales past 3 engineers.
There is no universal right answer. Here is the decision framework.

## Option A: Monorepo

```
infrastructure/
├── inventory/
│   ├── staging/
│   └── production/
├── playbooks/
├── roles/
└── collections/
```

**Run staging:** `ansible-playbook -i inventory/staging/ site.yml`
**Run production:** `ansible-playbook -i inventory/production/ site.yml`

### Monorepo: when it works

- Team is small (1-5 engineers), everyone has the same trust level
- Staging and production secrets use the same vault password (acceptable for small teams)
- You want one place to search, one PR to review
- CI/CD pipeline is simple: one repo, one pipeline

### Monorepo: when it breaks

- You want different access control for staging and production
- A junior engineer needs to experiment in staging without touching production
- Your vault contains production secrets that not everyone should see
- A bad merge to main could affect production immediately
- You need separate audit trails per environment

---

## Option B: Split inventory repositories

```
infrastructure-playbooks/    ← shared, no secrets
infrastructure-staging/      ← staging inventory + vault (staging secrets)
infrastructure-production/   ← production inventory + vault (production secrets)
```

See: `skeletons/split-staging/` for the full structure.

### Split repos: when it works

- You need different write access per environment (RBAC)
- Staging and production vault passwords must be different
- Regulatory requirements: production changes need separate approval
- Large team: junior engineers commit to staging, seniors gate production
- You want separate git history and audit trail per environment

### Split repos: when it breaks

- Small team with uniform trust: the overhead isn't worth it
- You need to do a cross-environment diff frequently
- Your CI/CD tooling doesn't support multi-repo pipelines well
- The team is not disciplined about keeping playbooks in sync

---

## Option C: Hybrid (playbooks + per-environment repos)

Most mature teams end up here:

```
ansible-playbooks/           ← git repo 1: all playbooks, no secrets
ansible-inventory-staging/   ← git repo 2: staging inventory + vault
ansible-inventory-production/← git repo 3: production inventory + vault
ansible-collections/         ← git repo 4 (optional): shared collection
```

Pipeline runs:
```bash
# Staging pipeline (triggered on PR to staging inventory repo)
git clone ansible-playbooks
git clone ansible-inventory-staging
ansible-playbook -i ansible-inventory-staging/inventory/ ansible-playbooks/site.yml

# Production pipeline (triggered on merge to production inventory repo, requires approval)
git clone ansible-playbooks
git clone ansible-inventory-production
ansible-playbook -i ansible-inventory-production/inventory/ ansible-playbooks/site.yml \
  --vault-password-file /ci/vault-production
```

---

## The decision matrix

| Factor | Monorepo | Split |
|--------|----------|-------|
| Team < 5 engineers | ✓ Better | ✗ Overhead |
| Regulatory audit requirements | ✗ Harder | ✓ Clean trail |
| Junior/senior access split needed | ✗ Hard | ✓ Natural |
| Different vault passwords required | ✗ Possible but awkward | ✓ Clean |
| Simple CI/CD | ✓ One pipeline | ✗ Multi-repo pipeline |
| Cross-env diff | ✓ Easy | ✗ Requires tooling |
| Scales beyond 10 engineers | ✗ Gets messy | ✓ Scales well |

## The migration path

Start with monorepo. When you feel the pain (usually: "I don't want to give
this engineer production access but they need staging access"), migrate.

Migration is straightforward:
1. Create two new repos
2. Copy `inventory/staging/` → repo 1, `inventory/production/` → repo 2
3. Remove inventory from monorepo
4. Update CI/CD pipelines
5. Done

The playbooks don't change. The roles don't change. Only the inventory moves.

## 🐇 Rabbit holes

- `/explore vault-id` — named vault passwords let you handle this in one repo
- `/explore awx-tower` — GUI for multi-repo pipelines with RBAC built in
- `/explore semaphoreui` — the open-source alternative to AWX
