import numpy as np
import pandas as pd
from typing import Tuple, Any

from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler
from sklearn.covariance import EllipticEnvelope
from sklearn.decomposition import PCA

from category_encoders.cat_boost import CatBoostEncoder
from category_encoders.helmert import HelmertEncoder
from category_encoders.james_stein import JamesSteinEncoder
from category_encoders.leave_one_out import LeaveOneOutEncoder
from category_encoders.m_estimate import MEstimateEncoder
from category_encoders.ordinal import OrdinalEncoder
from category_encoders.sum_coding import SumEncoder
from category_encoders.target_encoder import TargetEncoder
from category_encoders.woe import WOEEncoder

from .AlgoSpace import *


def train_test_split(xdata: np.array, ydata: np.array, train_size=0.7, valid_size=0.2) \
        -> Tuple[np.array, np.array, np.array, np.array, np.array, np.array]:
    num = xdata.shape[0]
    train_x, train_y = xdata[:int(num * train_size), :], ydata[:int(num * train_size)]
    valid_x, valid_y = xdata[int(num * train_size): int(num * (train_size + valid_size)), :], \
                       ydata[int(num * train_size): int(num * (train_size + valid_size))]
    test_x, test_y = xdata[int(num * (1 - train_size - valid_size)):, :], \
                     ydata[int(num * (1 - train_size - valid_size)):]
    return train_x, train_y, valid_x, valid_y, test_x, test_y


def xy_split(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    return df.iloc[:, :-1], df.iloc[:, -1]


def hotpoint_first(df: pd.DataFrame, encoder_name: str, cat_cols: list, left_cols: list) -> Tuple:
    if not cat_cols:
        return df, None

    base_encoder = None
    if encoder_name == "Ordinal":
        encoder = OrdinalEncoder(cols=cat_cols)
    else:
        base_encoder = OrdinalEncoder(cols=cat_cols)
        _df = base_encoder.fit_transform(X=df.loc[:, left_cols], y=df.iloc[:, -1])
        df = pd.concat([_df, df.iloc[:, -1]], axis=1)
        if encoder_name == "WOE":
            encoder = WOEEncoder(cols=cat_cols)
        elif encoder_name == "Target":
            encoder = TargetEncoder(cols=cat_cols)
        elif encoder_name == "Sum":
            encoder = SumEncoder(cols=cat_cols)
        elif encoder_name == "MEstimate":
            encoder = MEstimateEncoder(cols=cat_cols)
        elif encoder_name == "LeaveOneOut":
            encoder = LeaveOneOutEncoder(cols=cat_cols)
        elif encoder_name == "Helmert":
            encoder = HelmertEncoder(cols=cat_cols)
        elif encoder_name == "JamesStein":
            encoder = JamesSteinEncoder(cols=cat_cols)
        elif encoder_name == "CatBoost":
            encoder = CatBoostEncoder(cols=cat_cols)
        elif encoder_name == "MEstimate":
            encoder = MEstimateEncoder(cols=cat_cols)
        else:
            raise NotImplementedError("To be implemented")

    _df = encoder.fit_transform(X=df.loc[:, left_cols], y=df.iloc[:, -1])
    df = pd.concat([_df, df.iloc[:, -1]], axis=1)
    return df, base_encoder, encoder


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


def reduce_dimension(xdata: np.array) -> np.array:
    _pca = PCA()
    _pca.fit(xdata)
    variance_ratio = _pca.explained_variance_ratio_
    n_components = np.argmax(np.cumsum(variance_ratio) >= 0.8) + 1

    pca = PCA(n_components=n_components)
    pca_data = pca.fit_transform(xdata)

    return pca_data, pca, n_components
