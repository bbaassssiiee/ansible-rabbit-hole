kubeblocks
==========

A role to install kbcli to work with KubeBlocks

https://kubeblocks.io

Run Databases on Kubernetes? Run with KubeBlocks.

KubeBlocks is crafted for managing databases on Kubernetes, designed by domain experts with decades of experience.
It supports a wide range of stateful workloads, including relational databases, NoSQL, message queues.
By streamlining operations, enhancing flexibility, and offering extensions, KubeBlocks makes database management easier in cloud-native environments.

Requirements
------------

EL or Ubuntu Linux.

Role Variables
--------------
kubeblocks_update is undefined by default, and then pulling charts and images, and pushing them to our `registry_host` is disabled.

To enable maintenance on the images you'll need read-write access to the `registry_host`
`kubeblocks_update: true`


```yml
# defaults
desired_state: present  # or absent
# kubeblocks_update: false

# inventory group_vars examples only
registry_host: "{{ lookup('env','REGISTRY_HOST') }}"
registry_user: "readonly"
registry_pass: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          31336333626434393366313239626465333531343235383265336139613466346363633362353163
```

Addons
------
The file `defaults/main.yml` has a list of kubeblocks_add_ons. Two properties are important:

- state: absent/present if absent the addon will be uninstalled with kbcli.
- enabled: true/false, if false the helm chart will be removed.

Several addons have state absent because they are installed by default when installing kubeblocks, and we don't want these.

Dependencies
------------
kubernetes.core collection

Example Playbook
----------------


```yaml
    - hosts: controller
      roles:
         - role: otobots.kubeblocks
```
