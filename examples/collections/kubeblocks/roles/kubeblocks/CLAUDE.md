# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Ansible role for installing and managing KubeBlocks in Kubernetes clusters. KubeBlocks is a Kubernetes operator for managing databases and stateful workloads (MySQL, PostgreSQL, Redis, Kafka, RabbitMQ, MongoDB, etc.).

The role handles:
- Installing KubeBlocks CRDs and Helm charts
- Managing database cluster lifecycle through KubeBlocks operators
- Mirroring Helm charts to private registries for air-gapped environments

## Linting

```bash
# Run pre-commit checks
pre-commit run --all-files

# Install pre-commit hooks
pre-commit install
```

Pre-commit runs yamllint, shellcheck, and various file checks.

## Architecture

### State Management

The role uses a state-based approach controlled by the `desired_state` variable:

- `desired_state: present` - Installs KubeBlocks (executes `tasks/present.yml`)
- `desired_state: absent` - Uninstalls KubeBlocks (executes `tasks/absent.yml`)

The main entry point (`tasks/main.yml`) delegates to the appropriate state file.

### Database Operations

Database cluster operations are handled through `tasks/ops_request.yml`, which:

1. Validates inputs (db_type, ops_request, db_namespace)
2. Renders Jinja2 templates from `templates/{db_type}/{ops_request}.yaml`
3. Applies the rendered YAML to Kubernetes using kubernetes.core.k8s
4. Waits for clusters to reach Running state
5. Displays cluster status and connection information

Supported database types: `kafka`, `mysql`, `postgresql`, `rabbitmq`, `redis`, `zookeeper`

Supported operations: `cluster`, `restart`, `start`, `stop`, `scale-in`, `scale-out`, `verticalscale`, `volumeexpand`, `upgrade`, `switchover-specified-instance`

### Template Organization

Templates are organized by database type in `templates/{db_type}/`:
- Each operation has a corresponding YAML template
- Templates use Ansible variables for configuration (cpu, memory, storage, etc.)
- Variables are defined in `defaults/main.yml`

### Registry Mirroring

The role supports private registry mirroring for air-gapped deployments:

1. Helm charts are mirrored using the scripts in `scripts/`:
   - `scrape_helm_charts.py` - Scrapes chart metadata from the upstream repository
   - `download_charts.py` - Downloads Helm charts with mirror directory structure
   - `pusher.sh` - Uploads charts to private registry

2. Container images are configured via `registry_host` variable
3. The role logs into both Helm and Docker registries using `registry_user` and `registry_pass`

## Key Variables

From `defaults/main.yml`:
- `desired_state` - Controls installation/removal (present/absent)
- `registry_host` - Private registry for images (for air-gapped environments)
- `kubeblocks_addons` - List of database addons to enable/disable
- `db_*` - Database-specific defaults (cpu, memory, storage, version)

From `vars/main.yml`:
- `kubeblocks_version` - KubeBlocks version to install (currently 1.0.1)
- `crd_manifest` - CRD manifest filename

## Important Implementation Details

### Installation Flow (present.yml)

1. Login to registries (Helm and Docker) if `registry_user` is defined
2. Copy and apply KubeBlocks CRDs (`files/kubeblocks_crds.yaml`)
3. Wait 2 minutes for CRD reconciliation
4. Add Helm repository (from `files_repo` variable)
5. Install KubeBlocks Helm chart with custom registry settings
6. Install enabled addons from `kubeblocks_addons` list

The installation overrides default image registries to support air-gapped deployments:
- `image.registry`
- `dataProtection.image.registry`
- `addonChartsImage.registry`
- `images.registry`

### Uninstallation Flow (absent.yml)

1. Remove cache directories if `delete_caches` is defined
2. Run `kbcli kubeblocks uninstall` with auto-approval
3. Delete all KubeBlocks CRDs (using kubectl grep and xargs)
4. Remove kb-system namespace

Note: CRD deletion uses `failed_when: false` because empty results return rc 123.

### Operations Workflow (ops_request.yml)

1. Assert db_type and ops_request are valid
2. Validate db_namespace follows RFC 1123 label format (lowercase alphanumeric with hyphens, max 63 chars)
3. Template the operation manifest to `files/{db_type}/{ops_request}.yaml`
4. Create namespace if it doesn't exist
5. Apply the operation manifest
6. Query for matching clusters using `kbcli` and `jq`
7. Wait for clusters to reach Running phase (30 retries, 10s delay)
8. Display cluster summary, components, instances, and connection info

The workflow uses shell commands with `jq` for filtering cluster results by componentDef prefix.

## Files to Check When Adding Features

- New database type: Add templates in `templates/{db_type}/`, update assertions in `tasks/ops_request.yml`
- New addon: Add to `kubeblocks_addons` list in `defaults/main.yml`
- Change KubeBlocks version: Update `kubeblocks_version` in `vars/main.yml`
- Modify installation: Edit `tasks/present.yml`
- Change mirror workflow: Update scripts in `scripts/` directory
