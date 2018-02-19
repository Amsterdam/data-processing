import configparser

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


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
