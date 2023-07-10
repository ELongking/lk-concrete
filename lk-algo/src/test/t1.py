import sys

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个树形视图
        self.tree = QTreeView(self)
        self.tree.setGeometry(50, 50, 200, 200)

        # 创建一个标准项模型
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)

        # 添加一些自定义项目
        item1 = QStandardItem("Item 1")
        item2 = QStandardItem("Item 2")
        item3 = QStandardItem("Item 3")
        self.model.appendRow(item1)
        self.model.appendRow(item2)
        item2.appendRow(item3)

        # 添加更多自定义项目
        item4 = QStandardItem("Item 4")
        item5 = QStandardItem("Item 5")
        item6 = QStandardItem("Item 6")
        item3.appendRow(item4)
        item3.appendRow(item5)
        item5.appendRow(item6)


# 创建应用程序并显示窗口
app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
