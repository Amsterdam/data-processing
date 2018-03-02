import os
import configparser
import logging
from swiftclient.client import Connection

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from helpers.objectstore import Objectstore

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)

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

def objectstore_connection(config_full_path, config_name):
    """Get objectstore settings as a dict
       :config_full_path = /path_to_config/config.ini or config.ini if in root.
       :config_name = objectstore
    """
    assert os.environ['OBJECTSTORE_PASSWORD']

    config = configparser.RawConfigParser()
    logger.info('Connecting to config..: {}'.format(config_name))
    config.read(config_full_path)
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
