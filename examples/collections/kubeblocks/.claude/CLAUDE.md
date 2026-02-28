# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Ansible collection (`otobots.kubeblocks`) for installing and managing KubeBlocks in Kubernetes clusters. KubeBlocks is a Kubernetes operator for managing databases and stateful workloads (MySQL, PostgreSQL, Redis, Kafka, RabbitMQ, MongoDB, etc.).

The collection includes:
- **kubeblocks role**: Installs KubeBlocks operators, manages database cluster lifecycle, and supports air-gapped deployments
- **kbcli role**: Installs the kbcli command-line tool
- **Playbooks**: Example playbooks for common operations

## Building and Installing the Collection

```bash
# Build the collection (extracts version from galaxy.yml)
./collection.sh

# Or manually:
ansible-galaxy collection build --force
ansible-galaxy collection install otobots-kubeblocks-<version>.tar.gz --force
```

## Linting

```bash
# Lint YAML files
yamllint .

# Lint Ansible playbooks and roles
ansible-lint

# Install pre-commit hooks (if configured)
pip install -r requirements.txt
pre-commit install
pre-commit run --all-files
```

Linting configuration:
- `.yamllint`: YAML style rules (max line length 240, consistent indentation)
- `.ansible-lint`: Skips experimental, risky-shell-pipe, and role-name rules

## Running Playbooks

```bash
# Install KubeBlocks
ansible-playbook playbooks/kubeblocks.yml -e desired_state=present

# Uninstall KubeBlocks
ansible-playbook playbooks/kubeblocks.yml -e desired_state=absent

# Manage database clusters
ansible-playbook playbooks/kubeblocks-db.yml \
  -e db_type=postgresql \
  -e ops_request=cluster \
  -e db_namespace=my-db

# Install kbcli tool
ansible-playbook playbooks/kbcli.yml -e desired_state=present
```

## Collection Architecture

### Two-Role Structure

1. **kubeblocks role** (`roles/kubeblocks/`): Core KubeBlocks operator management
   - Manages KubeBlocks installation/removal via Helm
   - Handles database cluster operations through templated manifests
   - Supports private registry mirroring for air-gapped environments

2. **kbcli role** (`roles/kbcli/`): CLI tool installation
   - Installs kbcli binary on controller nodes
   - Used by kubeblocks role for cluster status queries

### Playbook Entry Points

- `playbooks/kubeblocks.yml`: Install/uninstall KubeBlocks operator
- `playbooks/kubeblocks-db.yml`: Execute database operations (create cluster, scale, etc.)
- `playbooks/kbcli.yml`: Install/uninstall kbcli tool
- `playbooks/clear-caches.yml`: Cleanup utility

### State-Based Workflow

The `kubeblocks` role uses `desired_state` to control operations:

- `desired_state: present` → `tasks/present.yml` (install)
- `desired_state: absent` → `tasks/absent.yml` (uninstall)
- Database operations → `tasks/ops_request.yml` (always executed via kubeblocks-db.yml)

### Database Operations Model

Database operations are templated YAML manifests in `roles/kubeblocks/templates/{db_type}/`:

Supported database types: `kafka`, `mysql`, `postgresql`, `rabbitmq`, `redis`, `zookeeper`

Supported operations:
- `cluster`: Create new database cluster
- `restart`, `start`, `stop`: Lifecycle management
- `scale-in`, `scale-out`: Horizontal scaling
- `verticalscale`: CPU/memory adjustments
- `volumeexpand`: Storage expansion
- `upgrade`: Version upgrades
- `switchover-specified-instance`: High availability operations

Workflow:
1. Templates are rendered with Ansible variables (cpu, memory, storage, etc.)
2. Manifests are applied to Kubernetes via `kubernetes.core.k8s`
3. Role waits for clusters to reach Running state (using `kbcli` and `jq`)
4. Cluster status and connection info are displayed

### Air-Gapped Support

The `kubeblocks` role supports private registry mirroring:

1. Scripts in `roles/kubeblocks/scripts/`:
   - `scrape_helm_charts.py`: Scrapes chart metadata from upstream
   - `download_charts.py`: Downloads Helm charts with mirror directory structure
   - `extract_helm_images.py`: Extracts container image references
   - `pusher.sh`: Uploads charts to private registry

2. Registry configuration via variables:
   - `registry_host`: Private registry hostname
   - `registry_user` / `registry_pass`: Authentication credentials
   - `kubeblocks_update`: Enable mirroring workflow

3. Helm installation overrides all image registries to use `registry_host`

## Key Variables

### Collection-Level Variables

From `roles/kubeblocks/vars/main.yml`:
- `kubeblocks_version`: KubeBlocks version to install (currently 1.0.1)
- `crd_manifest`: CRD manifest filename

From `roles/kubeblocks/defaults/main.yml`:
- `desired_state`: Installation state (present/absent)
- `registry_host`: Private registry for air-gapped deployments
- `registry_user` / `registry_pass`: Registry authentication
- `kubeblocks_addons`: List of database addons with name and enabled flag
- `db_*`: Database-specific defaults (cpu, memory, storage, replicas, version)

### Playbook Variables

Required for database operations:
- `db_type`: Database type (postgresql, mysql, redis, etc.)
- `ops_request`: Operation type (cluster, scale-out, etc.)
- `db_namespace`: Kubernetes namespace (must be RFC 1123 compliant)

## Important Implementation Details

### Installation Flow (present.yml)

1. Login to Helm and Docker registries (if `registry_user` defined)
2. Copy and apply KubeBlocks CRDs from `files/kubeblocks_crds.yaml`
3. Wait 2 minutes for CRD reconciliation
4. Add Helm repository (from `files_repo` variable)
5. Install KubeBlocks Helm chart with registry overrides
6. Install enabled addons from `kubeblocks_addons` list

Registry overrides applied:
- `image.registry`
- `dataProtection.image.registry`
- `addonChartsImage.registry`
- `images.registry`

### Uninstallation Flow (absent.yml)

1. Remove cache directories (if `delete_caches` defined)
2. Run `kbcli kubeblocks uninstall --auto-approve`
3. Delete all KubeBlocks CRDs via kubectl
4. Remove kb-system namespace

Note: CRD deletion uses `failed_when: false` because empty results return rc 123.

### Database Operations (ops_request.yml)

1. Validate `db_type` and `ops_request` are in allowed lists
2. Validate `db_namespace` is RFC 1123 compliant (lowercase alphanumeric, hyphens, max 63 chars)
3. Template operation manifest to `files/{db_type}/{ops_request}.yaml`
4. Create namespace if it doesn't exist
5. Apply manifest using `kubernetes.core.k8s`
6. Query matching clusters using `kbcli cluster list` and `jq` filters
7. Wait for clusters to reach Running phase (30 retries, 10s delay)
8. Display cluster summary, components, instances, and connection info

The workflow uses `jq` to filter cluster results by componentDef prefix matching `db_type`.

## Adding Features

### New Database Type

1. Create template directory: `roles/kubeblocks/templates/{db_type}/`
2. Add operation templates (cluster.yaml, scale-out.yaml, etc.)
3. Update assertion list in `roles/kubeblocks/tasks/ops_request.yml`
4. Add default variables in `roles/kubeblocks/defaults/main.yml`

### New Database Operation

1. Create template: `roles/kubeblocks/templates/{db_type}/{operation}.yaml`
2. Update allowed operations in `roles/kubeblocks/tasks/ops_request.yml`
3. Test with: `ansible-playbook playbooks/kubeblocks-db.yml -e db_type=<type> -e ops_request=<operation> -e db_namespace=test`

### New KubeBlocks Addon

1. Add to `kubeblocks_addons` list in `roles/kubeblocks/defaults/main.yml`
2. Set `enabled: true/false` to control whether the addon is installed
3. Only addons with `enabled: true` will be installed via Helm during the installation flow

### Change KubeBlocks Version

Update `kubeblocks_version` in `roles/kubeblocks/vars/main.yml`

### Modify Registry Mirroring

Edit scripts in `roles/kubeblocks/scripts/`:
- Python scripts use `requests` library for HTTP operations
- `pusher.sh` handles chart uploads to private registry

## Requirements

- Ansible >= 2.16.0 (specified in `meta/runtime.yml`)
- Python packages: `pre-commit` (in `requirements.txt`)
- Ansible collections: `kubernetes.core`
- External tools: `kbcli`, `kubectl`, `helm`, `jq`

## Role-Specific Documentation

For detailed implementation guidance on the kubeblocks role, see `roles/kubeblocks/CLAUDE.md`.
