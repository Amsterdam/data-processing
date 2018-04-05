
###############################################################################
# Helper functions to enrich data with public event data
###############################################################################

import pandas as pd
import json
import urllib
import argparse


def get_event_json():
    """parse public event data from json at amsterdam.data.nl
    Args:
        None
    Returns:
        * pd.DataFrame: data frame with events in Amsterdam
    """

    url = 'https://open.data.amsterdam.nl/Evenementen.json'
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode('utf-8'))
    # extract values from json
    results = []

    for item in data:
        result = {}

        result['title'] = item['details']['en']['title']
        result['name'] = item['location']['name']
        result['adress'] = item['location']['adress']
        result['zipcode'] = item['location']['zipcode']
        result['lat'] = item['location']['latitude']
        result['lon'] = item['location']['longitude']
        result['dates'] = item['dates']

        results.append(result)

    # convert to Pandas Dataframe
    event_df = pd.DataFrame(results)

    # extract start and enddate from nested lists
    event_df = pd.concat([event_df.drop(['dates'], axis=1), event_df['dates'].apply(pd.Series)], axis=1)
    # replace NaNs with startdates, enddates
    for row in event_df.loc[event_df.singles.isnull(), 'singles'].index:
        event_df.at[row, 'singles'] = [event_df.loc[row, 'startdate'],event_df.loc[row, 'enddate']]
    # extract first date, last date from singles column
    event_df['startdate'] = [item[0] for item in event_df.singles]
    event_df['enddate'] = [item[-1] for item in event_df.singles]

    event_df = event_df.drop('singles', axis=1)

    for col in ['startdate', 'enddate']:
        event_df[col] = pd.to_datetime(event_df[col], format = '%d-%m-%Y')
    
    for col in ['lon', 'lat']:
        event_df[col] = event_df[col].str.replace(',', '.').astype('float64')

    # add column event duration in days
    event_df['no_days'] = (event_df.enddate - event_df.startdate).astype('timedelta64[D]') + 1

    return event_df


def parser():
    """Parser function to run arguments from the command line and to add description to sphinx."""
    parser = argparse.ArgumentParser(description="""
    parse public event data from json at amsterdam.data.nl
    Args:
        None
    Returns:
        * pd.DataFrame: data frame with events in Amsterdam
    command line example:
        get_event_json()
    """)
    return parser


def main():
    args = parser().parse_args()
    get_event_json()


if __name__ == "__main__":
    main()
