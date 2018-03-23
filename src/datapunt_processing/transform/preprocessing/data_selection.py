
###############################################################################
# Helper functions for specific data selections on a pd.DataFrame
###############################################################################

import datetime as dt
import logging
import pandas as pd


def select_and_report(df, selection, description, max_drop_rate=None):
    """Select data from a data frame and report how many rows were dropped.
    Args:
        df(pd.DataFrame): apply selection on this data frame
        selection(pd.Series): boolean selection
        description(str): description in log message
        max_drop_rate(float, optional): max fraction of dropped rows
    Returns:
        pd.DataFrame
    """

    prev_rows = len(df)
    df = df[selection]
    curr_rows = len(df)
    n_dropped = prev_rows - curr_rows

    logging.info("Selection on {}: dropped {} rows."
                 .format(description, n_dropped))

    if max_drop_rate is not None:
        drop_rate = n_dropped / prev_rows
        if drop_rate > max_drop_rate:
            raise RuntimeError("Fraction of dropped rows too large ({}%, "
                               "max allowed {}%)."
                               .format(drop_rate * 100, max_drop_rate * 100))

    return df


def remove_nan_targets(df: pd.DataFrame):
    """Remove NaNs in the target list.
    Args:
        df(pd.DataFrame): data frame on which to operate
        run (Run): run parameters
    Returns:
        pd.DataFrame
    """

    n_row_original = len(df)
    df = df.dropna()
    logging.info("{} entries in the training set had no info on training "
                 "targets and were removed."
                 .format(n_row_original - len(df)))
    return df



class DateRange:
    """Class representing a range of dates
    
    Can be used to select data in data frames if the data frame contains a
    column 'date' and is populated with datetime.date values.
    """
    def __init__(self, start, end):
        """Define a period from start to end
        start (dt.datetime): start of the period
        end (dt.datetime): end of the period
            Note, the end date is not included in selections!
        """
        self.start = start
        self.end = end

        if self.end < self.start:
            raise RuntimeError("Start should precede end when defining a "
                               "DateRange")

    @staticmethod
    def from_dataframe(df: pd.DataFrame):
        """Create date range from a data frame
        Args:
            df (pd.DataFrame): a data frame  having a date column populated
                with dt.datetime values.
        Returns:
          DateRange object
        """
        if 'date' not in df:
            raise IndexError("The column 'date' was not found in the passed "
                             "data frame.")

        if len(df) < 2:
            return None

        return DateRange(df.date.min(), df.date.max() + dt.timedelta(days=1))

    def length(self):
        """Returns the time delta between end and start
        
        Returns:
            dt.timedelta
        """
        return self.end - self.start

    def __repr__(self):
        """To string conversion
        Returns:
            str
        """
        return "DateRange: " + str(self.start) + " - " + str(self.end)

    def __and__(self, other):
        """Operator &, intersects two date ranges
        Args:
            other (DateRange): other date range to intersect with
        Returns:
            DateRange
        """

        r_start = max(self.start, other.start)
        r_end = min(self.end, other.end)

        if r_start < r_end:
            return DateRange(r_start, r_end)
        else:
            return None

    def __eq__(self, other):
        """Check equality (operator ==)
        Args:
            other (DateRange): other date range to compare with
        Return:
            bool
        """
        return (self.start == other.start) and (self.end == other.end)

    def select(self, df):
        """Apply the data range selection on a data frame
        Args:
          df (pd.DataFrame): input data frame
        Returns:
          pd.DataFrame
        """

        assert 'date' in df, "DataFrame df should have a date column."

        result = df.loc[(df['date'] >= self.start) &
                        (df['date'] < self.end), :].copy()

        if len(result) == 0:
            logging.warning("Date selection yields empty result")

        return result
