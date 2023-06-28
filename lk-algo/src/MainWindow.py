import traceback
import sys
from PyQt5.QtWidgets import *

from connector.SqlHandle import SqlHandle

from component.MsgBox import WarningBox

from ProcessWindow import ProcessWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("lk-concrete-algo")
        self.setMinimumSize(640, 480)
        self.sql_handle = SqlHandle()

        self._center()
        self._init_gui()

    def _center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def _catch_error(self, ty, value, tb):
        traceback_format = traceback.format_exception(ty, value, tb)
        traceback_string = "".join(traceback_format)
        QMessageBox.critical(self, "额外报错，请联系作者解决", "{}".format(traceback_string))
        self.old_hook(ty, value, tb)

    def _init_gui(self):
        widget = QWidget()

        v_layout = QVBoxLayout()
        h_layout_1 = QHBoxLayout()
        h_layout_2 = QHBoxLayout()
        h_layout_3 = QHBoxLayout()
        h_layout_4 = QHBoxLayout()

        username_label = QLabel("用户名: ")
        self.username_text = QLineEdit("longking")
        self.username_text.setPlaceholderText("请输入用户名")
        h_layout_1.addWidget(username_label)
        h_layout_1.addWidget(self.username_text)

        password_label = QLabel("密码: ")
        self.password_text = QLineEdit("19980917")
        self.password_text.setPlaceholderText("请输入密码")
        self.password_text.setEchoMode(QLineEdit.Password)
        h_layout_2.addWidget(password_label)
        h_layout_2.addWidget(self.password_text)

        login_btn = QPushButton("登录")
        reset_btn = QPushButton("重置")
        login_btn.clicked.connect(self._login)
        reset_btn.clicked.connect(self._reset)
        h_layout_3.addWidget(login_btn)
        h_layout_3.addWidget(reset_btn)

        v_layout.addLayout(h_layout_1)
        v_layout.addLayout(h_layout_2)
        v_layout.addLayout(h_layout_3)
        v_layout.setContentsMargins(60, 40, 60, 40)

        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

    def _login(self):
        username = self.username_text.text()
        password = self.password_text.text()
        flag = self.sql_handle.login(username, password)
        if flag:
            self.pw = ProcessWindow(sql_handle=self.sql_handle)
            self.pw.show()
            self.showMinimized()
        else:
            WarningBox(self, "出错", "登陆失败, 请检查用户名和密码")

    def _reset(self):
        self.sql_handle.reset()
        self.username_text.clear()
        self.password_text.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec()
