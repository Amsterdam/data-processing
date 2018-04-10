
###############################################################################
# Helper functions to load in CROW, MORA file, clean, transform into pd.Dataframe
###############################################################################

import pandas as pd
import numpy as np
import argparse
from datetime import datetime
import sys

def read_crow_file(file, datecol):
    """
    parses the CROW afvaldata
    Args:
        file (xls/xlsx): containing at least a date column
        datecol: 'datum' format %Y-m-%d %H:%M:%S
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
    
    print('Resulting Data Shape: {} cols, {} ros.'.format(df.shape[0], df.shape[1]))
    
    return df


def read_mora_file(file, datecol):
    """
    parses the MORA csv and transforms into clean Pandas Dataframe
    Args:
        file (csv/xls/xlsx): containing at least a date column
        datecol: 'aa_adwh_datum_melding' format %Y-m-%d %H:%M:%S
    Returns:
        pd.DataFrame: cleaned data frame with datum and time column added
    """
    
    df = (pd.read_csv(file, sep=';')
          .pipe(strip_cols)
          .assign(
           datum = lambda x: pd.to_datetime(x[datecol], 
                   format = '%d-%m-%Y %H:%M:%S').dt.strftime('%Y-%m-%d'),
           tijd = lambda x: pd.to_datetime(x[datecol], 
                   format = '%d-%m-%Y %H:%M:%S').dt.strftime('%H:%M:%S'),
           jaar = lambda x: pd.to_datetime(x[datecol],
                   format = '%d-%m-%Y %H:%M:%S').dt.strftime('%Y')
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
    
    """ 
    simple utility function to clean dataframe columns
    """
    
    # clean columns names
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ', '_')
    
    # clean values in columns with np.objects (str)
    for col in df.select_dtypes([np.object]).columns[0:]:
        df.loc[:,(col)] = df.loc[:,(col)].replace('', np.nan).fillna('Onbekend')
    
    df = df.copy()
    return df


def valid_date(s):
    try:
        return datetime.strptime(s, "%d-%m-%Y %H:%M:%S")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle
    

def parser():
    """Parser function to run arguments from the command line and to add description to sphinx."""
    parser = argparse.ArgumentParser(description=
    """ parses the MORA Meldingen Openbare Ruimte Amsterdam once downloaded from objectstore.
    Args:
        file (csv): containing at least a date column
        datecol: in format %d-%m-%Y %H:%M:%S
    Returns:
        * pd.DataFrame: cleaned data frame with datum and time column added
    command line example: 
      `read_mora_file(PATH_TO_MORA_FILE + MORA_FILE, datecol='aa_adwh_datum_melding')`
    """
                                    )
    parser.add_argument('file', 
                        type=str,
                        help="MORA file to be loaded in")
    parser.add_argument('datecol',
                        type=str,
                        help="date column from which the date and time are extracted and put into different \
                        columns. The mora date column in source file is 'aa_adwh_datum_melding'")
    return parser


def main(): 
    args = parser().parse_args()
    read_mora_file(args.file, args.datecol)


if __name__ == '__main__':
    main()