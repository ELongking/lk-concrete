from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import *


class TPreProcessWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_widget()
        self.name = "TPreProcessWidget"

    def _init_widget(self):
        v_layout = QVBoxLayout()

        h_layout_1 = QHBoxLayout()
        default_label = QLabel("缺省值填充 -> ")
        h_layout_1.addWidget(default_label)
        self.default_btn_group = QButtonGroup(self)
        for index, title in enumerate(["填充0", "填充均值", "删除整行"]):
            ans_radio_btn = QRadioButton(title, self)
            self.default_btn_group.addButton(ans_radio_btn)
            h_layout_1.addWidget(ans_radio_btn)
        self.default_btn_group.buttons()[0].setChecked(True)

        h_layout_2 = QHBoxLayout()
        normal_label = QLabel("标准化方法 -> ")
        h_layout_2.addWidget(normal_label)
        self.normal_btn_group = QButtonGroup(self)
        for index, title in enumerate(["0~1分布", "-1~1分布", "正态分布"]):
            ans_radio_btn = QRadioButton(title, self)
            self.normal_btn_group.addButton(ans_radio_btn)
            h_layout_2.addWidget(ans_radio_btn)
        self.normal_btn_group.buttons()[0].setChecked(True)

        h_layout_3 = QHBoxLayout()
        self.ano_check_btn = QRadioButton("异常值舍弃")
        h_layout_3.addWidget(self.ano_check_btn)

        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        v_layout.addLayout(h_layout_3)
        v_layout.setSpacing(30)

        self.setLayout(v_layout)

    def export(self) -> dict:
        _default_value_convert = {"填充0": "zero", "填充均值": "mean", "删除整行": "delete"}
        _normal_method_convert = {"0~1分布": "minmax", "-1~1分布": "maxabs", "正态分布": "standard"}
        return {
            "default": _default_value_convert[self.default_btn_group.checkedButton().text()],
            "normalize": _normal_method_convert[self.normal_btn_group.checkedButton().text()],
            "isAnomaly": self.ano_check_btn.isChecked()
        }


class TAlgoSelectWidget(QWidget):
    def __init__(self, task_type):
        super().__init__()
        self.task_type = task_type
        self.name = "TAlgoSelectWidget"
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()

        reg_algo = ["ElasticNet", "Lasso", "Ridge", "RandomForest", "DecisionTree",
                    "AdaBoost", "ExtraTree", "LightGBM", "XgBoost", "CatBoost"]
        cls_algo = ["RandomForest", "DecisionTree",
                    "AdaBoost", "ExtraTree", "LightGBM", "XgBoost", "CatBoost"]

        all_algo = reg_algo if self.task_type == "reg" else cls_algo

        algo_layout = QGridLayout()
        self.algo_btn_group = QButtonGroup(self)
        self.algo_btn_group.setExclusive(False)
        for index, title in enumerate(all_algo):
            ans_check_btn = QCheckBox(title)
            self.algo_btn_group.addButton(ans_check_btn)
            algo_layout.addWidget(ans_check_btn, index // 3, index % 3)

        v_layout.addLayout(algo_layout)
        self.setLayout(v_layout)

    def export(self) -> dict:
        checked_btns = self.algo_btn_group.checkedButtons()
        return {"algos": [button.text() for button in checked_btns]}


class TSettingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.name = "TSettingWidget"
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        self.setting_btn_group = QButtonGroup(self)
        self.setting_btn_group.setExclusive(False)
        all_setting = ["算法参数优化", "特征值二次选择", "引入AutoML方法"]
        for index, title in enumerate(all_setting):
            ans_check_btn = QCheckBox(title)
            self.setting_btn_group.addButton(ans_check_btn)
            grid_layout.addWidget(ans_check_btn, index // 3, index % 3)

        v_layout.addLayout(grid_layout)
        self.setLayout(v_layout)

    def export(self) -> dict:
        return {
            "isOptimized": self.setting_btn_group.buttons()[0].isChecked(),
            "isVarSelected": self.setting_btn_group.buttons()[1].isChecked(),
            "isAutoImported": self.setting_btn_group.buttons()[2].isChecked()
        }


class TStartExportWidget(QWidget):
    def __init__(self, case_path):
        super().__init__()
        self.name = "TStartExportWidget"
        self.case_path = case_path
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        self.logging_text = QTextBrowser()
        v_layout_1 = QVBoxLayout()
        start_btn = QPushButton("开始训练")
        start_btn.clicked.connect(lambda: self.run)
        open_opt_btn = QPushButton("打开输出文件夹")
        open_opt_btn.clicked.connect(self._check_opt_dir)
        v_layout_1.addWidget(start_btn)
        v_layout_1.addWidget(open_opt_btn)
        h_layout.addWidget(self.logging_text)
        h_layout.addLayout(v_layout_1)

        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

    def run(self, setting: dict) -> None:
        pass

    def _log_text_show(self, txt: str, add: str = "\n") -> None:
        text = txt + add
        self.logging_text.append(text)

    def _check_opt_dir(self):
        command = f"explorer {self.case_path}"
        process = QProcess(self)
        process.startDetached(command)
