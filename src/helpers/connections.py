import os
import configparser
from swiftclient.client import Connection
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from helpers.logging import logger


# Setup basic logging
logger = logger()

# -----------------
# Database stuff
# -----------------

def postgres_engine_pandas(config_full_path, db_config_name):
    """
        Pandas uses SQLalchemy, this is the config wrapper to insert config parameters in to_sql queries.
        db_config_name = dev or docker to get the ip user/password and port values.
    """
    config = configparser.RawConfigParser()
    config.read(config_full_path)

    postgres_url = URL(
        drivername='postgresql',
        username=config.get(db_config_name, 'user'),
        password=config.get(db_config_name, 'password'),
        host=config.get(db_config_name, 'host'),
        port=config.get(db_config_name, 'port'),
        database=config.get(db_config_name, 'dbname')
    )

    engine = create_engine(postgres_url)
    return engine


# -----------------
# Objectstore
# -----------------
def get_config(full_path):
    """
    Get config file with login credentials, port numbers...
    Args:
        full_path - provide path tot he config file/ auth.conf etc.
     """
    config = configparser.RawConfigParser()
    config.read(full_path)
    logger.info('Found these configs.. {}'.format(config.sections()))

    return config


def objectstore_connection(config_full_path, config_name, print_config_vars=None):
    """
    Get an objectsctore connection.

    Args:
        1. config_full_path: /path_to_config/config.ini or config.ini if in root.
        2. config_name: objectstore
        3. print_config_vars: if set to True: print all variables from the config file

    Returns:
        objectstore connection
      """

    assert os.environ['OBJECTSTORE_PASSWORD']

    config = get_config(config_full_path)

    if print_config_vars:
         logger.info('config variables.. :{}'.format(OBJECTSTORE))

    conn = Connection(authurl=config.get(config_name, 'AUTHURL'),
                      user=config.get(config_name, 'USER'),
                      key=os.environ['OBJECTSTORE_PASSWORD'],
                      tenant_name=config.get(config_name, 'TENANT_NAME'),
                      auth_version=config.get(config_name, 'VERSION'),
                      os_options={'tenant_id': config.get(config_name, 'TENANT_ID'),
                                  'region_name': config.get(config_name, 'REGION_NAME'),
                                  # 'endpoint_type': 'internalURL'
                                  })
    logger.info('Established successfull connection to {}'.format(config.get(config_name, 'TENANT_NAME')))

    return conn
