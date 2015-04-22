__author__ = 'patelm'

import imp
import logging


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
        plugin_name = config.get(type, 'plugin_name')
        load_path = config.get(type, 'module_path')
        plugin = self._load_module(plugin_name, [load_path])
        if self.plugin_is_valid(plugin, required_attributes[type]):
            self.plugins[type] = plugin(config)

    def _load_module(self,name, path=None):
        logging.debug('loading %s from %s' % (name, path))
        module_name, rest = name.split('.', 1)
        logging.debug('%s - %s' % (module_name, rest))
        f, filename, description = imp.find_module(module_name, path)
        module = imp.load_module(module_name, f, filename, description)
        if hasattr(module, rest):
            return getattr(module, rest)
        elif '.' not in rest:
            return module
        return self._load_module(rest, [module.__path__])

    def plugin_is_valid(self, plugin, required_attributes):
        valid = True
        for attribute in required_attributes:
            if hasattr(plugin,attribute):
                valid = True
            else:
                return False
        return valid
