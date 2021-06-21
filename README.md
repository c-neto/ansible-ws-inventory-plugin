# ansible-ws-inventory-plugin

Dynamic inventory from HTTP API.

Actual data source compatible:

- MongoDB;
- Filesystem (JSON format)

## Diagram

![diagram](/.docs/diagram.png)

## Configure Ansible Inventory Plugin: augustoliks.ws

### Requirements

```bash
pip3 install requests
```

### Installing the Collection from Ansible Galaxy

Before using the `augustoliks.ws` collection, you need to install it with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install augustoliks.ws
```

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```bash
---
collections:
  - name: augustoliks.ws
    version: 1.0.0
```

### How To Use

Create inventory file `ws-iventory.yml`, and configure follow options:

```shell
# Plugin Name
plugin: augustoliks.ws.inventory

# Plugin Options
api_endpoint: 'http://127.0.0.1:8000/hosts'
username: ""
password: ""
timeout: 10
```

Run Ansible playbook with `ws-iventory.yml` inventory.

```bash
cd examples/
ansible-playbook -i ws-iventory.yml main.yml 
```
