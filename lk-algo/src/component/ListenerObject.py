from PyQt5.QtCore import QObject, pyqtSignal


class LObject(QObject):
    value_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self._value = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.value_changed.emit(value)
