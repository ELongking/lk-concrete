from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class ReadOnlyDelegate(QStyledItemDelegate):
    def __init__(self):
        super(ReadOnlyDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        return None

    def editorEvent(self, event, model, option, index):
        return False

    def sizeHint(self, option, index):
        return super().sizeHint(option, index)


class TabularItem(QStandardItem):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setFlags(self.flags() & ~Qt.ItemIsEnabled)
        self._init_model_item()

    def _init_model_item(self) -> None:
        preprocess_item = QStandardItem("前处理")
        algo_item = QStandardItem("算法选择")
        setting_item = QStandardItem("其他设置")
        start_item = QStandardItem("开始")

        self.appendRow(preprocess_item)
        self.appendRow(algo_item)
        self.appendRow(setting_item)
        self.appendRow(start_item)


class ImageItem(QStandardItem):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setFlags(self.flags() & ~Qt.ItemIsEnabled)
        self._init_model_item()

    def _init_model_item(self):
        preprocess_item = QStandardItem("前处理")
        algo_item = QStandardItem("算法选择")
        setting_item = QStandardItem("其他设置")
        start_item = QStandardItem("开始")

        self.appendRow(preprocess_item)
        self.appendRow(algo_item)
        self.appendRow(setting_item)
        self.appendRow(start_item)


class AsideTreeView(QTreeView):
    def __init__(self, parent, config: list):
        super().__init__(parent=parent)

        self.header().setHidden(True)

        self.config = config
        self.tmodel = QStandardItemModel()
        self.setModel(self.tmodel)
        delegate = ReadOnlyDelegate()
        self.setItemDelegate(delegate)

        self.tabular_item = QStandardItem("表格项")
        self.image_item = QStandardItem("图片项")
        self.tmodel.appendRow(self.tabular_item)
        self.tmodel.appendRow(self.image_item)

        self.item_num = [0, 0]
        self._init_tree()

    def _init_tree(self) -> None:
        for item in self.config:
            ans_name = item["fileName"]
            ans_name = ans_name.split("\\")[-1]
            if item["fileType"] == "tabular":
                ans_item = TabularItem(ans_name)
                self.tabular_item.appendRow(ans_item)
                self.item_num[0] += 1
            else:
                ans_item = ImageItem(ans_name)
                self.image_item.appendRow(ans_item)
                self.item_num[1] += 1
