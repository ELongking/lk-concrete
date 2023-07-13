import numpy as np
import pandas as pd
from typing import Tuple, Any

from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler
from sklearn.covariance import EllipticEnvelope

from .AlgoSpace import *


def train_test_split(xdata: np.array, ydata: np.array, train_size=0.7, valid_size=0.2) \
        -> Tuple[np.array, np.array, np.array, np.array, np.array, np.array]:
    num = xdata.shape[0]
    train_x, train_y = xdata[:int(num * train_size), :], ydata[:int(num * train_size), :]
    valid_x, valid_y = xdata[int(num * train_size): int(num * (train_size + valid_size)), :], \
                       ydata[int(num * train_size): int(num * (train_size + valid_size)), :]
    test_x, test_y = xdata[int(num * (1 - train_size - valid_size)):, :], \
                     ydata[int(num * (1 - train_size - valid_size)):, :]
    return train_x, train_y, valid_x, valid_y, test_x, test_y


def xy_split(df: pd.DataFrame, xcols: list, ycols: list) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return df.loc[:, xcols], df.loc[:, ycols]


def hotpoint_first(df: pd.DataFrame) -> pd.DataFrame:
    for col in range(df.shape[1]):
        mem = set()
        for row in range(df.shape[0]):
            ans = df.iloc[row, col]
            if pd.isnull(ans):
                pass
            else:
                try:
                    ans = float(ans)
                except:
                    ans = len(mem) + 1
                    mem.add(ans)
                df.iloc[row, col] = ans
    return df


def default_value_convert(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode == "zero":
        df.fillna(0, inplace=True)
    elif mode == "mean":
        mean = df.mean()
        for col in range(len(mean)):
            df.fillna(mean, inplace=True)
    else:
        df.dropna(inplace=True)
    return df


def anomaly_delete(df: pd.DataFrame, alpha=0.02):
    model = EllipticEnvelope(contamination=alpha)
    model.fit(df)

    outliers_mask = model.predict(df) == -1
    clean_data = df[~outliers_mask].copy()
    return clean_data


def data_normalization(xdata: np.array, mode: str) -> Tuple[Any, Any]:
    if mode == "minmax":
        scaler = MinMaxScaler()
        xdata = scaler.fit_transform(xdata)
    elif mode == "maxabs":
        scaler = MaxAbsScaler()
        xdata = scaler.fit_transform(xdata)
    else:
        scaler = StandardScaler()
        xdata = scaler.fit_transform(xdata)

    return xdata, scaler


def filter_algo_dicts(algos: list, mode: str) -> Tuple:
    _algo_dict = AlgoRegDict if mode == "reg" else AlgoClsDict
    _algo_dict_optimize = AlgoRegDictOptimize if mode == "reg" else AlgoClsDictOptimize

    algo_dict, algo_dict_optimize = dict(), dict()
    for key, val in _algo_dict.items():
        if key in algos:
            algo_dict[key] = val
    for key, val in _algo_dict_optimize.items():
        if key in algos:
            algo_dict_optimize[key] = val

    params_space = reg_params_space if mode == "reg" else cls_params_space

    return algo_dict, algo_dict_optimize, params_space
