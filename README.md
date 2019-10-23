# Odoo for RJ

This repository contains the basic instalations scripts and maintainace jobs
runned with ansible.

## Installation

To initialize the instalation process you need to define an ansible inventory:

```yml
---
staging:
  hosts:
    server_staging:
      ansible_port: 22
      ansible_host: 192.168.122.37
production:
  hosts:
    server_production:
      ansible_port: 22
      ansible_host: 192.168.122.195
```

Then you can run the instalation playbook:

    ansible-playbook -i inventory.yml -u [user] -K playbooks/odoo_instalation.yml
