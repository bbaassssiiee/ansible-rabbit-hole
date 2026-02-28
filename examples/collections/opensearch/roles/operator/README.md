operator
=========

An Ansible role to deploy and manage OpenSearch Operator on Kubernetes clusters.

Requirements
------------

Role Variables
--------------
registry_host: The container registry host (default: "docker.io")

Dependencies
------------

This role is part of a collection.

Example Playbook
----------------

    - hosts: localhost
      roles:
         - { role: bbaassssiiee.opensearch.operator }

License
-------

MIT

Author Information
------------------
@bbaassssiiee
