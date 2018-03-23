import os
import configparser
import psycopg2

from swiftclient.client import Connection
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from datapunt_processing import logger


# Setup basic logging
logger = logger()

# -----------------
# Database stuff
# -----------------


def postgres_engine_pandas(config_full_path, db_config_name):
    """
    Pandas uses SQLalchemy, this is the config wrapper to insert config parameters in to_sql queries.

    Args:
      1. config_full_path: location of the config.ini file including the name of the file, for example authentication/config.ini
      2. db_config_name: dev or docker to get the ip user/password and port values.

    Returns:
        The postgres pandas engine to do sql queries with.
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


def psycopg_connection_string(config_full_path, db_config_name):
    """
    Postgres connection string for psycopg2.

    Args:
      1. config_full_path: location of the config.ini file including the name of the file, for example authentication/config.ini
      2. db_config_name: dev or docker to get the ip user/password and port values.

    Returns:
        Returns the psycopg required connection string: 'PG:host= port= user= dbname= password='
    """

    config = configparser.RawConfigParser()
    config.read(config_full_path)

    logger.info('Config names: {}'.format(config.sections()))
    print(db_config_name)
    host = config.get(db_config_name,'host')
    logger.info(host)
    port = config.get(db_config_name,'port')
    user = config.get(db_config_name,'user')
    dbname = config.get(db_config_name,'dbname')
    password = config.get(db_config_name,'password')

    return 'host={} port={} user={} dbname={} password={}'.format(
        host, port, user, dbname, password
    )


def execute_sql(pg_str, sql):
    """
    Execute a sql query with psycopg2.

    Args:
        1. pg_str: connection string using helper function psycopg_connection_string, returning:``host= port= user= dbname= password=``
        2. sql: SQL string in triple quotes::

            ```CREATE TABLE foo (bar text)```

    Returns:
        Executed sql with conn.cursor().execute(sql)
    """
    with psycopg2.connect(pg_str) as conn:
        logger.info('connected to database')
        with conn.cursor() as cursor:
            logger.info('start exectuting sql query')
            cursor.execute(sql)

# -----------------
# Objectstore
# -----------------
def get_config(full_path):
    """
    Get config file with all login credentials, port numbers, etc.

    Args:
        full_path: provide the full path to the config.ini file, for example authentication/config.ini

    Returns:
        The entire configuration file to use them with ``config.get(config_name, 'AUTHURL')``
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
        An objectstore connection session.
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
