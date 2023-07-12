from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, \
    QGroupBox, QRadioButton, QLineEdit, QLabel, QButtonGroup
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建左侧treeview
        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)

        # 添加表格和图片两个大项目
        table_item = QStandardItem("表格")
        image_item = QStandardItem("图片")
        self.model.appendRow([table_item, image_item])

        # 为表格大项目添加二级项目
        table_subitem1 = self.create_subitem("表格1")
        table_subitem2 = self.create_subitem("表格2")
        table_item.appendRow([table_subitem1, table_subitem2])

        # 为图片大项目添加二级项目
        image_subitem1 = self.create_subitem("图片1")
        image_subitem2 = self.create_subitem("图片2")
        image_item.appendRow([image_subitem1, image_subitem2])

        # 创建右侧主页面
        self.stacked_widget = QStackedWidget()
        table_page1 = self.create_page("表格1页面", ["填写内容1", "填写内容2", "填写内容3"])
        table_page2 = self.create_page("表格2页面", ["填写内容4", "填写内容5", "填写内容6"])
        image_page1 = self.create_page("图片1页面", ["填写内容7", "填写内容8", "填写内容9"])
        image_page2 = self.create_page("图片2页面", ["填写内容10", "填写内容11", "填写内容12"])
        self.stacked_widget.addWidget(table_page1)
        self.stacked_widget.addWidget(table_page2)
        self.stacked_widget.addWidget(image_page1)
        self.stacked_widget.addWidget(image_page2)

        # 将treeview和右侧主页面放置在窗口中
        central_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.tree_view)
        layout.addWidget(self.stacked_widget)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_subitem(self, name):
        # 创建二级项目
        subitem = QStandardItem(name)

        # 创建四个小项目
        group_box = QGroupBox()
        layout = QVBoxLayout()
        radio_button1 = QRadioButton("选项1")
        radio_button2 = QRadioButton("选项2")
        radio_button3 = QRadioButton("选项3")
        radio_button4 = QRadioButton("选项4")
        layout.addWidget(radio_button1)
        layout.addWidget(radio_button2)
        layout.addWidget(radio_button3)
        layout.addWidget(radio_button4)
        group_box.setLayout(layout)

        # 将四个小项目添加到二级项目中
        subitem.appendRow([QStandardItem(group_box), None, None, None])

        # 将四个小项目分组
        button_group = QButtonGroup()
        button_group.addButton(radio_button1)
        button_group.addButton(radio_button2)
        button_group.addButton(radio_button3)
        button_group.addButton(radio_button4)

        # 为最后一个小项目添加点击事件
        radio_button4.clicked.connect(lambda: self.show_result(subitem))

        return subitem

    def create_page(self, name, labels):
        # 创建页面
        page = QWidget()

        # 创建填写内容的小项目
        label1 = QLabel(labels[0])
        line_edit1 = QLineEdit()
        label2 = QLabel(labels[1])
        line_edit2 = QLineEdit()
        label3 = QLabel(labels[2])
        line_edit3 = QLineEdit()

        # 将填写内容的小项目添加到页面中
        layout = QVBoxLayout()
        layout.addWidget(QLabel(name))
        layout.addWidget(label1)
        layout.addWidget(line_edit1)
        layout.addWidget(label2)
        layout.addWidget(line_edit2)
        layout.addWidget(label3)
        layout.addWidget(line_edit3)
        page.setLayout(layout)

        return page

    def show_result(self, item):
        # 获取前三个小项目中的填入信息
        group_box_item = item.child(0)
        group_box_layout = group_box_item.index().data(Qt.DisplayRole).layout()
        button_group = group_box_layout.itemAt(0).widget()
        selected_button = button_group.checkedButton()

        line_edit_items = [item.child(i) for i in range(1, 4)]
        line_edit_texts = [line_edit_item.index().data(Qt.DisplayRole) for line_edit_item in line_edit_items]

        result_text = f"{selected_button.text()} {line_edit_texts[0]} {line_edit_texts[1]} {line_edit_texts[2]}"

        # 在右侧主页面上显示结果
        index = item.index()
        parent_index = index.parent()

        if parent_index.row() == 0:
            if index.row() == 0:
                self.stacked_widget.setCurrentIndex(0)
                self.stacked_widget.currentWidget().layout().itemAt(1).widget().setText(result_text)
            elif index.row() == 1:
                self.stacked_widget.setCurrentIndex(1)
                self.stacked_widget.currentWidget().layout().itemAt(1).widget().setText(result_text)

        elif parent_index.row() == 1:
            if index.row() == 0:
                self.stacked_widget.setCurrentIndex(2)
                self.stacked_widget.currentWidget().layout().itemAt(1).widget().setText(result_text)
            elif index.row() == 1:
                self.stacked_widget.setCurrentIndex(3)
                self.stacked_widget.currentWidget().layout().itemAt(1).widget().setText(result_text)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
