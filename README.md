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

```yml
---
collections:
  - name: augustoliks.ws
    version: 1.0.3
```

### Usage

Create inventory file `ws-iventory.yml`, and configure follow options:

```yml
# Plugin Name
plugin: augustoliks.ws.inventory

# Plugin Options
api_endpoint: 'http://127.0.0.1:8000/hosts'
timeout: 10
```

Run Ansible playbook with `ws-iventory.yml` inventory.

```bash
ansible-playbook -i ws-iventory.yml main.yml 
```

---

## Configure HTTP Server API

Webserver Source code is in the [http-server-api/](./http-server-api) directory. 

Application wrapped in Container Image format, but it can be runs a system wide, with [systemd](https://github.com/systemd/systemd) or [sysvinit](https://wiki.debian.org/Debate/initsystem/sysvinit) etc.

## Pull Docker Image

```
docker pull augustoliks/ws-inventory:latest
```

## Configuration 

Source code was made in Python. The configuration app, using a library [dynaconf](https://github.com/rochacbruno/dynaconf), for provides multiple formats to configure properties of project. For default, configuration was made in JSON file format, but it could be made from any other source and format compatible with a configuration library. 

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

- `ENV_FOR_DYNACONF`: Select high level set properties. Options available: `mongodb`, `filesystem`;
- `BIND_ADDRESS`: Bind of HTTP Server address uvicorn;
- `BIND_PORT`: Port of HTTP Server uvicorn;
- `LOG_LEVEL`: Log of application. Levels available: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`;
- `URI_ROOT_PATH`: Base URI path routes of webserver (util in reverse proxys servers `nginx`, `apache`, `traefix`);
- `DB_DRIVER`: Persistence Tecnology. This option choosed, change properties of `DB_OPTS` properties. Technologies available: `mongodb`, `filesystem`
- `DB_OPTS`: Properties access Persist Layer:

  - mongodb:
    - `url`: URL with basic-auth to access mongodb instance

  - filesystem: 
    - `file`: Path of file which will be used with database.

## Example Complete

- Enter [./examples/](./examples) directory: 

```bash
cd examples/
```

- Install dependencies (require `virtualenv`):

```bash
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

- Provides `ws-inventory` and `mongodb` container instances:

```bash
docker-compose pull
docker-compose up -d
```

- Insert hosts:

<img src=".docs/swagger-insert-host.jpg" alt="drawing" width="500"/>

- List hosts:

<img src=".docs/swagger-list-hosts.jpg" alt="drawing" width="500"/>

- Check `playbook-main.yml` properties:

> :warning: `augustoliks` should be change with your system username.

```bash
$ cat playbook-main.yml                                                                                                     

---
- hosts: all
  remote_user: augustoliks
  become_user: augustoliks
  become: yes
  gather_facts: False

  tasks:
    - ansible.builtin.debug:
        var: hostvars
```

- Check `ws-inventory.yml` properties:

```bash
$ cat ws-inventory.yml                                                                                                      

plugin: "augustoliks.ws.inventory"
api_endpoint: "http://127.0.0.1:5000/read/hosts"
timeout: 10
```

- Test plugin

```bash
$ ansible-inventory -i ws-inventory.yml --graph
$ ansible-inventory -i ws-inventory.yml --list
```

- Run playbook

```bash
$ ansible-playbook -i ws-inventory.yml playbook-main.yml --ask-pass                                                         

SSH password: 

PLAY [all] ********************************************************************************************************************

TASK [ansible.builtin.debug] **************************************************************************************************
ok: [localhost] => {
    "hostvars": {
        "localhost": {
            ...
            "location": {
                "address": "string",
                "latitude": 35.1234,
                "longitude": 10.1234
            },
            ...
        }
    }
}

PLAY RECAP ********************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0                                                                     
```
