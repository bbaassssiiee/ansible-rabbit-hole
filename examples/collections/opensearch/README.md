## Overview

This is an Ansible collection (`bbaassssiiee.opensearch`) for deploying and managing OpenSearch clusters on Kubernetes. It uses the OpenSearch Operator and manages certificates, credentials, and ingress configuration.

## Common Commands

### Running the main playbook

Deploy OpenSearch cluster:
```bash
ansible-playbook playbooks/cluster.yml -e "opensearch_namespace=logging" -e "desired_state=present"
```

Remove OpenSearch cluster:
```bash
ansible-playbook playbooks/cluster.yml -e "opensearch_namespace=logging" -e "desired_state=absent"
```

### Running with tags

Execute specific stages:
```bash
# Setup only (namespaces, certificates, secrets)
ansible-playbook playbooks/cluster.yml -e "desired_state=present" --tags setup

# Operator only
ansible-playbook playbooks/cluster.yml -e "desired_state=present" --tags operator

# OpenSearch cluster only
ansible-playbook playbooks/cluster.yml -e "desired_state=present" --tags opensearch

# Ingress only
ansible-playbook playbooks/cluster.yml -e "desired_state=present" --tags ingress
```

### Testing the filter plugin

Test the bcrypt_hash filter:
```bash
ansible-playbook playbooks/tests.yml -e "password=your_password"
```

### Linting

Lint Ansible files:
```bash
ansible-lint
```

Lint YAML files:
```bash
yamllint .
```

## Architecture

### Deployment Flow

The main playbook (`playbooks/cluster.yml`) orchestrates deployment in this order:

1. **Setup** (`roles/setup`): Creates namespaces, CA secrets, and TLS certificates (transport, HTTP, admin) using cert-manager
2. **Operator** (`roles/operator`): Deploys OpenSearch Operator via Helm chart to the `operators` namespace
3. **OpenSearch** (`roles/opensearch`): Creates OpenSearchCluster custom resource, secrets for credentials, and optional NodePort service
4. **Ingress** (`roles/ingress`): Configures ingress-nginx for dashboard access

Teardown happens in reverse order when `desired_state=absent`.

### Role Structure

- **setup**: Manages foundational resources (namespaces, CA issuer, certificates)
- **operator**: Deploys the OpenSearch Operator using Helm (OCI registry)
- **opensearch**: Manages the OpenSearch cluster CRD, credentials, security config
- **ingress**: Creates Kubernetes Ingress resources for dashboard UI

### Key Variables

Each role uses `defaults/main.yml` for configuration. Critical variables:

- `desired_state`: `present` or `absent` (controls deployment/removal)
- `opensearch_namespace`: Target namespace (default: `logging`)
- `deployment_environment`: `development`, `acceptance`, or `production` (controls resource sizing)
- `opensearch_admin_pass`, `opensearch_index_pass`, `opensearch_dashboard_pass`: Override in inventory
- `containers_to_deploy`: Container image references with digests (in `opensearch` and `operator` roles)

### Custom Filter Plugin

The collection includes a custom filter plugin at `plugins/filter/bcrypt_hash.py` that generates bcrypt password hashes for OpenSearch security configuration. Configure filter plugin path in `ansible.cfg`:

```ini
filter_plugins = plugins/filter
```

### Certificate Management

Uses cert-manager with a ClusterIssuer (`ca-issuer` by default). Certificates are created as K8s secrets:
- Transport certificate (node-to-node communication)
- HTTP certificate (client-to-node communication)
- Admin certificate (admin user authentication)

Templates in `roles/setup/templates/` define the certificate resources.

### State Management

All roles follow a consistent pattern with tasks organized as:
- `main.yml`: Routes to present/absent tasks based on `desired_state`
- `present.yml`: Creates/updates resources
- `absent.yml`: Removes resources
- `verify.yml`: (where applicable) Validates deployment

## Kubernetes Integration

The collection depends on:
- `kubernetes.core` collection (>= 5.1.0)
- `community.general` collection (>= 10.3.0)

All operations run on `localhost` with `connection: local` since they interact with the Kubernetes API.

## Diagnostics

See `TESTS.md` for comprehensive kubectl commands to verify:
- Pod status and health
- OpenSearch cluster health
- Certificate configuration
- Authentication and connectivity
- Ingress configuration
