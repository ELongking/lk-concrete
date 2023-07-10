from PyQt5.QtCore import QThread, pyqtSignal, Qt


class CustomThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, func, **kwargs):
        super().__init__()
        self.func = func
        self.kwargs = kwargs

    def run(self):
        res = self.func(**self.kwargs)
        self.signal.emit(res)