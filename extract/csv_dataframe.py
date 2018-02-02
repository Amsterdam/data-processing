
###############################################################################
# Helper functions to load in CROW xlsx file, clean and transform into pd.Dataframe
###############################################################################

import pandas as pd
import numpy as np

def read_crowfile(file, datecol):
    """parses the CROW afvaldata
    datecol = format %Y-m-%d %H:%M:%S
    """
    df = (pd.read_excel(file)
          .pipe(strip_cols)
          .assign(
           datum = lambda x: pd.to_datetime(x[datecol], 
                   format = '%Y-%m-%d %H:%M:%S').dt.strftime('%Y:%m:%d'),
           tijd = lambda x: pd.to_datetime(x[datecol], 
                   format= '%Y-%m-%d %H:%M:%S').dt.strftime('%H:%M:%S'),
                  )
          .rename(columns={'breedtegraad': 'lat',
                           'lengtegraad': 'lon'})
         )
    #sort on datetime (ascending)
    df = df.sort_values(datecol).reset_index(drop=True)
    
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
