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


def process_component(component):
    res = ""
    if isinstance(component, QLineEdit):
        res = component.text()
    if isinstance(component, QRadioButton):
        res = component.isChecked()
    return res


class IPreProcessWidget(QWidget):
    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.name = "IPreProcessWidget"
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()
        v_layout.addWidget(QLabel("数据增强方法"))

        v_layout_1 = QVBoxLayout()
        h_layout_v1_1 = QHBoxLayout()
        mean_aug_label = QLabel("Mean & Std")
        mean_aug_check = QCheckBox()
        mean_aug_check.setChecked(True)
        mean_aug_check.setEnabled(False)
        mean_aug_text = QLineEdit("mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]")
        mean_aug_text.setEnabled(False)
        h_layout_v1_1.addWidget(mean_aug_check)
        h_layout_v1_1.addWidget(mean_aug_label)
        h_layout_v1_1.addWidget(mean_aug_text)
        v_layout_1.addLayout(h_layout_v1_1)

        h_layout_v1_2 = QHBoxLayout()
        resize_aug_label = QLabel("Resize")
        resize_aug_check = QCheckBox()
        resize_aug_check.setChecked(True)
        resize_aug_check.setEnabled(False)
        resize_aug_text = QLineEdit("256")
        resize_aug_text.setEnabled(False)
        h_layout_v1_2.addWidget(resize_aug_check)
        h_layout_v1_2.addWidget(resize_aug_label)
        h_layout_v1_2.addWidget(resize_aug_text)
        v_layout_1.addLayout(h_layout_v1_2)

        h_layout_v1_3 = QHBoxLayout()
        crop_aug_label = QLabel("RandomCrop")
        crop_aug_check = QCheckBox()
        self.crop_aug_text = QLineEdit("224")
        self.crop_aug_text.setPlaceholderText("Cannot larger than 256")
        h_layout_v1_3.addWidget(crop_aug_check)
        h_layout_v1_3.addWidget(crop_aug_label)
        h_layout_v1_3.addWidget(self.crop_aug_text)
        v_layout_1.addLayout(h_layout_v1_3)

        h_layout_v1_4 = QHBoxLayout()
        rana_aug_label = QLabel("RandomAug")
        rana_aug_check = QCheckBox()
        self.rana_aug_text = QLineEdit("2,6")
        self.rana_aug_text.setPlaceholderText("Format: n(the number of transforms),m(the number of sub-strategies")
        h_layout_v1_4.addWidget(rana_aug_check)
        h_layout_v1_4.addWidget(rana_aug_label)
        h_layout_v1_4.addWidget(self.rana_aug_text)
        v_layout_1.addLayout(h_layout_v1_4)

        h_layout_v1_5 = QHBoxLayout()
        cutmix_aug_label = QLabel("CutMix")
        cutmix_aug_check = QCheckBox()
        self.cutmix_aug_text = QLineEdit("0.6")
        self.cutmix_aug_text.setPlaceholderText("0-1, means mix-part ratio to ori image")
        h_layout_v1_5.addWidget(cutmix_aug_check)
        h_layout_v1_5.addWidget(cutmix_aug_label)
        h_layout_v1_5.addWidget(self.cutmix_aug_text)
        v_layout_1.addLayout(h_layout_v1_5)

        h_layout_v1_6 = QHBoxLayout()
        mixup_aug_label = QLabel("MixUp")
        mixup_aug_check = QCheckBox()
        self.mixup_aug_text = QLineEdit("0.6")
        self.mixup_aug_text.setPlaceholderText("0-1, means mix-part ratio to ori image")
        h_layout_v1_6.addWidget(mixup_aug_check)
        h_layout_v1_6.addWidget(mixup_aug_label)
        h_layout_v1_6.addWidget(self.mixup_aug_text)
        v_layout_1.addLayout(h_layout_v1_6)

        self.aug_check_group = QButtonGroup()
        self.aug_check_group.addButton(mean_aug_check)
        self.aug_check_group.addButton(resize_aug_check)
        self.aug_check_group.addButton(crop_aug_check)
        self.aug_check_group.addButton(rana_aug_check)
        self.aug_check_group.addButton(cutmix_aug_check)
        self.aug_check_group.addButton(mixup_aug_check)
        self.aug_check_group.setExclusive(False)

        v_layout.addLayout(v_layout_1)
        self.setLayout(v_layout)

    def export(self) -> dict:
        res = {"aug": []}
        for idx, btn in enumerate(self.aug_check_group.buttons()):
            if not btn.isChecked():
                continue

            if idx == 0 and idx == 1:
                pass
            elif idx == 2:
                res["aug"].append(["crop", self.crop_aug_text.text()])
            elif idx == 3:
                res["aug"].append(["randaug", self.rana_aug_text.text()])
            elif idx == 4:
                res["aug"].append(["cutmix", self.cutmix_aug_text.text()])
            elif idx == 5:
                res["aug"].append(["mixup", self.mixup_aug_text.text()])
            else:
                raise ValueError(f"No Value can be {idx}")

        return res


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

        self.all_algo = all_algo
        self.algo_radio_group = QButtonGroup()
        self.algo_size_comboxes = []
        for idx, algo in enumerate(all_algo):
            ans_h_layout = QHBoxLayout()
            ans_radio_btn = QRadioButton(algo["name"])
            if idx == 0:
                ans_radio_btn.setChecked(True)
            self.algo_radio_group.addButton(ans_radio_btn)
            ans_label = QLabel("模型大小", self)
            ans_size_combox = QComboBox()
            ans_size_combox.addItems(algo["size"])
            self.algo_size_comboxes.append(ans_size_combox)
            ans_tool_label = QLabel(self)
            ans_tool_label.setPixmap(QPixmap("../assets/info.png").scaledToWidth(30))
            ans_tool_label.setToolTip(reformat_tool_info(f=algo["info"]))

            ans_h_layout.addWidget(ans_label)
            ans_h_layout.addWidget(ans_size_combox)
            ans_h_layout.addWidget(ans_tool_label)

    def export(self) -> dict:
        for idx, btn in enumerate(self.algo_radio_group.buttons()):
            if btn.isChecked():
                return {"algos": [self.all_algo[idx]["name"], self.algo_size_comboxes[idx].currentText()]}


class ISettingWidget(QWidget):
    def __init__(self, index: int):
        super().__init__()
        self.index = index
        self.name = "ISettingWidget"
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()

        v_layout_1 = QVBoxLayout()
        h_layout_v1_1 = QHBoxLayout()
        opti_label = QLabel("优化器:")
        self.opti_select_combox = QComboBox()
        self.opti_select_combox.addItems(["SGD", "Adam", "AdamW"])
        self.opti_select_combox.currentIndexChanged.connect(self._opti_changed)
        h_layout_v1_1.addWidget(opti_label)
        h_layout_v1_1.addWidget(self.opti_select_combox)
        self._opti_setting_layout = QHBoxLayout()
        v_layout_1.addLayout(h_layout_v1_1)
        v_layout_1.addLayout(self._opti_setting_layout)

        v_layout_2 = QVBoxLayout()
        h_layout_v2_1 = QHBoxLayout()
        loss_label = QLabel("损失函数")
        self.loss_select_combox = QComboBox()
        self.loss_select_combox.addItems(["CrossEntropy",
                                          "LabelSmoothingCrossEntropy",
                                          "Focal", ])
        self.loss_select_combox.currentIndexChanged.connect(self._loss_changed)
        h_layout_v2_1.addWidget(opti_label)
        h_layout_v2_1.addWidget(self.opti_select_combox)
        self._loss_setting_layout = QHBoxLayout()
        v_layout_2.addLayout(h_layout_v2_1)
        v_layout_2.addLayout(self._loss_setting_layout)

        v_layout.addLayout(v_layout_1)
        v_layout.addLayout(v_layout_2)
        self.setLayout(v_layout)

    def _opti_changed(self, index):
        while self._opti_setting_layout.count():
            child = self._opti_setting_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        if index == 0:
            learning_rate_label = QLabel("学习率")
            learning_rate_text = QLineEdit("1e-3")
            momentum_label = QLabel("动量")
            momentum_text = QLineEdit("0.95")

            self._opti_setting_layout.addWidget(learning_rate_label)
            self._opti_setting_layout.addWidget(learning_rate_text)
            self._opti_setting_layout.addWidget(momentum_label)
            self._opti_setting_layout.addWidget(momentum_text)

        elif index == 1:
            learning_rate_label = QLabel("学习率")
            learning_rate_text = QLineEdit("1e-3")
            beta1_label = QLabel("一阶矩估计指数衰减率")
            beta1_text = QLineEdit("0.9")
            beta2_label = QLabel("二阶矩估计指数衰减率")
            beta2_text = QLineEdit("0.999")

            self._opti_setting_layout.addWidget(learning_rate_label)
            self._opti_setting_layout.addWidget(learning_rate_text)
            self._opti_setting_layout.addWidget(beta1_label)
            self._opti_setting_layout.addWidget(beta1_text)
            self._opti_setting_layout.addWidget(beta2_label)
            self._opti_setting_layout.addWidget(beta2_text)

        elif index == 2:
            learning_rate_label = QLabel("学习率")
            learning_rate_text = QLineEdit("1e-3")
            beta1_label = QLabel("一阶矩估计指数衰减率")
            beta1_text = QLineEdit("0.9")
            beta2_label = QLabel("二阶矩估计指数衰减率")
            beta2_text = QLineEdit("0.999")
            weight_decay_label = QLabel("权重衰减")
            weight_decay_text = QLineEdit("0.1")

            self._opti_setting_layout.addWidget(learning_rate_label)
            self._opti_setting_layout.addWidget(learning_rate_text)
            self._opti_setting_layout.addWidget(beta1_label)
            self._opti_setting_layout.addWidget(beta1_text)
            self._opti_setting_layout.addWidget(beta2_label)
            self._opti_setting_layout.addWidget(beta2_text)
            self._opti_setting_layout.addWidget(weight_decay_label)
            self._opti_setting_layout.addWidget(weight_decay_text)

    def _loss_changed(self, index):
        while self._loss_setting_layout.count():
            child = self._loss_setting_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        if index == 0:
            pass
        elif index == 1:
            smooth_label = QLabel("平滑度")
            smooth_text = QLineEdit("0.2")
            self._loss_setting_layout.addWidget(smooth_label)
            self._loss_setting_layout.addWidget(smooth_text)
        elif index == 2:
            alpha_label = QLabel("正负样本权重(α)")
            alpha_text = QLineEdit("0.5")
            gamma_label = QLabel("难易样本权重(γ)")
            gamma_text = QLineEdit("2")
            self._loss_setting_layout.addWidget(alpha_label)
            self._loss_setting_layout.addWidget(alpha_text)
            self._loss_setting_layout.addWidget(gamma_label)
            self._loss_setting_layout.addWidget(gamma_text)

    def export(self) -> dict:
        res = {"optimizer": [], "loss": [], "epoch": 10}

        res["optimizer"].append(self.opti_select_combox.currentText())
        for i in range(self._opti_setting_layout.count()):
            item = self._opti_setting_layout.itemAt(i)
            if item.widget():
                res["optimizer"].append(process_component(item.widget()))

        res["loss"].append(self.loss_select_combox.currentText())
        for i in range(self._loss_setting_layout.count()):
            item = self._loss_setting_layout.itemAt(i)
            if item.widget():
                res["loss"].append(process_component(item.widget()))
        return res


class IStartExportWidget(QWidget):

    def __init__(self, index: int, case_path: str, task_type: str):
        super().__init__()
        self.index = index
        self.name = "IStartExportWidget"
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
