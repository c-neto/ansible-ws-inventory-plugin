from ansible.plugins.inventory import BaseInventoryPlugin


DOCUMENTATION = '''
name: augustoliks.ws.inventory
plugin_type: inventory
author:
    - Carlos Neto (carlos.neto.dev@gmail.com)
short_description: Get Inventory from HTTP API
version_added: 0.0.1
description:
    - Zabbix Inventory plugin
    - All vars from zabbix are prefixed with zbx_
requirements:
    - "python >= 3.4"
options:
    username:
        description:
            - Username to access HTTP API.
        type: str
        required: true
    password:
        description:
            - Password to access HTTP API.
        type: str
        required: true
    timeout:
        description:
            - The timeout of API request (seconds).
        type: int
        default: 10
    ws_url:
      description:
       - URL of web service HTTP API
      type: bool
      default: false
'''


class InventoryModule(BaseInventoryPlugin):

    NAME = 'ws_inventory'

    def verify_file(self, path: str):
        """return true/false if this is possibly a valid file for this plugin to consume"""

        if super(InventoryModule, self).verify_file(path) and path.endswith('inventory.yml'):
            valid = True
        else:
            valid = False

        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        config = self._read_config_data(path)

        hosts = [
            {
                'host_name': 'localhost',
                'localization': {
                    "address": "rua x, 6661",
                    "latitude": 0.0,
                    "longitude": 0.0
                }
            }
        ]

        for host in hosts:
            self.inventory.add_host(host['host'])
            self.inventory.set_variable(
                host['host_name'],
                'localization',
                host['localization']
            )
