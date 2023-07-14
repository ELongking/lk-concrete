from PyQt5.QtCore import pyqtSignal
from loguru import logger
from datetime import datetime as dt
import os.path as osp


class LoggerHandler:
    def __init__(self, opt_path: str, signal: pyqtSignal(str)):
        self.opt_path = opt_path
        self.signal = signal
        self.logger = logger

    def init_logger(self, task_name: str):
        self.logger.add(sink=osp.join(self.opt_path, f"{task_name}-{dt.now().strftime('%Y%m%d_%H%M%S')}.log"))

    def normal_browser_emit(self, text) -> None:
        time_tag = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        res = f"{time_tag} || {text}"
        self.signal.emit(res)

    def tab_browser_emit(self, text: str, step: int, level: int) -> None:
        assert step > 0
        assert level > 0

        arrow = "  " * (level - 1) + "- " + f"[{step}.{level}]" + " -" + ">"
        time_tag = dt.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        res = f"{arrow} {time_tag} || {text}"
        self.signal.emit(res)

    def set_info(self, text: str):
        self.logger.info(text)

    def set_warning(self, text: str):
        self.logger.warning(text)

    def set_error(self, text: str):
        self.logger.error(text)
