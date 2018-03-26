import os
import argparse

import pandas as pd

from datapunt_processing.helpers.connections import postgres_engine_pandas
from datapunt_processing import logger

# Setup basic logging
logger = logger()


def load_xls(datadir, config_path, db_config_name):
    """Load xlsx into postgres for multiple files"""
    files = os.listdir(datadir)
    files_xls = [f for f in files if f.split('.')[-1] in ('xlsx', 'xls')]
    logger.info(files_xls)

    for filename in files_xls:
        df = pd.read_excel(datadir + '/' + filename)
        if df.empty:
            logger.info('No data')
            continue

        logger.info("added " + filename)
        logger.info(df.columns)

        # load the data into pg
        engine = postgres_engine_pandas(config_path, db_config_name)
        # TODO: link to to_sql function
        table_name = filename.split('.')[0]
        df.to_sql(table_name, engine, if_exists='replace', index=True, index_label='idx')  # ,dtype={geom: Geometry('POINT', srid='4326')})
        logger.info(filename + ' added as ' + table_name)


def parser():
    desc = 'Upload xls files as separate tables into PostgreSQL using Pandas to_sql.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'datadir', type=str, help='Local data directory, for example: projectdir/data')
    #parser.add_argument(
    #    'tablename', type=str, help='Write the desired table name in lowercase and underscores.')
    parser.add_argument(
        'config_path', type=str, help='Location of the config.ini file: for example: /auth/config.ini')
    parser.add_argument(
        'dbconfig', type=str, help='config.ini name of db settings: dev or docker')
    return parser



def main():
    args = parser().parse_args()
    load_xls(args.datadir,
             #args.tablename,
             args.config_path,
             args.dbconfig)


if __name__ == '__main__':
    main()
