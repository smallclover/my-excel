from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog, QFileDialog, QMessageBox

from db_op import DBOperations
from import_dialog import Ui_ImportDialog


class ImportDialog(QDialog, Ui_ImportDialog):
    data_imported = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):

        self.chooseFile.clicked.connect(self.browse_file)
        self.OkButton.clicked.connect(self.import_data)
        self.cancelButton.clicked.connect(self.reject)

    def browse_file(self):
        try:
            default_directory = 'C:/Users/wangshun/Desktop'
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "选择文件",
                default_directory,  # 设置默认目录
                "Text Files (*.txt);;CSV Files (*.csv)"
            )
            if file_name:
                self.fileUrl.setText(file_name)
        except Exception as e:
            print(e)

    def import_data(self):
        try:
            file_path = self.fileUrl.text()
            delimiter = self.get_delimiter()
            linebreak = self.get_linebreak()

            if not file_path:
                QMessageBox.warning(self, "警告", "请先选择文件")
                return

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            rows = content.split(linebreak)
            data_list = [row.split(delimiter) for row in rows]
            DBOperations.insert_data_into_db(data_list)
            QMessageBox.information(self, "成功", "数据已成功导入数据库")
            self.data_imported.emit()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入数据时出现错误: {e}")

    def get_delimiter(self):
        delimiter_map = {
            '空格': ' ',
            '逗号 (,)': ',',
            '分号 (;)': ';',
            '制表符 (\\t)': '\t'
        }
        selected = self.delimerList.currentText()
        return delimiter_map.get(selected, ' ')  # 默认返回空格

    def get_linebreak(self):
        linebreak_map = {
            '\\n': '\n',
            '\\r\\n': '\r\n',
            '\\r': '\r'
        }
        selected = self.lineBreakList.currentText()
        return linebreak_map.get(selected, '\n')  # 默认返回 \n

