ingress
=========

An Ansible role to deploy and manage OpenSearch Ingress on Kubernetes clusters.

Requirements
------------

Role Variables
--------------
opensearch_namespace: The namespace for OpenSearch (default: "opensearch")
domain_name: The domain name for the Ingress resource (default: "opensearch.local")

Dependencies
------------

This role is part of a collection.

Example Playbook
----------------

    - hosts: localhost
      roles:
         - { role: bbaassssiiee.opensearch.ingress }

License
-------

MIT

Author Information
------------------
@bbaassssiiee
