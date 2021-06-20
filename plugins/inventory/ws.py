from ansible.plugins.inventory import BaseInventoryPlugin


class InventoryModule(BaseInventoryPlugin):

    NAME = 'ws'  # used internally by Ansible, it should match the file name but not required

    def verify_file(self, path: str):
        """return true/false if this is possibly a valid file for this plugin to consume"""
        valid = True
#        valid = False

#        if super(InventoryModule, self).verify_file(path):
#            if path.endswith('carlos.yml'):
#                valid = True

        return valid

    def parse(self, inventory, loader, path, cache=True):

        # call base method to ensure properties are available for use with other helper methods
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # this method will parse 'common format' inventory sources and
        # update any options declared in DOCUMENTATION as needed
        config = self._read_config_data(path)
        print(config)
        # if NOT using _read_config_data you should call set_options directly,
        # to process any defined configuration for this plugin,
        # if you don't define any options you can skip
        # self.set_options()

        # example consuming options from inventory source
        hosts = [
            {
                'host': 'localhost',
                'meta': {
                    'latitude': 0.0,
                    'longitude': 0.0
                }
            }
        ]

        # parse data and create inventory objects:
        for host in hosts:
            self.inventory.add_host(host['host'])
            self.inventory.set_variable(host['host'], 'localization', host['meta'])
