from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, QHBoxLayout, QComboBox


class InfoLabel(QLabel):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPixmap(QPixmap("../assets/icons/info.png").scaledToWidth(16))
        self.setToolTip(text)


class LkItem(QWidget):
    def __init__(
            self,
            label_txt: str,
            key: str,
            main: QWidget,
            tip_txt: str = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.key = key
        self.label = QLabel(label_txt + ": ")
        self.main = main
        self.tip_txt = tip_txt
        self._set()

    def _set(self):
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.label)
        h_layout.addWidget(self.main)
        if self.tip_txt:
            h_layout.addWidget(InfoLabel(self.tip_txt))
        h_layout.setStretch(0, 2)
        h_layout.setStretch(1, 7)
        self.setLayout(h_layout)

    def get_element(self):
        return self.main

    def get_text(self):
        if isinstance(self.main, QLineEdit):
            return self.main.text()
        elif isinstance(self.main, QComboBox):
            return self.main.currentText()

    def get_pair(self):
        if isinstance(self.main, QLineEdit):
            return {self.key: self.main.text()}
        elif isinstance(self.main, QComboBox):
            return {self.key: self.main.currentText()}
