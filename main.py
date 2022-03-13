import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import os

'''
读取文件
'''

main_code = '''
# include <stdio.h>
int main(void)
{
    print("hello world!")
    return 0;
}
'''


# 读取文件
def get_code(file_path: str, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as fp:
        return fp.read()


# 保存文件
def save_code(file_path: str, code: str, encoding='utf-8'):
    with open(file_path, 'w', encoding=encoding) as fp:
        fp.write(code)


# 扫描文件夹生成目录
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # 当前目录路径
        print(dirs)  # 当前路径下所有子目录
        print(files)  # 当前路径下所有非目录子文件


class MainDemo(QMainWindow):

    def __init__(self):
        super(MainDemo, self).__init__()
        self.ui = uic.loadUi("main.ui")
        # 事件绑定：按钮点击绑定到 handleCalc 事件
        # 菜单栏事件
        self.ui.actionopen.triggered.connect(self.open_file)
        self.ui.actionsave.triggered.connect(self.save_file)
        self.ui.actionnew.triggered.connect(self.new_file)
        self.ui.actionopenworkspace.triggered.connect(self.open_workspace)

        # self.ui.actionhelp.triggered.connect(self.get_help)
        # self.ui.actionrun.triggered.connect(self.run)
        # 目录点击事件
        # self.ui.listWidget.itemClicked.connect(self.change_text)
        # 当前编辑的文件

        # 文本框改变事件
        self.ui.textEdit.textChanged.connect(self.text_change)
        self.edit_file_name = ''
        # 文件目录 如 D:\ProgramData\Anaconda3\python.exe E:/Users/41558/Desktop/编译原理/main.py
        self.file_dict = {
            # 'untitled.c': ['untitled']
        }
        self.ui.treeWidget.setHeaderLabels(['文件夹', '文件'])
        self.ui.treeWidget.clicked.connect(self.tree_clicked)

    def tree_clicked(self):
        try:
            item = self.ui.treeWidget.currentItem()
            self.edit_file_name = item.text(1)
            file_path = self.file_dict.get(self.edit_file_name)
            code = get_code(file_path=file_path)
            self.ui.textEdit.setPlainText(code)  # 文本框改变
            self.ui.file_name_label.setText(self.edit_file_name)  # 文件名改变
        except Exception as e:
            QMessageBox.critical(
                self.ui,
                '错误',
                '该文件类型不支持预览')

    def open_workspace(self):
        file_path = QFileDialog.getExistingDirectory(self.ui, "选择文件夹")
        file_name(file_path)
        for root, dirs, files in os.walk(file_path):
            # # 添加文件夹
            # for i in dirs:
            #     root_item = QTreeWidgetItem(self.ui.treeWidget)
            #     root_item.setIcon(0, QIcon('./icon/folder-minus.svg'))
            #     root_item.setText(0, i)
            for i in files:
                root_item = QTreeWidgetItem(self.ui.treeWidget)
                root_item.setIcon(1, QIcon('./icon/file.svg'))
                root_item.setText(1, i)
                self.file_dict[i] = os.path.join(root, i)

    # 新建文件
    def new_file(self):
        new_file_name, ok = QInputDialog.getText(
            self,
            "输入文件名称",
            "名称:",
            QLineEdit.Normal,
            "untitled.c")
        if not ok:
            QMessageBox.warning(
                self.ui,
                '你取消了操作',
                '文件将不会被创建')
        else:
            save_code(file_path=new_file_name, code=main_code)
            self.edit_file_name = new_file_name  # 当前编辑文件改变
            self.file_dict[new_file_name] = new_file_name  # 添加到文件目录中
            self.ui.textEdit.setPlainText(main_code)  # 文本框改变
            self.ui.file_name_label.setText(self.edit_file_name)  # 文件名改变

    # 打开文件
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui,  # 父窗口对象
            "选择文件",  # 标题
            r"./",  # 起始目录
            "C/C++代码 (*.c *.cpp *.txt)"  # 选择类型过滤项，过滤内容在括号中
        )

        try:
            self.edit_file_name = file_path.split('/')[-1]
            code = get_code(file_path=file_path)
            self.file_dict[self.edit_file_name] = file_path
            self.ui.textEdit.setPlainText(code)
            self.ui.file_name_label.setText(self.edit_file_name)  # 文件名改变
            print(self.file_dict)
        except FileNotFoundError as e:
            print('文件没有找到或者取消了打开文件操作', e)

    # 保存文件
    def save_file(self):
        code = self.ui.textEdit.toPlainText()
        file_path = self.file_dict.get(self.edit_file_name)
        save_code(file_path=file_path, code=code)
        self.ui.file_name_label.setText(self.edit_file_name)  # 文件名改变

    # 文本被改变时
    def text_change(self):
        self.ui.file_name_label.setText(self.edit_file_name + '*')  # 文件名改变


if __name__ == '__main__':
    app = QApplication(sys.argv)
    stats = MainDemo()
    stats.ui.show()
    app.exec_()
