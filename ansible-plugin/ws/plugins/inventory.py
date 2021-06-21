from ansible.plugins.inventory import BaseInventoryPlugin
import requests


DOCUMENTATION = '''
name: augustoliks.ws.inventory
plugin_type: inventory
author:
    - Carlos Neto (carlos.neto.dev@gmail.com)
short_description: Get Inventory from HTTP API
version_added: 1.0.1
description:
    - Zabbix Inventory plugin
    - All vars from zabbix are prefixed with zbx_
requirements:
    - "python >= 3.4"
    - "requirements"
options:
    timeout:
        description:
            - The timeout of API request (seconds).
        type: int
        default: 10
    api_endpoint:
      description:
       - URL of web service HTTP API
      type: str
      default: false
      required: true
'''


class InventoryModule(BaseInventoryPlugin):

    NAME = 'inventory'

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

        response = requests.get(config['api_endpoint'])
        response.raise_for_status()

        for host in response.json():
            self.inventory.add_host(host['host_name'])
            self.inventory.set_variable(
                host['host_name'],
                'location',
                host['location']
            )
