from collections import defaultdict

import joblib
import os.path as osp
import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSignal
from hyperopt import Trials, fmin, tpe, space_eval
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold

from AlgoSpace import *

from typing import List, Tuple, Any

from LogText import LoggerHandler


def algo_filter(task_type: str,
                train_x: np.array,
                train_y: np.array,
                valid_x: np.array,
                valid_y: np.array,
                test_x: np.array,
                test_y: np.array,
                lh: LoggerHandler) -> Tuple[List, Any]:
    lh.tab_browser_emit(text="筛选步骤即将开始", step=2, level=2)

    algo_dict = AlgoRegDict.copy() if task_type == "reg" else AlgoClsDict.copy()
    model = []
    acc_train = []
    acc_val = []
    mse_train = []
    mse_val = []

    for key in algo_dict.keys():
        algo_dict[key].fit(train_x, train_y.ravel())
        acc_train.append(algo_dict[key].score(train_x, train_y.ravel()))
        acc_val.append(algo_dict[key].score(valid_x, valid_y.ravel()))

        train_pred = algo_dict[key].predict(train_x)
        val_pred = algo_dict[key].predict(valid_x)

        mse_train.append(round(mean_squared_error(train_y, train_pred), 3))
        mse_val.append(round(mean_squared_error(valid_y, val_pred), 3))

        mod = pd.DataFrame(
            [model, acc_train, acc_val, mse_train, mse_val, ]).T
        mod.columns = ['model', 'score_train', 'score_val', 'mse_train', 'mse_val']
        top_5_part = mod.sort_values(by='score_val', ascending=False)
        models = top_5_part.iloc[0:5, 0].tolist()
        lh.tab_browser_emit(text=f"筛选模型为: {', '.join(models)}", step=2, level=3)

        score = r2_score(test_y, algo_dict[models[0]].predict(test_x))
        lh.tab_browser_emit(text=f"筛选步骤得到最好效果的模型为: {models[0]}, 测试集得分为: {score}", step=2, level=3)
        return models, (models[0], algo_dict[key], score)


def hyperparams_extract(models: list,
                        task_type: str,
                        train_x: np.array,
                        train_y: np.array,
                        valid_x: np.array,
                        valid_y: np.array,
                        lh: LoggerHandler,
                        is_var: bool = False,
                        idx: int = -1) -> dict:
    _add = f"(特征筛选-No.{idx})" if is_var else ""
    lh.tab_browser_emit(text=f"参数优化步骤准备开始{_add}", step=2, level=2)

    algo_dict_optimize = AlgoRegDictOptimize.copy() if task_type == "reg" else AlgoClsDictOptimize.copy()
    params_space = reg_params_space if task_type == "reg" else cls_params_space
    xn = train_x.shape[0]

    model_after_params_optimize = defaultdict(dict)
    train_y, valid_y = train_y.ravel(), valid_y.ravel()
    feature = np.vstack((train_x, valid_x))
    value = np.hstack((train_y, valid_y))

    def hyper_on(params):
        all_r2_score = 0
        kf = KFold(n_splits=4, shuffle=True, random_state=42)

        for train_idx, test_idx in kf.split(feature):
            tr_x, te_x = feature[train_idx], feature[test_idx]
            tr_y, te_y = value[train_idx], value[test_idx]
            std = model(**params)
            std.fit(tr_x, tr_y)
            all_r2_score += r2_score(te_y, std.predict(te_x))
        return -all_r2_score / 4

    for mod in models:
        lh.tab_browser_emit(text=f"{mod}相关参数正在优化中...", step=2, level=3)

        model = algo_dict_optimize[mod]
        trials = Trials()
        res = fmin(hyper_on, space=params_space(mod, xn), trials=trials, algo=tpe.suggest,
                   max_evals=100)
        res = space_eval(params_space(mod, xn), res)

        if mod == 'CatBoost':
            res['iterations'] = 100

        model_after_params_optimize[mod] = model(**res)

    return model_after_params_optimize


def get_variable_importance(model, name: str) -> List:
    if name == 'Lasso':
        imp = model.coef_
    elif name == 'Ridge':
        imp = model.coef_
    elif name == 'ElasticNet':
        imp = model.coef_
    elif name == 'RandomForest':
        imp = model.feature_importances_
    elif name == 'DecisionTree':
        imp = model.feature_importances_
    elif name == 'AdaBoost':
        imp = model.feature_importances_
    elif name == 'ExtraTree':
        imp = model.feature_importances_
    elif name == 'LightGBM':
        imp = model.feature_importances_
    elif name == 'CatBoost':
        imp = model.feature_importances_
    elif name == 'XgBoost':
        imp = model.feature_importances_

    if imp.ndim != 1:
        imp = imp.ravel().reshape(-1, 1)
    else:
        imp = imp.reshape(-1, 1)
    return imp.ravel().tolist()


def variable_selected(model_name: str,
                      imp: list,
                      xcols: list,
                      train_x: np.array,
                      train_y: np.array,
                      valid_x: np.array,
                      valid_y: np.array,
                      test_x: np.array,
                      test_y: np.array,
                      task_type: str,
                      lh: LoggerHandler) -> Tuple:
    lh.tab_browser_emit(text="特征值筛选步骤准备开始...", step=2, level=2)

    idx_lst = list(range(1, len(imp) + 1))
    sort_zip = sorted(zip(imp, xcols, idx_lst), key=lambda x: x[0], reverse=True)
    label = [item[1] for item in sort_zip]

    lh.tab_browser_emit(text=f"特征权重从大到小的排列顺序为: {', '.join(label)}", step=2, level=3)

    score_lst = []
    best_score = float("-inf")
    res = tuple()
    for idx in idx_lst:
        child_label = label[:idx]
        child_train_x = train_x.take(idx_lst[0:idx], 1)
        child_valid_x = valid_x.take(idx_lst[0:idx], 1)
        child_test_x = test_x.take(idx_lst[0:idx], 1)
        child_model = hyperparams_extract(models=[model_name],
                                          train_x=child_train_x,
                                          train_y=train_y,
                                          valid_x=child_valid_x,
                                          valid_y=valid_y,
                                          task_type=task_type,
                                          lh=lh,
                                          is_var=True,
                                          idx=idx)

        for name, algo in child_model.items():
            algo.fit(child_train_x, train_y)
            score = r2_score(test_y.ravel(), algo.predict(child_test_x, 1))
            score_lst.append(score)
            if score > best_score:
                best_score = score
                res = (name, algo, best_score, child_label)

        lh.tab_browser_emit(text=f"前{idx}个特征所构成的模型, 测试集得分为: {score_lst[-1]}", step=2, level=3)

    lh.tab_browser_emit(text=f"表现最好的模型所使用的特征个数为: {len(res[-1])}, 测试集得分为: {res[-2]}", step=2, level=2)

    return res


def save_model(model, model_name: str, opt_path: str, desc: list = None) -> None:
    if desc:
        _desc = "-" + "-".join(desc)
        joblib.dump(model, osp.join(opt_path, model_name + _desc + ".pkl"))
    else:
        joblib.dump(model, osp.join(opt_path, model_name + ".pkl"))


def auto_prediction(train_x: np.array,
                    train_y: np.array,
                    valid_x: np.array,
                    valid_y: np.array,
                    test_x: np.array,
                    test_y: np.array,
                    xcols: list,
                    label: str,
                    task_type: str,
                    opt_path: str):
    from autogluon.tabular import TabularPredictor

    train_data = pd.DataFrame(np.hstack(train_x, train_y), columns=[*xcols, label])
    valid_data = pd.DataFrame(np.hstack(valid_x, valid_y), columns=[*xcols, label])
    test_data = pd.DataFrame(np.hstack(test_x, test_y), columns=[*xcols, label])

    if task_type == "reg":
        predictor = TabularPredictor(label=label,
                                     path=opt_path,
                                     problem_type="regression",
                                     eval_metric="r2",
                                     log_to_file=False, )
    else:
        predictor = TabularPredictor(label=label,
                                     path=opt_path,
                                     problem_type="multiclass",
                                     eval_metric="accuracy",
                                     log_to_file=False, )

    predictor.fit(train_data=train_data, tuning_data=valid_data, time_limit=300, presets="best_quality")
    res = predictor.predict(test_data)
    return r2_score(test_data[label], res)