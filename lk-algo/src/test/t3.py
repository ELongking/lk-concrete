from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel


class MyThread(QThread):
    signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.is_run = False

    def run(self):
        self.is_run = True
        self.signal.emit(self.is_run)
        # 执行耗时任务
        self.sleep(5)
        self.is_run = False
        self.signal.emit(self.is_run)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.button = QPushButton("Start")
        self.label = QLabel("Not running")
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.thread = MyThread()
        self.thread.signal.connect(self.paintEvent)
        self.button.clicked.connect(self.start_thread)

    def start_thread(self):
        self.thread.start()

    def paintEvent(self, flag):
        print(flag)
        painter = QPainter(self)
        if flag:
            painter.drawText(10, 50, "Running")
        else:
            painter.drawText(10, 50, "Not running")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
