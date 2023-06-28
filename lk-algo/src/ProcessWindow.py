from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from component.MsgBox import WarningBox, SuccessBox

from utils.FileUtils import *

from connector.SqlHandle import SqlHandle
from connector.OssHandle import OssHandle


class ProcessWindow(QMainWindow):
    def __init__(self, sql_handle: SqlHandle):
        super(ProcessWindow, self).__init__()
        self.sql_handle = sql_handle
        self.oss_handle = OssHandle()

        self.menu = self.menuBar()
        self.resize(1280, 800)
        self._center()
        self._init_gui()

        self.cid_cname = dict()

    def _center(self) -> None:
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, ((screen.height() - size.height()) // 2) - 50)

    def _init_gui(self) -> None:
        self._init_menu()

    def _init_menu(self) -> None:
        file = self.menu.addMenu("文件")
        file_download = file.addMenu("下载")
        self.cid_cname = self.sql_handle.show_all_cinfo()
        for cname in self.cid_cname.keys():
            ans_action = QAction(cname, self)
            ans_action.triggered.connect(lambda: self._download_file(cname))
            file_download.addAction(ans_action)

        file_import = QAction("引入", self)
        file_import.triggered.connect(self._directory_import)
        file.addAction(file_import)

    def _download_file(self, cname) -> None:
        flag, msg = self.oss_handle.download(uid=self.sql_handle.config["uid"],
                                             cid=self.cid_cname[cname],
                                             uname=self.sql_handle.config["username"],
                                             cname=cname)
        if flag:
            SuccessBox(self, "完成", "下载成功")
        else:
            WarningBox(self, "出错", msg)

    def _directory_import(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if folder_path:
            flag = check_case_directory(folder_path)
            if flag:
                pass
            else:
                WarningBox(self, "出错", "请检查目录格式")
        else:
            WarningBox(self, "出错", "请选择文件夹")
