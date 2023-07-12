from PyQt5.QtWidgets import *

from connector.SqlHandle import SqlHandle
from connector.OssHandle import OssHandle

from component.AsideTree import AsideTreeView
from component.ImageCheckWidgets import *
from component.TabularCheckWidgets import *
from component.ListenerObject import LObject

from function.MenuFunc import *


class ProcessWindow(QMainWindow):
    def __init__(self, sql_handle: SqlHandle):
        super(ProcessWindow, self).__init__()
        self.sql_handle = sql_handle
        self.oss_handle = OssHandle()
        self.is_import = LObject()
        self.is_import.value_changed.connect(self._init_dynamic_gui)

        self.resize(1280, 800)
        self._center()

        self.cid_cname = dict()
        self.config = []

        self.now_cid = ""
        self.now_cname = ""

        self._init_static_gui()

    def _center(self) -> None:
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, ((screen.height() - size.height()) // 2) - 50)

    def _init_static_gui(self) -> None:
        self._init_menu()
        self._init_status()

    def _init_dynamic_gui(self, flag) -> None:
        if flag:
            self._init_tabs()
        else:
            pass

    def _init_menu(self) -> None:
        self.menu = self.menuBar()
        file = self.menu.addMenu("文件")
        file_download = file.addMenu("下载")
        self.cid_cname = self.sql_handle.show_all_cinfo()

        for cname in self.cid_cname.keys():
            ans_action = QAction(cname, self)
            ans_action.triggered.connect(lambda: download_file(self, cname))
            file_download.addAction(ans_action)

        file_import = QAction("引入", self)
        file_import.triggered.connect(lambda: directory_import(self))
        file.addAction(file_import)

    def _init_tabs(self):
        tabs = QTabWidget()
        self.detail_tab = QWidget()
        self.train_tab = QWidget()
        self.infer_tab = QWidget()

        tabs.addTab(self.detail_tab, "概况")
        tabs.addTab(self.train_tab, "训练")
        tabs.addTab(self.infer_tab, "推理")

        self._init_train_tab()
        self.setCentralWidget(tabs)

    def _init_status(self):
        status_bar = QStatusBar()
        uname_label = QLabel(f" 用户 -> {self.sql_handle.config['username']}")
        self.cname_label = QLabel()
        status_bar.addWidget(uname_label)
        status_bar.addWidget(self.cname_label)
        self.setStatusBar(status_bar)

    def _init_train_tab(self):
        aside_tree = AsideTreeView(parent=self.train_tab, config=self.config)
        self.train_main_widget = QStackedWidget()
        self.train_main_widget.addWidget(QWidget())

        tabular_case_path = osp.join("../data", self.sql_handle.config["username"], self.now_cname, "tabular")
        image_case_path = osp.join("../data", self.sql_handle.config["username"], self.now_cname, "image")

        for _ in range(aside_tree.item_num[0]):
            t_stacked_widgets = [
                TPreProcessWidget(),
                TAlgoSelectWidget(task_type=self.sql_handle.get_task_type(cid=self.config[0]["cid"], mode="tabular")),
                TSettingWidget(),
                TStartExportWidget(case_path=tabular_case_path),
            ]
            for t in t_stacked_widgets:
                self.train_main_widget.addWidget(t)
        for _ in range(aside_tree.item_num[1]):
            i_stacked_widgets = [
                IPreProcessWidget(), IAlgoSelectWidget(), ISettingWidget(), IStartExportWidget(),
            ]
            for i in i_stacked_widgets:
                self.train_main_widget.addWidget(i)

        h_layout = QHBoxLayout()
        h_layout.addWidget(aside_tree)
        h_layout.addWidget(self.train_main_widget)
        h_layout.setStretch(0, 2)
        h_layout.setStretch(1, 8)
        self.train_tab.setLayout(h_layout)

        aside_tree.clicked.connect(self._tree_change_widget)

    def _tree_change_widget(self, element):
        parent = element.parent()
        if parent.parent().isValid():
            parent_index = parent.row()
            widget_index = element.row()
            self.train_main_widget.setCurrentIndex(parent_index * 4 + widget_index + 1)
        else:
            pass
