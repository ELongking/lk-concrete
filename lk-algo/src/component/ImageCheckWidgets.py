from PyQt5.QtWidgets import *


class IPreProcessWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()

        h_layout_1 = QHBoxLayout()
        default_label = QLabel("缺省值填充 -> ")
        h_layout_1.addWidget(default_label)
        default_btn_group = QButtonGroup(self)
        for index, title in enumerate(["填充0", "填充均值", "删除整行"]):
            default_btn_group.addButton(QRadioButton(title, self))
            h_layout_1.addWidget(default_btn_group.buttons()[index])
        default_btn_group.buttons()[0].setChecked(True)

        h_layout_2 = QHBoxLayout()
        normal_label = QLabel("标准化方法 -> ")
        h_layout_2.addWidget(normal_label)
        normal_btn_group = QButtonGroup(self)
        for index, title in enumerate(["0~1分布", "-1~1分布", "正态分布"]):
            normal_btn_group.addButton(QRadioButton(title, self))
            h_layout_2.addWidget(default_btn_group.buttons()[index])
        default_btn_group.buttons()[0].setChecked(True)

        h_layout_3 = QHBoxLayout()
        ana_check_btn = QCheckBox("异常值舍弃")

        h_layout_3.addWidget(ana_check_btn)

        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        v_layout.addLayout(h_layout_3)
        v_layout.setSpacing(30)

        self.setLayout(v_layout)


class IAlgoSelectWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_widget()

    def _init_widget(self):
        v_layout = QVBoxLayout()

        all_algo = ["ElasticNet", "Lasso", "Ridge", "RandomForest", "DecisionTree",
                    "AdaBoost", "ExtraTree", "LightGBM", "XgBoost", "CatBoost"]
        algo_layout = QGridLayout()
        algo_btn_group = QButtonGroup(self)
        for index, title in enumerate(all_algo):
            ans_check_btn = QCheckBox(title)
            algo_btn_group.addButton(ans_check_btn)
            algo_layout.addWidget(ans_check_btn, index // 3, index % 3)
        v_layout.addLayout(algo_layout)
        self.setLayout(v_layout)


class ISettingWidget(QWidget):
    def __init__(self):
        super().__init__()

    def _init_widget(self):
        grid_layout = QGridLayout()
        setting_btn_group = QButtonGroup(self)
        all_setting = ["算法参数优化", "特征值二次选择", "引入AutoML方法"]
        for index, title in enumerate(all_setting):
            ans_check_btn = QCheckBox(title)
            setting_btn_group.addButton(ans_check_btn)
            grid_layout.addWidget(ans_check_btn, index // 3, index % 3)

        self.setLayout(grid_layout)


class IStartExportWidget(QWidget):
    def __init__(self):
        super().__init__()

    def _init_widget(self):
        v_layout = QVBoxLayout()

        h_layout = QHBoxLayout()
        logging_text = QTextBrowser()
        v_layout_1 = QVBoxLayout()
        start_btn = QPushButton("开始训练")
        open_opt_btn = QPushButton("打开输出文件夹")
        v_layout_1.addWidget(start_btn)
        v_layout_1.addLayout(open_opt_btn)
        h_layout.addWidget(logging_text)
        h_layout.addLayout(v_layout_1)

        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)


