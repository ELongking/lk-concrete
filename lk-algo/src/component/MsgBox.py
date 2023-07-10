from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap

from src.utils.ThreadUtils import CustomThread


class WarningBox(QMessageBox):
    def __init__(self, parent=None, title="", text="", ):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setIconPixmap(QPixmap("../assets/icons/warning.png"))
        self.setDefaultButton(QMessageBox.Yes)
        self._exec()

    def _exec(self):
        result = super().exec_()
        return result


class SuccessBox(QMessageBox):
    def __init__(self, parent=None, title="", text=""):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.setText(text)
        self.setIconPixmap(QPixmap("../assets/icons/correct.png"))
        self.setDefaultButton(QMessageBox.Yes)
        self._exec()

    def _exec(self):
        result = super().exec_()
        return result


class ProcessBox(QMessageBox):
    def __init__(self, parent=None, title="", text="", thread: CustomThread = None):
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.setText(text)

        self.stop_btn = QPushButton("取消")
        self.stop_btn.clicked.connect(self._stop_thread)
        self.setDefaultButton(self.stop_btn)

        self.thread = thread
        self.thread.signal.connect(self.process_finish)

    def exec(self):
        self.show()
        self.thread.start()

    def _stop_thread(self):
        self.thread.terminate()
        self.setWindowTitle("提示")
        self.setText("文件下载中止")

    def process_finish(self, res):
        if res == "success":
            self.setWindowTitle("成功")
            self.setText("文件下载完毕")
        else:
            self.setWindowTitle("失败")
            self.setText(res)
