import glob
import pandas as pd

# to DO: argparser
# load csv to PostgreSQL database, write to 'service_afvalcontainers' schema
def load_csv_to_postgres(datadir, filename, table_name, schema, config_path, config_name, all_csv=None):
    """
    Load csv into postgres for single & multiple files
    Args:
        datadir: data directory where file to be uploaded is stored. f.i. data/
        filename: name of the csv
        table_name: name of the tbale in postgresql
        schema: the schema in postgreSQL where data file should land
        config_path: path to the config file. f.i. auth/config.ini
        config_name: name of the databse config. f.i. 'postgresql'
        all_csv = default false. If True will upload all the csv files in the datadir.
        
        example: load_csv_to_postgres(datadir=PATH, filename='afvalcontainers_munged.csv', 
                     table_name = 'afvalcontainers_munged',
                     schema = 'service_afvalcontainers', 
                     config_path= '../config.ini', 
                     config_name='postgresql')
        """
    
    df = pd.read_csv(datadir + filename)
        
    if all_csv:
        csv_files = [glob.glob(x) for x in [datadir + '*.csv']]
        for csv_file in csv_files:
            df = pd.read_csv(datadir + csv_file)
        
    # establish engine
    engine = postgres_engine_pandas(config_path, config_name)
    print (engine)
    
    table_name = table_name
    
    df.to_sql(table_name, engine, schema = schema,
              if_exists='replace', 
              index=True, 
              index_label='idx')      