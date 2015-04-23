__author__ = 'patelm'

import imp
import logging
import importlib

DATASTORE_KEY = 'datastore'
DRIVER_KEY = 'driver'
RESOURCE_LOCATOR_KEY = 'resource-locator'

required_attributes = {DATASTORE_KEY: ['add_backend'],
                       DRIVER_KEY: ['update'],
                       RESOURCE_LOCATOR_KEY: ['get_resources']}

class PluginManager():

    plugins = {}

    def __init__(self, config):
        logging.debug('initializing plugins ')
        self._load_plugins(config)

    def get_datastore(self):
        return self.plugins[DATASTORE_KEY]

    def get_driver(self):
        return self.plugins[DRIVER_KEY]

    def get_resource_locator(self):
        return self.plugins[RESOURCE_LOCATOR_KEY]

    def _load_plugins(self,config):
        self._load_plugin(DATASTORE_KEY, config)
        self._load_plugin(DRIVER_KEY, config)
        self._load_plugin(RESOURCE_LOCATOR_KEY, config)

    def _load_plugin(self, type, config):
        logging.debug('Loading %s' % type)

        module_name = config.get(type, 'module_name')
        plugin_class = config.get(type, 'plugin_class')

        # Load the module and get a handle to the class definition.
        module = importlib.import_module(module_name)
        plugin_class = getattr(module, plugin_class)

        # Validate the class definition is correct.
        if self.plugin_is_valid(plugin_class, required_attributes[type]):
            # Instantiate the class
            self.plugins[type] = plugin_class(config)

    def plugin_is_valid(self, plugin_class, required_attributes):
        valid = True
        for attribute in required_attributes:
            if hasattr(plugin_class,attribute):
                valid = True
            else:
                return False
        return valid
