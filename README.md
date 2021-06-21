[![Build Dockerfile](https://github.com/augustoliks/ansible-ws-inventory-plugin/actions/workflows/docker-http-server.yml/badge.svg?branch=main)](https://github.com/augustoliks/ansible-ws-inventory-plugin/actions/workflows/docker-http-server.yml)
[![Build Ansible Collection](https://github.com/augustoliks/ansible-ws-inventory-plugin/actions/workflows/ansible-colection-galaxy.yml/badge.svg)](https://github.com/augustoliks/ansible-ws-inventory-plugin/actions/workflows/ansible-colection-galaxy.yml)

[![augustoliks/ws-inventory](https://img.shields.io/badge/dockerfile-augustoliks/ws--inventory:latest-blue.svg)](https://hub.docker.com/r/augustoliks/ws-inventory)
[![Docker Pulls](https://img.shields.io/docker/pulls/augustoliks/ws-inventory.svg)](https://hub.docker.com/r/augustoliks/ws-inventory/)

[![augustoliks/ws-inventory](https://img.shields.io/badge/ansible--galaxy-augustoliks.ws-green.svg)](https://galaxy.ansible.com/augustoliks/ws)

# ansible-ws-inventory-plugin

Ansible Inventory Plugin, created to get hosts from HTTP API.

Actual data source compatible:

- MongoDB;
- Filesystem (JSON format).

## Diagram

<p align="center">
  <img src=".docs/diagram.png" />
</p>

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

### Usage

*Example present in [./examples/](./examples) directory* 

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

---

## Configure HTTP Server API

[http-server-api](./http-server-api)

```json
{
  "filesystem": {
    "BIND_ADDRESS": "0.0.0.0",
    "BIND_PORT": 5000,
    "URI_ROOT_PATH": "/",
    "LOG_LEVEL": "DEBUG",
    "DB_DRIVER": "filesystem",
    "DB_OPTS": {
      "file": "/tmp/inventory.json"
    }
  },
  "mongodb": {
    "BIND_ADDRESS": "0.0.0.0",
    "BIND_PORT": 5000,
    "URI_ROOT_PATH": "/",
    "LOG_LEVEL": "DEBUG",
    "DB_DRIVER": "mongodb",
    "DB_OPTS": {
      "url": "mongodb://root:root@127.0.0.1:27017"
    }
  }
}
```