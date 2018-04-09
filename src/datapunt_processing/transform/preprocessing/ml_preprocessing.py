
###############################################################################
# Helper functions for machine learning preprocessing purposes
# Some functions require numpy array, some pd.Dataframes as specified
###############################################################################

from __future__ import division
import pandas as pd
import numpy as np
import math
import sys
from sklearn.preprocessing import LabelEncoder, Normalizer, Imputer


# some functions executing some basic preprocessing steps for ml
predict_cols = ['x']
feature_cols = list(set(df.columns) - set(predict_cols))

def preprocess(df, predict_cols, feature_cols, do_outlier_removal=False):
    
        """
    Label encode categorical features to 0,1,...,x
    Args:
        df: pandas dataframe
        predict_cols: the column(s) containing the predictive variable
        feature_cols : the columns that are categorical and need to be encoded
        do_outlier_removal: if True: remove the outlier based on median absolute deviation (MAD)
    returns:
        dataframe with label encoded features and target columns
    """
    
       
    col_dtypes = df[list(set(df.columns) - set(predict_cols))].dtypes
    cat_features = [c for c, dtype in col_dtypes.iteritems() if dtype not in ['int64', 'int32', 'float64']] 
    num_features = [c for c, dtype in col_dtypes.iteritems() if dtype in ['int64', 'int32', 'float64']]

    print("Encoding...")
    for c in cat_features:
        df.loc[:, c] = LabelEncoder().fit_transform(df.loc[:, c].fillna('unknown'))
        # agg = df.groupby(c).size().to_frame('size').reset_index()
        # df = pd.merge(df, agg, on=c)
        # df = df.drop(c, axis=1).rename(columns={'size': c})

    print("Imputing...") # outcomment if not needed
    imp = Imputer(missing_values=np.nan, strategy="median", axis=0)

    # Impute numerical features
    df[num_features] = imp.fit_transform(df[num_features])
    df[num_features] = df[num_features].fillna(-1000)

    if do_outlier_removal:
        for col in df.columns.values:
            outliers = np.where(_is_outlier(df.loc[:, (col)])) # refers to outlier function
            df.ix[:, (col)].iloc[outliers] = median

    print("Dropping NaN prediction rows...")
    # remove na`s in target cols. Otherwise impute
    #df = df.dropna(subset=predict_cols, axis=0)

    # Impute targets
    df[predict_cols] = df[predict_cols].fillna(-1)

    return df
  
def _is_outlier(points, thresh=3.5):
    """
    Remove points based on their "median absolute deviation".
    Returns a boolean array with True if points are outliers and False 
    otherwise.
    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
                 a modified z-score (based on the median absolute deviation) greater
                 than this value will be classified as outliers.
    Returns:
    --------
        mask : A numobservations-length boolean array.
    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation # tweak if necessary

    return modified_z_score > thresh


def normalize(X, axis=-1, order=2):
    """ 
    Normalize the dataset X 
    Args:
        np.array X
    """
    l2 = np.atleast_1d(np.linalg.norm(X, order, axis))
    l2[l2 == 0] = 1
    return X / np.expand_dims(l2, axis)


def standardize(X):
    """ 
    Standardize the dataset X 
    Args:
        np.array X
    """
    X_std = X
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    for col in range(np.shape(X)[1]):
        if std[col]:
            X_std[:, col] = (X_std[:, col] - mean[col]) / std[col]
    # X_std = (X - X.mean(axis=0)) / X.std(axis=0)
    return X_std


def train_test_split(X, y, test_size=0.5, shuffle=True, seed=None):
    """ 
    Split the data into train and test sets 
    Args:
        np.array X
        np.array y 
    """
    if shuffle:
        X, y = shuffle_data(X, y, seed)
    # Split the training data from test data in the ratio specified in
    # test_size
    split_i = len(y) - int(len(y) // (1 / test_size))
    X_train, X_test = X[:split_i], X[split_i:]
    y_train, y_test = y[:split_i], y[split_i:]

    return X_train, X_test, y_train, y_test


def shuffle_data(X, y, seed=None):
    """ 
    Random shuffle of the samples in X and y 
    Args:
        np.array X
        np.array y 
    """
    if seed:
        np.random.seed(seed)
    idx = np.arange(X.shape[0])
    np.random.shuffle(idx)
    return X[idx], y[idx]


def k_fold_cross_validation_sets(X, y, k, shuffle=True):
    """ 
    Split the data into k sets of training / test data 
    """
    if shuffle:
        X, y = shuffle_data(X, y)

    n_samples = len(y)
    left_overs = {}
    n_left_overs = (n_samples % k)
    if n_left_overs != 0:
        left_overs["X"] = X[-n_left_overs:]
        left_overs["y"] = y[-n_left_overs:]
        X = X[:-n_left_overs]
        y = y[:-n_left_overs]

    X_split = np.split(X, k)
    y_split = np.split(y, k)
    sets = []
    for i in range(k):
        X_test, y_test = X_split[i], y_split[i]
        X_train = np.concatenate(X_split[:i] + X_split[i + 1:], axis=0)
        y_train = np.concatenate(y_split[:i] + y_split[i + 1:], axis=0)
        sets.append([X_train, X_test, y_train, y_test])

    # Add left over samples to last set as training samples
    if n_left_overs != 0:
        np.append(sets[-1][0], left_overs["X"], axis=0)
        np.append(sets[-1][2], left_overs["y"], axis=0)

    return np.array(sets)
