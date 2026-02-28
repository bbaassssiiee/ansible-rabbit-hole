#!/bin/bash -eux
MY_VER=$(grep '^version:' galaxy.yml|cut -d: -f2|sed 's/ //')
ansible-galaxy collection build --force
ansible-galaxy collection install "otobots-kubeblocks-$MY_VER.tar.gz" --force
