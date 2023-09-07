import os.path as osp

from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from src.component.TinyTools import InfoLabel, LkItem
from src.tabular.Prediction import PredictionThread


def reformat_tool_info(f: list) -> str:
    res = ""
    if f:
        for index, item in enumerate(f):
            if index == 0:
                res += item[0] + "\n"
            else:
                res += f"{item[0]} -> {item[1]}, {item[2]}M\n"
    res = res[:-1]
    return res


def clear_layout(layout: QLayout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clear_layout(child.layout())


def process_component(component):
    res = None
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
        ans_tool_label = InfoLabel("图片色彩标准化的均值和方差")
        h_layout_v1_1.addWidget(mean_aug_check)
        h_layout_v1_1.addWidget(mean_aug_label)
        h_layout_v1_1.addWidget(mean_aug_text)
        h_layout_v1_1.addWidget(ans_tool_label)
        v_layout_1.addLayout(h_layout_v1_1)

        h_layout_v1_2 = QHBoxLayout()
        resize_aug_label = QLabel("Resize")
        resize_aug_check = QCheckBox()
        resize_aug_check.setChecked(True)
        resize_aug_check.setEnabled(False)
        resize_aug_text = QLineEdit("256")
        resize_aug_text.setEnabled(False)
        ans_tool_label = InfoLabel("Resize images")
        h_layout_v1_2.addWidget(resize_aug_check)
        h_layout_v1_2.addWidget(resize_aug_label)
        h_layout_v1_2.addWidget(resize_aug_text)
        h_layout_v1_2.addWidget(ans_tool_label)
        v_layout_1.addLayout(h_layout_v1_2)

        h_layout_v1_3 = QHBoxLayout()
        crop_aug_label = QLabel("RandomCrop")
        crop_aug_check = QCheckBox()
        self.crop_aug_text = QLineEdit("224")
        ans_tool_label = InfoLabel("图片裁剪的尺寸, 不能大于256")
        h_layout_v1_3.addWidget(crop_aug_check)
        h_layout_v1_3.addWidget(crop_aug_label)
        h_layout_v1_3.addWidget(self.crop_aug_text)
        h_layout_v1_3.addWidget(ans_tool_label)
        v_layout_1.addLayout(h_layout_v1_3)

        h_layout_v1_4 = QHBoxLayout()
        rana_aug_label = QLabel("RandomAug")
        rana_aug_check = QCheckBox()
        self.rana_aug_text = QLineEdit("2,6")
        ans_tool_label = InfoLabel("Format: n(the number of transforms),m(the number of sub-strategies")
        h_layout_v1_4.addWidget(rana_aug_check)
        h_layout_v1_4.addWidget(rana_aug_label)
        h_layout_v1_4.addWidget(self.rana_aug_text)
        h_layout_v1_4.addWidget(ans_tool_label)
        v_layout_1.addLayout(h_layout_v1_4)

        h_layout_v1_5 = QHBoxLayout()
        cutmix_aug_label = QLabel("CutMix")
        cutmix_aug_check = QCheckBox()
        self.cutmix_aug_text = QLineEdit("0.6")
        ans_tool_label = InfoLabel("0到1, 图片融合的比例")
        h_layout_v1_5.addWidget(cutmix_aug_check)
        h_layout_v1_5.addWidget(cutmix_aug_label)
        h_layout_v1_5.addWidget(self.cutmix_aug_text)
        h_layout_v1_5.addWidget(ans_tool_label)
        v_layout_1.addLayout(h_layout_v1_5)

        h_layout_v1_6 = QHBoxLayout()
        mixup_aug_label = QLabel("MixUp")
        mixup_aug_check = QCheckBox()
        self.mixup_aug_text = QLineEdit("0.6")
        ans_tool_label = InfoLabel("0到1, 图片融合的比例")
        h_layout_v1_6.addWidget(mixup_aug_check)
        h_layout_v1_6.addWidget(mixup_aug_label)
        h_layout_v1_6.addWidget(self.mixup_aug_text)
        h_layout_v1_6.addWidget(ans_tool_label)
        v_layout_1.addLayout(h_layout_v1_6)

        self.aug_check_group = []
        self.aug_check_group.append(mean_aug_check)
        self.aug_check_group.append(resize_aug_check)
        self.aug_check_group.append(crop_aug_check)
        self.aug_check_group.append(rana_aug_check)
        self.aug_check_group.append(cutmix_aug_check)
        self.aug_check_group.append(mixup_aug_check)

        v_layout.addLayout(v_layout_1)
        self.setLayout(v_layout)

    def export(self) -> dict:
        res = {"aug": []}
        for idx, btn in enumerate(self.aug_check_group):
            if not btn.isChecked():
                continue
            if idx == 0 or idx == 1:
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
                "size": ["18", "34", "50", "101", "152"],
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
                "size": ["0.5", "1.0", "1.5", "2.0"],
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
                "size": ["1", "2", "3"],
                "info": []
            },
            {
                "name": "YoloX",
                "size": ["nano", "tiny", "small", "medium"],
                "info": []
            },
            {
                "name": "EfficientDet",
                "size": ["1", "2", "3"],
                "info": []
            }
        ]
        seg_algo = [{"name": "MaskRCNN", "size": ["1", "2", "3"]}, {"name": "SoloV2", "size": ["1", "2", "3"]}]

        if self.task_type == "cls":
            all_algo = cls_algo
        elif self.task_type == "det":
            all_algo = det_algo
        else:
            all_algo = seg_algo

        self.all_algo = all_algo
        self.algo_radio_group = QButtonGroup()
        self.algo_radio_group.buttonClicked.connect(self._algo_changed)
        self.algo_size_comboxes = []
        for idx, algo in enumerate(all_algo):
            ans_h_layout = QHBoxLayout()
            ans_radio_btn = QRadioButton(algo["name"])
            if idx == 0:
                ans_radio_btn.setChecked(True)
            self.algo_radio_group.addButton(ans_radio_btn, idx)
            ans_label = QLabel("模型大小", self)
            ans_size_combox = QComboBox()
            ans_size_combox.addItems(algo["size"])
            self.algo_size_comboxes.append(ans_size_combox)
            ans_tool_label = InfoLabel(reformat_tool_info(f=algo["info"]))

            ans_h_layout.addWidget(ans_radio_btn)
            ans_h_layout.addWidget(ans_label)
            ans_h_layout.addWidget(ans_size_combox)
            ans_h_layout.addWidget(ans_tool_label)
            v_layout.addLayout(ans_h_layout)

        self._algo_changed(self.algo_radio_group.buttons()[0])
        self.setLayout(v_layout)

    def _algo_changed(self, btn):
        idx = self.algo_radio_group.id(btn)
        for i in range(len(self.algo_size_comboxes)):
            if i != idx:
                self.algo_size_comboxes[i].setEnabled(False)
            else:
                self.algo_size_comboxes[i].setEnabled(True)

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
        opti_select_combox = QComboBox()
        opti_select_combox.addItems(["SGD", "Adam", "AdamW"])
        opti_select_combox.currentIndexChanged.connect(self._opti_changed)
        self.opti_select_item = LkItem(label_txt="优化器", key="optimizer", main=opti_select_combox)
        h_layout_v1_1.addWidget(self.opti_select_item)
        self._opti_setting_layout = QVBoxLayout()
        self._opti_settings = []
        v_layout_1.addLayout(h_layout_v1_1)
        v_layout_1.addLayout(self._opti_setting_layout)
        self._opti_changed(0)

        v_layout_2 = QVBoxLayout()
        h_layout_v2_1 = QHBoxLayout()
        loss_select_combox = QComboBox()
        loss_select_combox.addItems(["CrossEntropy",
                                     "LabelSmoothingCrossEntropy",
                                     "Focal", ])
        loss_select_combox.currentIndexChanged.connect(self._loss_changed)
        self.loss_select_item = LkItem(label_txt="损失函数", key="loss_func", main=loss_select_combox)
        h_layout_v2_1.addWidget(self.loss_select_item)
        self._loss_setting_layout = QVBoxLayout()
        self._loss_settings = []
        v_layout_2.addLayout(h_layout_v2_1)
        v_layout_2.addLayout(self._loss_setting_layout)
        self._loss_changed(0)

        v_layout_3 = QVBoxLayout()
        h_layout_v3_1 = QHBoxLayout()
        lr_text = QLineEdit("0.01")
        self.lr_item = LkItem(label_txt="学习率", key="lr", main=lr_text)
        scheduler_select_combox = QComboBox()
        scheduler_select_combox.addItems(["None", "Cosine", "Step", "Poly"])
        scheduler_select_combox.currentIndexChanged.connect(self._scheduler_changed)
        self.scheduler_select_item = LkItem(label_txt="迭代策略", key="scheduler", main=scheduler_select_combox)
        h_layout_v3_1.addWidget(self.lr_item)
        h_layout_v3_1.addWidget(self.scheduler_select_item)
        self._scheduler_setting_layout = QVBoxLayout()
        self._scheduler_settings = []
        v_layout_3.addLayout(h_layout_v3_1)
        v_layout_3.addLayout(self._scheduler_setting_layout)
        self._scheduler_changed(0)

        v_layout_4 = QVBoxLayout()
        h_layout_v4_1 = QHBoxLayout()
        epoch_text = QLineEdit("100")
        self.epoch_item = LkItem(label_txt="训练次数", key="epoch", main=epoch_text)
        valid_text = QLineEdit("10")
        self.valid_item = LkItem(label_txt="验证间隔", key="valid", main=valid_text)
        h_layout_v4_1.addWidget(self.epoch_item)
        h_layout_v4_1.addWidget(self.valid_item)
        # -------------------
        h_layout_v4_2 = QHBoxLayout()
        batch_text = QLineEdit("32")
        batch_text.textChanged.connect(lambda x: self.last_batch_radio.setText(f"若最后一个批次中数据数量不足{x}, 是否舍弃?"))
        self.batch_item = LkItem(label_txt="批次大小", key="bs", main=batch_text)
        self.last_batch_radio = QRadioButton("若最后一个批次中数据数量不足32, 是否舍弃?")
        h_layout_v4_2.addWidget(self.batch_item)
        h_layout_v4_2.addWidget(self.last_batch_radio)
        v_layout_4.addLayout(h_layout_v4_1)
        v_layout_4.addLayout(h_layout_v4_2)

        v_layout.addLayout(v_layout_1)
        v_layout.addLayout(v_layout_2)
        v_layout.addLayout(v_layout_3)
        v_layout.addLayout(v_layout_4)
        self.setLayout(v_layout)

    def _opti_changed(self, index):
        self._opti_settings = []
        clear_layout(layout=self._opti_setting_layout)

        if index == 0:
            learning_rate_text = QLineEdit("1e-3")
            learning_rate_item = LkItem(label_txt="学习率", key="lr", main=learning_rate_text)
            self._opti_settings.append(learning_rate_item)
            momentum_text = QLineEdit("0.95")
            momentum_item = LkItem(label_txt="动量", key="momentum", main=momentum_text)
            self._opti_settings.append(momentum_item)

        elif index == 1:
            learning_rate_text = QLineEdit("1e-3")
            learning_rate_item = LkItem(label_txt="学习率", key="lr", main=learning_rate_text)
            self._opti_settings.append(learning_rate_item)
            beta1_text = QLineEdit("0.9")
            beta1_item = LkItem(label_txt="一阶矩估计指数衰减率", key="beta1", main=beta1_text)
            self._opti_settings.append(beta1_item)
            beta2_text = QLineEdit("0.999")
            beta2_item = LkItem(label_txt="二阶矩估计指数衰减率", key="beta2", main=beta2_text)
            self._opti_settings.append(beta2_item)

        elif index == 2:
            learning_rate_text = QLineEdit("1e-3")
            learning_rate_item = LkItem(label_txt="学习率", key="lr", main=learning_rate_text)
            self._opti_settings.append(learning_rate_item)
            beta1_text = QLineEdit("0.9")
            beta1_item = LkItem(label_txt="一阶矩估计指数衰减率", key="beta1", main=beta1_text)
            self._opti_settings.append(beta1_item)
            beta2_text = QLineEdit("0.999")
            beta2_item = LkItem(label_txt="二阶矩估计指数衰减率", key="beta2", main=beta2_text)
            self._opti_settings.append(beta2_item)
            weight_decay_text = QLineEdit("0.1")
            weight_decay_item = LkItem(label_txt="权重衰减", key="weight_decay", main=weight_decay_text)
            self._opti_settings.append(weight_decay_item)

        if self._opti_settings:
            for i in range(0, len(self._opti_settings), 2):
                ans_h_layout = QHBoxLayout()
                ans_h_layout.addWidget(self._opti_settings[i])
                try:
                    ans_h_layout.addWidget(self._opti_settings[i + 1])
                except:
                    pass
                self._opti_setting_layout.addLayout(ans_h_layout)

    def _loss_changed(self, index):
        self._loss_settings = []
        clear_layout(layout=self._loss_setting_layout)

        if index == 0:
            pass
        elif index == 1:
            smooth_text = QLineEdit("0.2")
            smooth_item = LkItem(label_txt="平滑度", key="smooth", main=smooth_text)
            self._loss_settings.append(smooth_item)
        elif index == 2:
            alpha_text = QLineEdit("0.5")
            alpha_item = LkItem(label_txt="正负样本权重(α)", key="alpha", main=alpha_text)
            self._loss_settings.append(alpha_item)
            gamma_text = QLineEdit("2")
            gamma_item = LkItem(label_txt="难易样本权重(γ)", key="gamma", main=gamma_text)
            self._loss_settings.append(gamma_item)

        if self._loss_settings:
            for i in range(0, len(self._loss_settings), 2):
                ans_h_layout = QHBoxLayout()
                ans_h_layout.addWidget(self._loss_settings[i])
                try:
                    ans_h_layout.addWidget(self._loss_settings[i + 1])
                except:
                    pass
                self._loss_setting_layout.addLayout(ans_h_layout)

    def _scheduler_changed(self, index):
        self._scheduler_settings = []
        clear_layout(layout=self._scheduler_setting_layout)

        if index == 0:
            pass
        elif index == 1:
            min_lr_text = QLineEdit("1e-5")
            min_lr_item = LkItem(label_txt="学习率最小值", key="lr_min", main=min_lr_text)
            self._scheduler_settings.append(min_lr_item)
            t_initial_text = QLineEdit("0")
            t_initial_item = LkItem(label_txt="下降一个周期的迭代次数", key="t_initial", main=t_initial_text)
            self._scheduler_settings.append(t_initial_item)
            # ---
            warmup_t_text = QLineEdit("0")
            warmup_t_item = LkItem(label_txt="预热迭代次数", key="warmup_t", main=warmup_t_text)
            self._scheduler_settings.append(warmup_t_item)
            warmup_lr_text = QLineEdit("0")
            warmup_lr_item = LkItem(label_txt="预热状态初始学习率", key="warmup_lr_init", main=warmup_lr_text)
            self._scheduler_settings.append(warmup_lr_item)
            # ---
            cycle_limit_text = QLineEdit("1")
            cycle_limit_item = LkItem(label_txt="下降周期的最大个数", key="cycle_limit", main=cycle_limit_text)
            self._scheduler_settings.append(cycle_limit_item)
            cycle_decay_text = QLineEdit("1")
            cycle_decay_item = LkItem(label_txt="周期初始开始的下降倍数", key="cycle_decay", main=cycle_decay_text)
            self._scheduler_settings.append(cycle_decay_item)

        elif index == 2:
            decay_t_text = QLineEdit("10")
            decay_t_item = LkItem(label_txt="下降一个系数的迭代次数", key="decay_t", main=decay_t_text)
            self._scheduler_settings.append(decay_t_item)
            decay_rate_text = QLineEdit("1")
            decay_rate_item = LkItem(label_txt="下降系数", key="decay_rate", main=decay_rate_text)
            self._scheduler_settings.append(decay_rate_item)
            # ---
            warmup_t_text = QLineEdit("0")
            warmup_t_item = LkItem(label_txt="预热迭代次数", key="warmup_t", main=warmup_t_text)
            self._scheduler_settings.append(warmup_t_item)
            warmup_lr_text = QLineEdit("0")
            warmup_lr_item = LkItem(label_txt="预热状态初始学习率", key="warmup_lr_init", main=warmup_lr_text)
            self._scheduler_settings.append(warmup_lr_item)

        else:
            min_lr_text = QLineEdit("1e-5")
            min_lr_item = LkItem(label_txt="学习率最小值", key="lr_min", main=min_lr_text)
            self._scheduler_settings.append(min_lr_item)
            t_initial_text = QLineEdit("0")
            t_initial_item = LkItem(label_txt="下降一个周期的迭代次数", key="t_initial", main=t_initial_text)
            self._scheduler_settings.append(t_initial_item)
            power_text = QLineEdit("0.5")
            power_item = LkItem(label_txt="多项式指数", key="power", main=power_text)
            self._scheduler_settings.append(power_item)
            # ---
            warmup_t_text = QLineEdit("0")
            warmup_t_item = LkItem(label_txt="预热迭代次数", key="warmup_t", main=warmup_t_text)
            self._scheduler_settings.append(warmup_t_item)
            warmup_lr_text = QLineEdit("0")
            warmup_lr_item = LkItem(label_txt="预热状态初始学习率", key="warmup_lr_init", main=warmup_lr_text)
            self._scheduler_settings.append(warmup_lr_item)
            # ---
            cycle_limit_text = QLineEdit("1")
            cycle_limit_item = LkItem(label_txt="下降周期的最大个数", key="cycle_limit", main=cycle_limit_text)
            self._scheduler_settings.append(cycle_limit_item)
            cycle_decay_text = QLineEdit("1")
            cycle_decay_item = LkItem(label_txt="周期初始开始的下降倍数", key="cycle_decay", main=cycle_decay_text)
            self._scheduler_settings.append(cycle_decay_item)

        if self._scheduler_settings:
            for i in range(0, len(self._scheduler_settings), 2):
                ans_h_layout = QHBoxLayout()
                ans_h_layout.addWidget(self._scheduler_settings[i])
                try:
                    ans_h_layout.addWidget(self._scheduler_settings[i + 1])
                except:
                    pass
                self._scheduler_setting_layout.addLayout(ans_h_layout)

    def export(self) -> dict:
        res = {"optimizer": dict(), "loss": dict(), "scheduler": dict(), "epoch": "", "valid": "", "bs": "",
               "is_last": None}

        res["optimizer"].update(self.opti_select_item.get_pair())
        for item in self._opti_settings:
            res["optimizer"].update(item.get_pair())

        res["loss"].update(self.loss_select_item.get_pair())
        for item in self._loss_settings:
            res["loss"].update(item.get_pair())

        res["scheduler"].update(self.scheduler_select_item.get_pair())
        for item in self._scheduler_settings:
            res["loss"].update(item.get_pair())

        res.update(self.batch_item.get_pair())
        res.update(self.valid_item.get_pair())
        res.update(self.lr_item.get_pair())
        res.update(self.epoch_item.get_pair())
        res.update(is_last=self.last_batch_radio.isChecked())
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
        print(self.setting_config)

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
