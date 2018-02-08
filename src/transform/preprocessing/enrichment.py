
###############################################################################
# Helper functions for specific data enrichment processes
###############################################################################

import pandas as pd


def enrich_datetime(df):
    """Add datetime features (i.e. year, day of week, etc., also for ML feature generation)
    Args:
        df (pd.DataFrame): schedule or historical data
    Returns:
        pd.DataFrame
    """

    # Convert datetime_sch to pandas time stamps
    df['datetime_sch'] = pd.to_datetime(df['datetime_sch'])

    # Sort along time axis
    df = df.sort_values('datetime_sch', ascending=True)

    # Calculate hour and quarter hour
    df = df.assign(hour=lambda x: x['datetime_sch'].dt.hour +
                                  x['datetime_sch'].dt.minute / 60.)
    df = df.assign(time_qhour=lambda x: (x['datetime_sch'].dt.minute / 15).astype(int) + x['hour'] * 4)

    df['date'] = df['datetime_sch'].dt.date

    # Compute day-like features below from date and merge back onto history
    date_features = pd.DataFrame(df['date'].unique(), columns=['date'])

    # Compute features from dates
    date_features = date_features.assign(year=lambda self: [x.year for x in self['date']])
    date_features = date_features.assign(month=lambda self: [x.month for x in self['date']])
    date_features = date_features.assign(week=lambda self: [x.isocalendar()[1] for x in self['date']])
    date_features = date_features.assign(dayofweek=lambda self: [x.weekday() for x in self['date']])
    date_features = date_features.assign(dayofyear=lambda self: [x.timetuple().tm_yday for x in self['date']])

    # Merge back onto original data frame
    n_rows_before = df.shape[0]
    df = pd.merge(df, date_features, on=['date'], suffixes=('_old', ''))

    # Check that no rows are dropped
    assert df.shape[0] == n_rows_before, "No rows may be dropped while " \
                                         "merging onto date features. " \
                                         "This is a bug!"

    return df
