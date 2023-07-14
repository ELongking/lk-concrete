import json
import os
import traceback
import time
import sys

import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from sklearn.utils import shuffle

from .PmmlConvert import AlgoConverter
from .PreProcess import *
from .CalcProcess import *
from .LogText import LoggerHandler


class PredictionThread(QThread):
    signal = pyqtSignal(str)
    bool_signal = pyqtSignal(bool)

    def __init__(
            self,
            df_path: str,
            data_config: dict,
            setting_config: dict,
            task_type: str,
            opt_path: str,
    ):
        super(PredictionThread, self).__init__()
        self.df_path = df_path
        self.data_config = data_config
        self.setting_config = setting_config
        self.opt_path = opt_path
        self.task_type = task_type
        self.pipeline = []
        self.logger = LoggerHandler(opt_path=opt_path,
                                    signal=self.signal)

        self.old_hook = sys.excepthook
        sys.excepthook = self._catch_error

    def _catch_error(self, ty, value, tb) -> None:
        traceback_format = traceback.format_exception(ty, value, tb)
        traceback_string = "".join(traceback_format)
        ans_signal = traceback_string
        self.logger.normal_browser_emit(ans_signal)
        self.quit()
        self.old_hook(ty, value, tb)

    def quit(self):
        self.bool_signal.emit(False)
        super().quit()

    def run(self) -> None:
        self.bool_signal.emit(True)

        self.logger.tab_browser_emit("准备工作开始...", step=1, level=1)
        task_name = osp.basename(self.df_path).split(".")[0]
        self.logger.init_logger(task_name=task_name)
        start_time = time.time()
        os.makedirs(self.opt_path, exist_ok=True)
        df = pd.read_excel(self.df_path)
        sup = dict()

        self.logger.tab_browser_emit("前处理步骤准备开始...", step=1, level=1)

        df, cats_encoder = hotpoint_first(df=df)
        sup["encoder"] = cats_encoder
        self.logger.tab_browser_emit("非数值类型转化完毕", step=1, level=2)

        df = default_value_convert(df=df, mode=self.setting_config["default"])
        self.logger.tab_browser_emit(f"缺省值处理完毕, 选择的方法为{self.setting_config['default']}", step=1, level=2)

        if self.setting_config["isAnomaly"]:
            df = anomaly_delete(df=df)
            self.logger.tab_browser_emit(f"异常值删除完毕", step=1, level=2)

        df = shuffle(df, random_state=42)
        xdf, ydf = xy_split(df=df, xcols=self.data_config["leftData"], ycols=self.data_config["rightData"])
        xdata, ydata = xdf.values, ydf.values

        xdata, scaler = data_normalization(xdata=xdata, mode=self.setting_config["normalize"])
        joblib.dump(scaler, osp.join(self.opt_path, "scaler.pkl"))
        self.pipeline.append(("scaler", scaler))
        self.logger.tab_browser_emit(f"数据标准化完毕, 选择的方法为{self.setting_config['normalize']}", step=1, level=2)

        algo_dict, algo_dict_optimize, params_space = filter_algo_dicts(algos=self.setting_config["algos"],
                                                                        mode=self.task_type)
        self.logger.tab_browser_emit(f"前处理步骤完毕", step=1, level=1)

        train_x, train_y, valid_x, valid_y, test_x, test_y = train_test_split(xdata=xdata, ydata=ydata)
        for idx, target in enumerate(self.data_config["rightData"]):
            self.logger.tab_browser_emit(f"预测模型构建步骤准备开始, 现在的目标值: {target}", step=2, level=1)
            tr_y, vl_y, te_y = train_y[:, idx], valid_y[:, idx], test_y[:, idx]

            models, res = algo_filter(ad=algo_dict,
                                      task_type=self.task_type,
                                      train_x=train_x,
                                      train_y=tr_y,
                                      valid_x=valid_x,
                                      valid_y=vl_y,
                                      test_x=test_x,
                                      test_y=te_y,
                                      lh=self.logger)
            if res[-1] < 0.6:
                self.logger.tab_browser_emit(text="模型表现较差, 即数据间相关性较低, 无法得到具有可靠性的模型, 因此流程直接中止。",
                                             step=2,
                                             level=2)
                return
            save_model(model=res[1], model_name=res[0], opt_path=self.opt_path, desc=[target, "filter"])
            if self.setting_config["inferIndex"] == 0:
                self.pipeline.append((res[0], res[1]))

            if self.setting_config["isOptimized"]:
                best_models = hyperparams_extract(models=models,
                                                  ado=algo_dict_optimize,
                                                  params_space=params_space,
                                                  train_x=train_x,
                                                  train_y=tr_y,
                                                  valid_x=valid_x,
                                                  valid_y=vl_y,
                                                  lh=self.logger)
                best_score = float("-inf")
                res = None
                for name, algo in best_models.items():
                    algo.fit(train_x, tr_y)
                    score = r2_score(te_y.ravel(), algo.predict(test_x))
                    if score > best_score:
                        best_score = score
                        res = (name, algo, best_score)
                self.logger.tab_browser_emit(text=f"参数优化步骤得到最好效果的模型为: {res[0]}, 测试集得分为: {res[-1]}", step=2, level=3)

                if res[-1] < 0.6:
                    self.logger.tab_browser_emit(text="模型表现较差, 即数据间相关性较低, 无法得到具有可靠性的模型, 因此流程直接中止。",
                                                 step=2,
                                                 level=2)
                    return

                save_model(model=res[1],
                           model_name=res[0],
                           opt_path=self.opt_path,
                           desc=[target, "base", "optimized"])
                if self.setting_config["inferIndex"] == 1:
                    self.pipeline.append((res[0], res[1]))

            if self.setting_config["isVarSelected"]:
                importance_weight = get_variable_importance(model=res[1],
                                                            name=res[0])
                res = variable_selected(model_name=res[0],
                                        imp=importance_weight,
                                        xcols=self.data_config["leftData"],
                                        relationship=self.data_config["relData"],
                                        train_x=train_x,
                                        train_y=tr_y,
                                        valid_x=valid_x,
                                        valid_y=vl_y,
                                        test_x=test_x,
                                        test_y=te_y,
                                        ado=algo_dict_optimize,
                                        params_space=params_space,
                                        lh=self.logger)
                if res[-1] < 0.6:
                    self.logger.tab_browser_emit(text="模型表现较差, 即数据间相关性较低, 无法得到具有可靠性的模型, 因此流程直接中止。",
                                                 step=2,
                                                 level=2)
                    return
                save_model(model=res[1],
                           model_name=res[0],
                           opt_path=self.opt_path,
                           desc=[target, "deep", "optimized"])
                if self.setting_config["inferIndex"] == 2:
                    sup["selected_vars"] = res[-1]
                    self.pipeline.append((res[0], res[1]))

            if self.setting_config["isAutoImported"]:
                self.logger.tab_browser_emit("AutoML方法进行中, 最长运行时间5分钟", step=3, level=1)
                score = auto_prediction(train_x=train_x,
                                        train_y=tr_y,
                                        valid_x=valid_x,
                                        valid_y=vl_y,
                                        test_x=test_x,
                                        test_y=te_y,
                                        label=target,
                                        xcols=self.data_config["leftData"],
                                        task_type=self.task_type,
                                        opt_path="./temp", )
                self.logger.tab_browser_emit(f"AutoML方法模型验证集得分为: {score}", step=3, level=1)

        converter = AlgoConverter()
        converter.add_element(pipeline=self.pipeline)
        converter.export(path=osp.join(self.opt_path, "infer"))

        f = open(osp.join(self.opt_path, task_name + '-support.json'), "w", encoding="utf-8")
        json.dump(sup, f)
        f.close()

        end_time = time.time()
        self.logger.normal_browser_emit(
            text="-" * 10 + f" 流程完毕, 总共时间消耗为: {round(end_time - start_time, 3)}min " + "-" * 10)
        self.quit()
