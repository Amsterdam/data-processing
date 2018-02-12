
###############################################################################
# Helper functions to load in CROW, MORA file, clean, transform into pd.Dataframe
###############################################################################

import pandas as pd
import numpy as np

def read_crow_file(file, datecol):
    """
    parses the CROW afvaldata
    Args:
        file (xls/xlsx): containing at least a date column
        datecol: informat %Y-m-%d %H:%M:%S
    Returns:
        * pd.DataFrame: cleaned data frame with datum and time column added
    """
    
    df = (pd.read_excel(file)
          .pipe(strip_cols)
          .assign(
           datum = lambda x: pd.to_datetime(x[datecol], 
                   format = '%Y-%m-%d %H:%M:%S').dt.strftime('%Y-%m-%d'),
           tijd = lambda x: pd.to_datetime(x[datecol], 
                   format= '%Y-%m-%d %H:%M:%S').dt.strftime('%H:%M:%S'),
                  )
          .rename(columns={'breedtegraad': 'lat',
                           'lengtegraad': 'lon'})
         )
    #sort on datum (ascending)
    df = df.sort_values(by = 'datum').reset_index(drop=True)
    
    print('Resulting Data Shape: {} cols, {} rows.'.format(df.shape[0], df.shape[1]))
    
    return df


def read_mora_file(file, datecol):
    """
    parses the MORA Meldingen Openbare Ruimte Amsterdam
    Args:
        file (csv): containing at least a date column
        datecol: in format %d-m-%Y %H:%M:%S
    Returns:
        * pd.DataFrame: cleaned data frame with datum and time column added
    """
    
    df = (pd.read_csv(file, sep=';')
          .pipe(strip_cols)
          .assign(
           datum = lambda x: pd.to_datetime(x[datecol], 
                   format = '%d-%m-%Y %H:%M:%S').dt.strftime('%Y-%m-%d'),
           tijd = lambda x: pd.to_datetime(x[datecol], 
                   format= '%d-%m-%Y %H:%M:%S').dt.strftime('%H:%M:%S'),
                  )
          .rename(columns={'aa_adwh_bag_buurt_code': 'bag_buurt_code',
                           'aa_adwh_datum_melding': 'datum_melding',
                           'lattitude': 'lat',
                           'longitude': 'lon'}))    
    #sort on datum (ascending)
    #df = df.sort_values(by = 'datum').reset_index(drop=True)
    
    print('Resulting Data Shape: {} cols, {} rows.'.format(df.shape[0], df.shape[1]))
    
    return df

        
def strip_cols(df):
    
    # clean columns names
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ', '_')
    
    # clean values in columns with np.objects (str)
    for col in df.select_dtypes([np.object]).columns[0:]:
        df.loc[:,(col)] = df.loc[:,(col)].replace('', np.nan).fillna('Onbekend')
    
    df = df.copy()
    return df