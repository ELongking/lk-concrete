import traceback
import sys

from PyQt5.QtCore import QThread, pyqtSignal

from src.tabular.LogText import LoggerHandler


class TrainThread(QThread):
    signal = pyqtSignal(str)
    bool_signal = pyqtSignal(bool)

    def __init__(self,
                 opt_path: str):
        super().__init__()
        self.logger = LoggerHandler(opt_path=opt_path,
                                    signal=self.signal)

        self.old_hook = sys.excepthook
        sys.excepthook = self._catch_error

    def _catch_error(self, ty, value, tb) -> None:
        traceback_format = traceback.format_exception(ty, value, tb)
        traceback_string = "".join(traceback_format)
        ans_signal = traceback_string
        self.logger.normal_browser_emit(ans_signal)
        self.quit()
        self.old_hook(ty, value, tb)

    def quit(self) -> None:
        self.bool_signal.emit(False)
        super().quit()

    def run(self) -> None:
        self.bool_signal.emit(True)
        self.logger.tab_browser_emit("准备工作开始...", step=1, level=1)
