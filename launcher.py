import sys
from idlelib.help_about import AboutDialog

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QDate, QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QDialog, QTableWidgetItem, QMessageBox, QProgressDialog, QFileDialog

from calendar_dialog import Ui_CalenderDialog
from db_op import DBOperations
from excel_util import ExcelUtil
from main import Ui_MainWindow
from add_dialog import Ui_Dialog
from import_dialog import Ui_ImportDialog
from my_work import MyWork


class MyExcelMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        DBOperations.create_table()
        self.init_ui()
        self.init_table()

    def init_ui(self):
        current_date = QDate.currentDate()
        formatted_date = current_date.toString("yyyy-MM-dd")
        self.currentDateLabel.setText(f'当前日期：{formatted_date}')

        self.addButton.clicked.connect(self.add_dialog)
        self.exportButton.clicked.connect(self.export_to_excel)
        self.delButton.clicked.connect(self.del_dialog)
        self.editButton.clicked.connect(self.edit_dialog)
        self.importButton.clicked.connect(self.import_dialog)
        self.AboutMenu.triggered.connect(self.about_dialog)
        self.chooseDateButton.clicked.connect(self.show_calendar)


    def init_table(self):
        data_list = DBOperations.get_data()
        self.load_data(data_list)

    def load_data(self, data_list):
        self.tableWidget.setRowCount(len(data_list))
        for i, row in enumerate(data_list):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
        self.tableWidget.setColumnHidden(0, True)

    def add_dialog(self):

        dialog = AddDialog()
        dialog.data_saved.connect(self.refresh_table)
        # dialog.show()
        dialog.exec()

    def del_dialog(self):
        try:
            selected_items = self.tableWidget.selectedItems()
            if not selected_items:
                self.show_hint('请指定要删除的数据')
                return

            selected_row = selected_items[0].row()
            print(selected_row)
            selected_id = self.tableWidget.item(selected_row, 0).text()
            print(f'selected_id: {selected_id}')
            data = [self.tableWidget.item(selected_row, col).text() for col in range(self.tableWidget.columnCount())]
            print(f'data: {data}')

            dialog = AddDialog(3, data, selected_id, self)
            dialog.data_saved.connect(self.refresh_table)
            # dialog.show()
            dialog.exec()

        except Exception as e:
            print(e)

    def edit_dialog(self):
        try:
            selected_items = self.tableWidget.selectedItems()
            if not selected_items:
                self.show_hint('请指定要修改的数据')
                return

            selected_row = selected_items[0].row()
            print(selected_row)
            selected_id = self.tableWidget.item(selected_row, 0).text()
            print(f'selected_id: {selected_id}')
            data = [self.tableWidget.item(selected_row, col).text() for col in range(self.tableWidget.columnCount())]
            print(f'data: {data}')

            dialog = AddDialog(2, data, selected_id, self)
            dialog.data_saved.connect(self.refresh_table)
            # dialog.show()
            dialog.exec()

        except Exception as e:
            print(e)

    def import_dialog(self):
        dialog = ImportDialog()
        dialog.data_imported.connect(self.refresh_table)
        # dialog.show()
        dialog.exec()

    def about_dialog(self):
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle('About')
        about_dialog.setText('''
        这是一个生成勤务表的项目
        作者:三页半
        ''')
        about_dialog.exec()

    def show_calendar(self):
        # 创建并显示 CalendarDialog
        dialog = CalendarDialog()
        dialog.exec()

    def export_to_excel(self):
        # 创建并显示“导出中”提示框
        self.export_dialog = QProgressDialog("导出中，请稍候...", None, 0, 0, self)
        self.export_dialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.export_dialog.setMinimumDuration(0)  # 立即显示提示框
        self.export_dialog.show()

        # 创建并启动后台线程
        self.export_thread = ExportThread()
        self.export_thread.finished.connect(self.on_export_finished)
        self.export_thread.start()

    def on_export_finished(self):
        # 关闭“导出中”提示框
        self.export_dialog.hide()
        self.show_hint("导出成功")

    def refresh_table(self):
        self.tableWidget.setRowCount(0)
        # 清除表格内容
        self.tableWidget.clearContents()
        # 获取新数据
        data_list = DBOperations.get_data()
        # 重新加载新数据
        self.load_data(data_list)

    def show_hint(self, message):
        hint_msg = QMessageBox()
        hint_msg.setText(message)
        hint_msg.setWindowTitle("提示")
        hint_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        hint_msg.exec()


class AddDialog(QDialog, Ui_Dialog):
    data_saved = QtCore.pyqtSignal()

    # 1:追加2:修改3:删除
    def __init__(self, action_type=1, data=[], row_id=None, parent=None):
        super().__init__(parent)
        self.row_id = row_id
        self.action_type = action_type
        self.setupUi(self)
        self.init_ui(data, row_id)

    def init_ui(self, data=None, row_id=None):
        self.okButton.clicked.connect(self.ok_clicked)
        self.cancelButton.clicked.connect(self.reject)
        if self.action_type == 1:
            pass
        elif self.action_type == 2:
            self.titleLabel.setText("是否要确认修改")
            self.work_start_time.setCurrentText(data[1])
            self.work_end_time.setCurrentText(data[2])
            self.work_content.setText(data[5])
        else:
            self.titleLabel.setText("是否要确认删除！！！")
            self.work_start_time.setEnabled(False)
            self.work_end_time.setEnabled(False)
            self.work_content.setEnabled(False)
            self.work_start_time.setCurrentText(data[1])
            self.work_end_time.setCurrentText(data[2])
            self.work_content.setText(data[5])

    def ok_clicked(self):
        try:
            self.close()
            if self.action_type == 1:
                current_date = QDate.currentDate()
                formatted_date = current_date.toString("yyyy-MM-dd")
                my_work = MyWork(formatted_date, self.work_start_time.currentText(), self.work_end_time.currentText(),
                                 self.work_content.toPlainText())
                DBOperations.add_data(my_work)
                self.show_hint('追加成功')
            elif self.action_type == 2:
                DBOperations.up_data(self.row_id, {
                    'value1': self.work_start_time.currentText(),
                    'value2': self.work_end_time.currentText(),
                    'value3': self.work_content.toPlainText()
                })
                self.show_hint('修改成功')
            else:
                DBOperations.del_data(self.row_id)
                self.show_hint('删除成功')
            self.data_saved.emit()
            self.accept()
        except Exception as e:
            print(e)

    def show_hint(self, message):
        hint_msg = QMessageBox()
        hint_msg.setText(message)
        hint_msg.setWindowTitle("提示")
        hint_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        hint_msg.exec()


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


class CalendarDialog(QDialog, Ui_CalenderDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        pass

class ExportThread(QThread):
    # 定义信号
    finished = pyqtSignal()

    def run(self):
        # 执行耗时操作
        try:
            excel_util = ExcelUtil()
            excel_util.export_to_excel()
            self.finished.emit()  # 发射信号，通知操作完成
        except Exception as e:
            print(e)
            self.finished.emit()  # 即使发生异常也发射信号


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MyExcelMainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
