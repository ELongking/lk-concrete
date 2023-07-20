import os.path as osp

from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

from src.tabular.Prediction import PredictionThread


def reformat_tool_info(f: list) -> str:
    res = ""
    if f:
        for index, item in enumerate(f):
            if index == 0:
                res += item[0]
            res += f"{item[0]} -> {item[1]}, {item[2]}M\n"
    return res


class IPreProcessWidget(QWidget):
    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.name = "IPreProcessWidget"
        self._init_widget()

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
        hotpoint_label = QLabel("类别编码方法 -> ")
        h_layout_3.addWidget(hotpoint_label)
        _all_encoders = ["CatBoost", "Helmert", "JamesStein", "LeaveOneOut",
                         "MEstimate", "Ordinal", "Sum", "Target",
                         "WOE"]
        self.encoder_method_combox = QComboBox()
        self.encoder_method_combox.addItems(_all_encoders)
        h_layout_3.addWidget(self.encoder_method_combox)

        h_layout_4 = QHBoxLayout()
        self.ano_check_btn = QRadioButton("异常值舍弃")
        h_layout_4.addWidget(self.ano_check_btn)

        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        v_layout.addLayout(h_layout_3)
        v_layout.addLayout(h_layout_4)
        v_layout.setSpacing(30)

        self.setLayout(v_layout)

    def export(self) -> dict:
        _default_value_convert = {"填充0": "zero", "填充均值": "mean", "删除整行": "delete"}
        _normal_method_convert = {"0~1分布": "minmax", "-1~1分布": "maxabs", "正态分布": "standard"}
        return {
            "default": _default_value_convert[self.default_btn_group.checkedButton().text()],
            "normalize": _normal_method_convert[self.normal_btn_group.checkedButton().text()],
            "cats_encoder": self.encoder_method_combox.currentText(),
            "isAnomaly": self.ano_check_btn.isChecked()
        }


class IAlgoSelectWidget(QWidget):
    def __init__(self, index: int, task_type: str):
        super().__init__()
        self.index = index
        self.task_type = task_type
        self.name = "IAlgoSelectWidget"
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()

        cls_algo = [
            {
                "name": "ResNet",
                "size": [18, 34, 50, 101, 152],
                "info": [
                    ["四个Layer内的Block数目和种类"],
                    [18, "2,2,2,2 ResBlock", 11.176],
                    [34, "3,4,6,3 ResBlock", 21.286],
                    [50, "3,4,6,3 BottleNeckBlock", 23.512],
                    [101, "3,4,23,3 BottleNeckBlock", 42.504],
                    [152, "3,8,36,3 BottleNeckBlock", 58.148]
                ]
            },
            {
                "name": "ShuffleNet",
                "size": [0.5, 1.0, 1.5, 2.0],
                "info": [
                    ["FeatureBlock 输出通道"],
                    [0.5, "24,48,96,192,1024", 0.344],
                    [1.0, "24,116,232,464,1024", 1.257],
                    [1.5, "24,176,352,704,1024", 2.485],
                    [2.0, "24,244,488,976,2048", 5.359]
                ]
            },
            {
                "name": "EfficientNet",
                "size": ["s", "m", "l", "xl"],
                "info": [
                    ["MBConvBlock 输出通道"],
                    ["s", "24,48,64,128,160,256", 20.314],
                    ["m", "24,48,80,160,176,304,512", 53.511],
                    ["l", "32,64,96,192,224,384,640", 117.566],
                    ["xl", "32,64,96,192,256,512,640", 207.171]
                ]
            },
            {
                "name": "MobileNet",
                "size": ["small", "large"],
                "info": [
                    ["InvertedResidual 输出通道"],
                    ["small", "16,24*2,40*3,48*2,96*2", 1.52],
                    ["large", "16,24*2,40*3,80*4,112*2,160*3", 4.205]
                ]
            },
            {
                "name": "VisionTransformer",
                "size": ["tiny", "small", "base", "large"],
                "info": [
                    ["维度,深度,多头数目,ffw通道数"],
                    ["tiny", "192,12,3,768", 5.482],
                    ["small", "384,12,6,1536", 21.579],
                    ["base", "768,12,12,3072", 85.624],
                    ["large", "1024,24,16,4096", 303.031]
                ]
            }]
        det_algo = [
            {
                "name": "FasterRCNN",
                "size": [1, 2, 3],
                "info": []
            },
            {
                "name": "YoloX",
                "size": ["nano", "tiny", "small", "medium"],
                "info": []
            },
            {
                "name": "EfficientDet",
                "size": [1, 2, 3],
                "info": []
            }
        ]
        seg_algo = [{"name": "MaskRCNN", "size": [1, 2, 3]}, {"name": "SoloV2", "size": [1, 2, 3]}]

        if self.task_type == "cls":
            all_algo = cls_algo
        elif self.task_type == "det":
            all_algo = det_algo
        else:
            all_algo = seg_algo

        algo_radio_group = QButtonGroup()
        for algo in all_algo:
            ans_h_layout = QHBoxLayout()
            ans_radio_btn = QRadioButton(algo["name"])
            algo_radio_group.addButton(ans_radio_btn)
            ans_label = QLabel("模型大小", self)
            ans_size_combox = QComboBox()
            ans_size_combox.addItems(algo["size"])
            ans_tool_label = QLabel(self)
            ans_tool_label.setPixmap(QPixmap("../assets/info.png").scaledToWidth(30))
            ans_tool_label.setToolTip(reformat_tool_info(f=algo["info"]))

            ans_h_layout.addWidget(ans_label)
            ans_h_layout.addWidget(ans_size_combox)
            ans_h_layout.addWidget(ans_tool_label)


    def export(self) -> dict:
        checked_btns = self.algo_btn_group.buttons()
        return {"algos": [button.text() for button in checked_btns if button.isChecked()]}


class TSettingWidget(QWidget):
    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.name = "TSettingWidget"
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        self.setting_btn_group = QButtonGroup(self)
        self.setting_btn_group.setExclusive(False)
        self.pmml_box = QComboBox(self)
        self.pmml_box.addItem("1. 初步筛选结果")
        all_setting = ["算法参数优化", "特征值二次选择", "引入AutoML方法"]

        for index, title in enumerate(all_setting):
            ans_check_btn = QCheckBox(title)
            ans_check_btn.toggled.connect(lambda checked, idx=index: self.button_state_changed(idx))
            self.setting_btn_group.addButton(ans_check_btn)
            grid_layout.addWidget(ans_check_btn, index // 3, index % 3)

        grid_layout.addWidget(QLabel("推理模式: "), 1, 0)
        grid_layout.addWidget(self.pmml_box, 1, 1, 1, 2)

        v_layout.addLayout(grid_layout)
        self.setLayout(v_layout)

    def button_state_changed(self, idx) -> None:
        btn = self.setting_btn_group.buttons()[idx]
        if idx == 2:
            pass
        elif idx == 1:
            text = "3. 特征选择后结果(特征数会比之前少, 请注意查看)"
            if btn.isChecked():
                self.pmml_box.addItem(text)
            else:
                if self.pmml_box.findText(text) == -1:
                    pass
                else:
                    self.pmml_box.removeItem(self.pmml_box.findText(text))
        else:
            text = "2. 参数优化后结果"
            if btn.isChecked():
                self.pmml_box.addItem(text)
            else:
                if self.pmml_box.findText(text) == -1:
                    pass
                else:
                    self.pmml_box.removeItem(self.pmml_box.findText(text))

    def export(self) -> dict:
        return {
            "isOptimized": self.setting_btn_group.buttons()[0].isChecked(),
            "isVarSelected": self.setting_btn_group.buttons()[1].isChecked(),
            "isAutoImported": self.setting_btn_group.buttons()[2].isChecked(),
            "inferIndex": int(self.pmml_box.currentText()[0]) - 1
        }


class TStartExportWidget(QWidget):

    def __init__(self, index: int, case_path: str, task_type: str):
        super().__init__()
        self.index = index
        self.name = "TStartExportWidget"
        self.case_path = case_path
        self.task_type = task_type
        self.setting_config = {}
        self.data_config = {}
        self.thread: PredictionThread

        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        self.logging_text = QTextBrowser()
        v_layout_1 = QVBoxLayout()
        start_btn = QPushButton("开始训练")
        start_btn.clicked.connect(self.run)
        self.stop_btn = QPushButton("中止训练")
        self.stop_btn.clicked.connect(self.stop)
        self.stop_btn.setEnabled(False)
        open_opt_btn = QPushButton("打开输出文件夹")
        open_opt_btn.clicked.connect(self._check_opt_dir)
        v_layout_1.addWidget(start_btn)
        v_layout_1.addWidget(self.stop_btn)
        v_layout_1.addWidget(open_opt_btn)
        h_layout.addWidget(self.logging_text)
        h_layout.addLayout(v_layout_1)

        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)

    def import_widgets(self, widgets: list, data_config: dict):
        self.widgets = widgets
        self.data_config = data_config

    def run(self) -> None:
        self.setting_config = {}
        for widget in self.widgets:
            self.setting_config.update(widget.export())

        df_path = osp.join(self.case_path, self.data_config["fileName"])
        self.thread = PredictionThread(setting_config=self.setting_config,
                                       data_config=self.data_config,
                                       task_type=self.task_type,
                                       df_path=df_path,
                                       opt_path=osp.join(self.case_path, "output"))
        self.thread.signal.connect(self._log_text_show)
        self.thread.bool_signal.connect(self._stop_enabled_changed)

        self.thread.start()

    def stop(self) -> None:
        self.thread.quit()

    def _log_text_show(self, txt: str) -> None:
        self.logging_text.append(txt)

    def _check_opt_dir(self) -> None:
        command = f"explorer {self.case_path}"
        process = QProcess(self)
        process.startDetached(command)

    def _stop_enabled_changed(self, flag: bool) -> None:
        self.stop_btn.setEnabled(flag)
