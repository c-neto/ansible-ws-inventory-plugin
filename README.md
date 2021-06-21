# ansible-ws-inventory-plugin

Dynamic inventory from HTTP API.

![diagram](/.docs/diagram.png)

## Requirements

```bash
pip3 install requests
```

## Installing the Collection from Ansible Galaxy

Before using the Zabbix collection, you need to install it with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install augustoliks.ws
```

You can also include it in a requirements.yml file and install it via `ansible-galaxy collection install -r requirements.yml`, using the format:

```bash
---
collections:
  - name: augustoliks.ws
    version: 1.0.0
```

## How To Use

Create `ws-iventory.yml` file, and configure follow options:

```shell
plugin: augustoliks.ws.inventory
api_endpoint: 'http://127.0.0.1:8000/hosts'
```

## Examples

```bash
cd examples/
ansible-playbook -i ws-inventory.yml main.yml 
```
