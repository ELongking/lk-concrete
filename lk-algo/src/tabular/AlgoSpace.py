import math

from sklearn.linear_model import Lasso, Ridge, ElasticNet
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, ExtraTreesRegressor, \
    RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBRegressor, XGBClassifier
from lightgbm import LGBMRegressor, LGBMClassifier
from catboost import CatBoostRegressor, CatBoostClassifier

from hyperopt import hp

AlgoRegDict = {
    'ElasticNet': ElasticNet(),
    'Lasso': Lasso(),
    'Ridge': Ridge(),
    'RandomForest': RandomForestRegressor(),
    'DecisionTree': DecisionTreeRegressor(),
    'AdaBoost': AdaBoostRegressor(),
    'ExtraTree': ExtraTreesRegressor(),
    'LightGBM': LGBMRegressor(),
    'CatBoost': CatBoostRegressor(verbose=False,
                                  allow_writing_files=False),
    'XgBoost': XGBRegressor(),
}

AlgoRegDictOptimize = {
    'ElasticNet': ElasticNet,
    'Lasso': Lasso,
    'Ridge': Ridge,
    'RandomForest': RandomForestRegressor,
    'DecisionTree': DecisionTreeRegressor,
    'AdaBoost': AdaBoostRegressor,
    'ExtraTree': ExtraTreesRegressor,
    'LightGBM': LGBMRegressor,
    'CatBoost': CatBoostRegressor,
    'XgBoost': XGBRegressor,
}

AlgoClsDict = {
    'RandomForest': RandomForestClassifier(),
    'DecisionTree': DecisionTreeClassifier(),
    'AdaBoost': AdaBoostClassifier(),
    'ExtraTree': ExtraTreesClassifier(),
    'LightGBM': LGBMClassifier(),
    'CatBoost': CatBoostClassifier(verbose=False,
                                   allow_writing_files=False),
    'XgBoost': XGBClassifier()
}
AlgoClsDictOptimize = {
    'RandomForest': RandomForestClassifier,
    'DecisionTree': DecisionTreeClassifier,
    'AdaBoost': AdaBoostClassifier,
    'ExtraTree': ExtraTreesClassifier,
    'LightGBM': LGBMClassifier,
    'CatBoost': CatBoostClassifier,
    'XgBoost': XGBClassifier
}


def reg_params_space(algo_name: str, xn: int) -> dict:
    if algo_name == 'ElasticNet':
        return {
            'alpha': hp.uniform('alpha', 0.001, 10),
            'l1_ratio': hp.uniform('l1_ratio', 0, 1),
            'max_iter': hp.choice('max_iter', range(100 * xn, 1000 * xn)),
            "tol": hp.uniform("tol", 0, 1e-3)
        }

    elif algo_name == 'Lasso':
        return {
            'alpha': hp.uniform('alpha', 0.001, 1),
            'selection': hp.choice('selection', ['cyclic', 'random']),
            'max_iter': hp.choice('max_iter', range(100 * xn, 1000 * xn + 1)),
            "tol": hp.uniform("tol", 0, 1e-3)
        }

    elif algo_name == 'Ridge':
        return {
            'alpha': hp.uniform('alpha', 0.001, 10),
            'max_iter': hp.choice('max_iter', range(100 * xn, 1000 * xn + 1)),
            'solver': hp.choice('solver', ['svd', 'cholesky', 'sparse_cg', 'lsqr', 'sag']),
            "tol": hp.uniform("tol", 0, 1e-3)
        }

    elif algo_name == 'RandomForest':
        return {
            'max_depth': hp.choice('max_depth', range(5, 51)),
            'min_samples_split': hp.choice('min_samples_split', range(2, 21)),
            'min_samples_leaf': hp.choice('min_samples_leaf', range(1, 11)),
            'n_estimators': hp.choice('n_estimators', range(10 * xn, 100 * xn + 1))
        }


    elif algo_name == 'DecisionTree':
        return {
            'splitter': hp.choice('splitter', ['best']),
            'max_depth': hp.choice('max_depth', range(5, 51)),
            'min_samples_split': hp.choice('min_samples_split', range(2, 21)),
            'min_samples_leaf': hp.choice('min_samples_leaf', range(1, 11)),
            'max_leaf_nodes': hp.choice('max_leaf_nodes', range(10, 101))
        }

    elif algo_name == 'AdaBoost':
        return {
            'n_estimators': hp.choice('n_estimators', range(50 * xn, 200 * xn + 1)),
            'learning_rate': hp.uniform('learning_rate', 0.01, 1),
            'loss': hp.choice('loss', ['linear', 'square', 'exponential']),
            'base_estimator': hp.choice('base_estimator', [DecisionTreeRegressor(), SVR(), KNeighborsRegressor()])
        }

    elif algo_name == 'ExtraTree':
        return {
            'max_depth': hp.choice('max_depth', range(5, 51)),
            'min_samples_split': hp.choice('min_samples_split', range(2, 21)),
            'min_samples_leaf': hp.choice('min_samples_leaf', range(1, 11)),
            'n_estimators': hp.choice('n_estimators', range(50 * xn, 200 * xn))
        }



    elif algo_name == 'LightGBM':
        return {
            'reg_alpha': hp.uniform('reg_alpha', 0, 1),
            'reg_lambda': hp.uniform('reg_lambda', 0, 1),
            'learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
            'max_depth': hp.choice('max_depth', range(4, int(10 * math.log(xn)) + 1)),
            'min_child_samples': hp.choice('min_child_samples', range(1, 21)),
            'min_child_weight': hp.uniform('min_child_weight', 0, 10)
        }

    elif algo_name == 'CatBoost':
        return {
            'learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
            'iterations': hp.choice('iterations', [20]),
            'l2_leaf_reg': hp.uniform('l2_leaf_reg', 1, 11),
            'bagging_temperature': hp.uniform('bagging_temperature', 0.02, 1),
            'boosting_type': hp.choice('boosting_type', ['Ordered', 'Plain']),
            'depth': hp.choice('depth', range(4, int(10 * math.log(xn)) + 1)),
            'leaf_estimation_method': hp.choice('leaf_estimation_method', ['Newton', 'Gradient']),
            'random_strength': hp.choice('random_strength', range(1, 102)),
            'verbose': hp.choice('verbose', [False]),
            'allow_writing_files': hp.choice('allow_writing_files', [False])
        }

    elif algo_name == 'XgBoost':
        return {
            'reg_alpha': hp.uniform('reg_alpha', 0, 1),
            'reg_lambda': hp.uniform('reg_lambda', 0, 1),
            'learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
            'max_depth': hp.choice('max_depth', range(4, int(10 * math.log(xn)) + 1)),
            'n_estimators': hp.choice('n_estimators', range(xn, 100 * xn + 1)),
            'min_child_weight': hp.uniform('min_child_weight', 1, 10)
        }


def cls_params_space(algo_name: str, xn: int) -> dict:
    if algo_name == 'RandomForest':
        return {
            'max_depth': hp.choice('max_depth', range(5, 51)),
            'min_samples_split': hp.choice('min_samples_split', range(2, 21)),
            'min_samples_leaf': hp.choice('min_samples_leaf', range(1, 11)),
            'n_estimators': hp.choice('n_estimators', range(10 * xn, 100 * xn + 1))
        }

    elif algo_name == 'DecisionTree':
        return {
            'splitter': hp.choice('splitter', ['best']),
            'max_depth': hp.choice('max_depth', range(5, 51)),
            'min_samples_split': hp.choice('min_samples_split', range(2, 21)),
            'min_samples_leaf': hp.choice('min_samples_leaf', range(1, 11)),
            'max_leaf_nodes': hp.choice('max_leaf_nodes', range(10, 101))
        }

    elif algo_name == 'AdaBoost':
        return {
            'n_estimators': hp.choice('n_estimators', range(50 * xn, 200 * xn + 1)),
            'learning_rate': hp.uniform('learning_rate', 0.01, 1),
            'loss': hp.choice('loss', ['linear', 'square', 'exponential']),
            'base_estimator': hp.choice('base_estimator', [DecisionTreeClassifier(), SVC(), KNeighborsClassifier()])
        }

    elif algo_name == 'ExtraTree':
        return {
            'max_depth': hp.choice('max_depth', range(5, 51)),
            'min_samples_split': hp.choice('min_samples_split', range(2, 21)),
            'min_samples_leaf': hp.choice('min_samples_leaf', range(1, 11)),
            'n_estimators': hp.choice('n_estimators', range(50 * xn, 200 * xn))
        }

    elif algo_name == 'LightGBM':
        return {
            'reg_alpha': hp.uniform('reg_alpha', 0, 1),
            'reg_lambda': hp.uniform('reg_lambda', 0, 1),
            'learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
            'max_depth': hp.choice('max_depth', range(4, int(10 * math.log(xn)) + 1)),
            'min_child_samples': hp.choice('min_child_samples', range(1, 21)),
            'min_child_weight': hp.uniform('min_child_weight', 0, 10)
        }

    elif algo_name == 'CatBoost':
        return {
            'learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
            'iterations': hp.choice('iterations', [20]),
            'l2_leaf_reg': hp.uniform('l2_leaf_reg', 1, 11),
            'bagging_temperature': hp.uniform('bagging_temperature', 0.02, 1),
            'boosting_type': hp.choice('boosting_type', ['Ordered', 'Plain']),
            'depth': hp.choice('depth', range(4, int(10 * math.log(xn)) + 1)),
            'leaf_estimation_method': hp.choice('leaf_estimation_method', ['Newton', 'Gradient']),
            'random_strength': hp.choice('random_strength', range(1, 102)),
            'verbose': hp.choice('verbose', [False]),
            'allow_writing_files': hp.choice('allow_writing_files', [False])
        }

    elif algo_name == 'XgBoost':
        return {
            'reg_alpha': hp.uniform('reg_alpha', 0, 1),
            'reg_lambda': hp.uniform('reg_lambda', 0, 1),
            'learning_rate': hp.uniform('learning_rate', 0.01, 0.3),
            'max_depth': hp.choice('max_depth', range(4, int(10 * math.log(xn)) + 1)),
            'n_estimators': hp.choice('n_estimators', range(xn, 100 * xn + 1)),
            'min_child_weight': hp.uniform('min_child_weight', 1, 10)
        }
