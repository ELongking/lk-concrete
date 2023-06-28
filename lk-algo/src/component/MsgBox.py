from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap


class WarningBox(QMessageBox):
    def __init__(self, parent=None, title="", text=""):
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
