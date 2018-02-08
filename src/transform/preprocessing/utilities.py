import logging
import os

from IPython.display import display

import pandas as pd
import numpy as np
import pickle


def merge_and_report(left, right, on: list, description='',
                     n_unmatched_limit=None) -> pd.DataFrame:
    """Performs a merge between two data frame and reports stats on matches
    Only left merges are supported for now. If a column is present in both the
    left and right data frame, the left column has priority and the right
    column is ignored.
    Args:
        left (pd.DataFrame): lhs
        right (pd.DataFrame): rhs
        on (list[str]): columns to match on.
        description (str or None): description of what merge is done
        n_unmatched_limit (int): throw error when number of rows not found in
            left side is larger than this number
    Returns:
        pd.DataFrame
    """

    left_cols = set(left.columns) - set(on)
    right_cols = set(right.columns) - set(on)

    if left_cols & right_cols != set():
        logging.debug("in merge_and_report: left and right side contain the "
                      "same columns. Only taking left side.")

    right_cols_merge = list((set(right.columns) - set(left.columns)) | set(on))

    df = pd.merge(left, right[right_cols_merge], on=on, how='left', indicator=True)

    # Reporting
    n_matched = np.sum(df['_merge'] == 'both')
    n_unmatched = np.sum(df['_merge'] == 'left_only')

    if description is not None:
        msg = "Merge" + ((" (" + description + ") ") if description else " ") + "on " + str(on)
        logging.info(msg + ": n_matched = " + str(n_matched) + ", n_unmatched = " + str(n_unmatched))

    df.drop(['_merge'], axis=1, inplace=True)

    if n_unmatched_limit is not None:
        if n_unmatched > n_unmatched_limit:
            raise RuntimeError("Number of unmatched rows too large (limit={})"
                               .format(n_unmatched_limit))

    return df


def cols_not_in(columns, df: pd.DataFrame):
    return [c for c in columns if c not in df.columns]


def rms(array):
    """
    Calculate the root mean square of an array
    """
    return np.sqrt(np.mean((array)**2))


def calc_error(df):
    """
    :param df:  DataFrame
                Predictions data frame.
    :return:    Series
                Error (truth - prediction)
    """
    return df['passengers_tob'] - df['pred_passengers_tob']



def is_numeric(column):
    """
    :param column:  Series
                    A column.
    :return:        bool
                    True when is a numeric type.
    """
    return np.issubdtype(column.dtype, np.number)


def assert_unique(series):
    """
    Assert that all values are unique. Raises a value error if not. Empty series are ignored.
    :param series: input
    :return: none
    """
    if len(series) > 0:
        if series.value_counts().iloc[0] != 1:
            raise ValueError("All entries are required to be unique.")


def optional_make_dir(path):
    """Creates directory at if it does not exist yet
    Args:
        path (str): path to create directory in
    """

    if not os.path.exists(path):
        os.mkdir(path)


class BigFile(object):
    """Wrapper for pickling big files
    See pickle_big_dump and pickle_big_load functions.
    """

    def __init__(self, f):
        """Initializer
        Args:
            f: file handle
        """
        self.f = f

    def __getattr__(self, item):
        return getattr(self.f, item)

    def read(self, n):
        """Read n bytes
        Reads a big file in batch of almost ~ 1 GB
        Args:
            n (int): number of bytes
        Returns:
            bytearray: buffer
        """
        if n >= (1 << 31):
            buffer = bytearray(n)
            idx = 0
            while idx < n:
                batch_size = min(n - idx, 1 << 31 - 1)
                buffer[idx:idx + batch_size] = self.f.read(batch_size)
                idx += batch_size
            return buffer
        return self.f.read(n)

    def write(self, buffer):
        """Write buffer
        Writes in batches of ~ 1GB
        Args:
            buffer (bytearray): buffer
        """
        n = len(buffer)
        idx = 0
        while idx < n:
            batch_size = min(n - idx, 1 << 31 - 1)
            self.f.write(buffer[idx:idx + batch_size])
            idx += batch_size


def pickle_big_dump(obj, file_path):
    with open(file_path, "wb") as f:
        return pickle.dump(obj, BigFile(f), protocol=pickle.HIGHEST_PROTOCOL)


def pickle_big_load(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(BigFile(f))


def get_script_dir():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')


def get_last_full_year(df):
    """Find the last full year in data frame
    E.g. will return 2016 if you are in 2017.
    Args:
        df (pd.DataFrame): input data, has column dayofyear
    Returns:
        int: last full year
    """
    return df[df.dayofyear >= 365].year.drop_duplicates().max()
