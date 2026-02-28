# Tests & Diagnostics

## Quick Backend Validation

###Validate the node port

```sh
kubectl get svc opensearch-nodeport -n logging
```

### Obtain an IP address of a node

```sh
 kubectl get nodes -o json | jq '.items[] | {name: .metadata.name, ip: .status.addresses[] | select(.type=="InternalIP") | .address}'
 ```

### List the indices
```sh
curl -k -u $USER:$PASSWORD https://$IP_ADDRESS:9200/_cat/indices?v
```

## Quick Dashboard Validation

```sh
curl -k -H "Host: opensearch.local" https://$IP_ADDRESS/app/login
```

## Initial Diagnostics

### Check if OpenSearch pods are running
```sh
kubectl get pods -n logging -l app=opensearch-cluster-nodes
```

### Get the events
```sh
kubectl get events -n logging --sort-by='.lastTimestamp' | tail -20
```

### Check if the OpenSearch cluster is green
```sh
kubectl get opensearchcluster opensearch-cluster -n logging
```

### Check OpenSearch cluster health in more detail
```sh
kubectl exec -n logging opensearch-cluster-nodes-0 -- curl -k -u admin:admin https://localhost:9200/_cluster/health | jq
```

### Check if all pods are running and ready (1/1)
```sh
kubectl get pods -n logging | grep opensearch-cluster-nodes
```

### Check if dashboards are running
```sh
kubectl logs -n logging deployment/opensearch-cluster-dashboards  | grep running | jq
```

### Inspect the opensearchcluster spec
```sh
kubectl get opensearchcluster opensearch-cluster -n logging -o yaml
```

### Check Dashboards logs for more detailed errors
```sh
kubectl logs -n logging deployment/opensearch-cluster-dashboards --tail=50 | jq
```

## Certificates
### Check if certificates exist as secrets
```sh
kubectl get secrets -n logging | grep -E "(ca-certificate|opensearch-admin-credentials|opensearch-http-cert)"
```

### Check if the certificates are properly mounted.
```sh
kubectl describe pod -n logging -l app=opensearch-cluster-dashboards | grep -A 12 "Volumes:"
```

### Check if certificates exist in the dashboards pod
```sh
kubectl exec -n logging deployment/opensearch-cluster-dashboards -- ls -la /usr/share/opensearch-dashboards/config/certs/
```

### Check if the CA is the Issuer you expect
```sh
kubectl get secret ca-certificate -n logging -o jsonpath='{.data.ca\.crt}' | base64 -d | openssl x509 -text -noout
kubectl exec -n logging deployment/opensearch-cluster-dashboards -- cat /usr/share/opensearch-dashboards/config/certs/ca.crt | openssl x509 -noout -text
```

## Authentication
Verify the admin credentials secret exists and is correct.
### Check if the admin credentials secret exists
```sh
kubectl get secret opensearch-admin-credentials -n logging -o yaml
```

### Test authentication directly against OpenSearch
```sh
kubectl exec -n logging opensearch-cluster-nodes-0 -- curl -k -u admin:$(kubectl get secret opensearch-admin-credentials -n logging -o jsonpath='{.data.password}' | base64 -d) https://localhost:9200/ | jq
```

## Network Connectivity
Test if Dashboards can reach the OpenSearch service:

### From within the dashboards pod, test connectivity
```sh
kubectl exec -n logging deployment/opensearch-cluster-dashboards -- curl -k -u admin:$(kubectl get secret opensearch-admin-credentials -n logging -o jsonpath='{.data.password}' | base64 -d) https://opensearch-cluster.logging.svc.cluster.local:9200/_cluster/health | jq
```

## Service and Endpoint Issues

### Check if the OpenSearch service exists and has endpoints
```sh
kubectl get svc opensearch-cluster -n logging
kubectl get endpoints opensearch-cluster -n logging
```

## Check security plugin status
```sh
kubectl exec -n logging opensearch-cluster-nodes-0 -c opensearch -- curl -s -k -u admin:$(kubectl get secret opeth='{.data.password}' | base64 -d) https://localhost:9200/_plugins/_security/health | jq
```

## Check the Operator
```sh
kubectl get deployments -n operators
kubectl get pods -n operators
```
## Check if the ingress pods are running

```sh
kubectl get pods -n ingress-nginx
```

## Get detailed information about the ingress

```sh
kubectl describe ingress opensearch-cluster-dashboards-ingress -n logging
```

## Check if the service exists and has the right selector
```sh
kubectl get svc opensearch-cluster-dashboards -n logging
kubectl describe svc opensearch-cluster-dashboards -n logging
```
