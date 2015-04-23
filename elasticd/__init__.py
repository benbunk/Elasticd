from elasticd import registrar

__author__ = 'PatelM'

import ConfigParser
import logging
import imp
import server
import os.path
from registrar import Registrar
from plugin_manager import PluginManager


FORMAT = '%(asctime)-15s %(module)s %(funcName)s %(thread)d %(message)s'
logging.basicConfig(format=FORMAT, filename='elasticd.log',level=logging.DEBUG)


def startup():
#load the config file and start the listener, daemon
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(os.path.split(os.path.dirname(__file__))[0], 'conf/settings.cfg'))
    if (len(config.sections()) < 1):
        logging.debug("Config is empty or incorrectly configured.")
        exit(-1)

    logging.debug("init starting up")

    p_manager = PluginManager(config)

    datastore = p_manager.get_datastore()
    registrar = Registrar(datastore)
    server.set_registrar(registrar)
    server.start()
