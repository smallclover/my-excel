import datetime
import sys
from idlelib.help_about import AboutDialog

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QDate, QTimer, QThread, pyqtSignal, QDateTime, QTime
from PyQt6.QtWidgets import QMainWindow, QDialog, QTableWidgetItem, QMessageBox, QProgressDialog, QFileDialog

from calendar_dialog import Ui_CalenderDialog
from db_op import DBOperations
from excel_util import ExcelUtil
from main import Ui_MainWindow
from add_dialog import Ui_Dialog
from import_dialog import Ui_ImportDialog
from my_work import MyWork
from small_tools import SmallTools


class MyExcelMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        DBOperations.create_table()
        self.init_ui()
        self.init_table()

    def init_ui(self):
        current_date = QDate.currentDate()
        target_date = current_date.toString("yyyy/MM/dd dddd")
        self.currentDateInput.setText(SmallTools.get_date_to_jp(target_date))
        self.exportDateInput.setText(SmallTools.get_date_to_jp(target_date))

        # 获取当前月份并设置为默认选中项
        current_month = QDate.currentDate().month()
        self.exportMonthcomboBox.setCurrentIndex(current_month - 1)  # 索引从 0 开始

        self.addButton.clicked.connect(self.add_dialog)
        self.exportButton.clicked.connect(self.export_to_excel)
        self.delButton.clicked.connect(self.del_dialog)
        self.editButton.clicked.connect(self.edit_dialog)
        self.importButton.clicked.connect(self.import_dialog)
        self.AboutMenu.triggered.connect(self.about_dialog)
        self.chooseExportDateButton.clicked.connect(self.show_calendar)
        self.exportMonthcomboBox.currentIndexChanged.connect(self.get_current_month_data)

    def init_table(self):
        data_list = DBOperations.get_data()
        self.load_data(data_list)

    def load_data(self, data_list):
        self.tableWidget.setRowCount(len(data_list))
        for i, row in enumerate(data_list):
            # print(f'row:{row}')
            for j, value in enumerate(row):
                if j == 2 or j == 3:  # 第三列是 work_start_time，第四列是 work_end_time
                    # 假设 value 是 'hh:mm:ss' 格式的字符串
                    formatted_time = datetime.datetime.strptime(value, "%Y/%m/%d %H:%M:%S").strftime("%H:%M:%S")
                    self.tableWidget.setItem(i, j, QTableWidgetItem(formatted_time))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

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
        dialog.chosen_date.connect(self.update_export_date)
        dialog.exec()

    def export_to_excel(self):
        # 创建并显示“导出中”提示框
        self.export_dialog = QProgressDialog("导出中，请稍候...", None, 0, 0, self)
        self.export_dialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.export_dialog.setMinimumDuration(0)  # 立即显示提示框
        self.export_dialog.show()

        export_date_full = self.exportMonthcomboBox.currentText()

        # 创建并启动后台线程
        self.export_thread = ExportThread(export_date_full)
        self.export_thread.finished.connect(self.on_export_finished)
        self.export_thread.start()

    def on_export_finished(self):
        # 关闭“导出中”提示框
        self.export_dialog.hide()
        self.show_hint("导出成功")

    def refresh_table(self, date_string=None):
        self.tableWidget.setRowCount(0)
        # 清除表格内容
        self.tableWidget.clearContents()
        # 获取新数据
        data_list = DBOperations.get_data(date_string)
        # 重新加载新数据
        self.load_data(data_list)

    def update_export_date(self, date_string):
        self.exportDateInput.setText(date_string)
        export_date = date_string.split(' ')[0]
        self.refresh_table(export_date)

    def get_current_month_data(self):
        current_month = self.exportMonthcomboBox.currentText()
        self.refresh_table(current_month)

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
                # 获取当前日期
                current_date = QDate.currentDate()
                formatted_date = current_date.toString("yyyy/MM/dd")
                # 获取开始时间和结束时间 (hh:mm:ss)
                start_time = self.work_start_time.currentText()
                end_time = self.work_end_time.currentText()
                print(f'start_time:{start_time}, end_time:{end_time}')

                # 将时间字符串解析为 QTime 对象
                start_time_obj = QTime.fromString(start_time, "hh:mm:ss")
                end_time_obj = QTime.fromString(end_time, "hh:mm:ss")

                # 确保时间对象有效
                if not start_time_obj.isValid():
                    raise ValueError(f"start_time_obj:{start_time_obj} Invalid time format")
                if not end_time_obj.isValid():
                    raise ValueError(f"end_time_obj:{end_time_obj} Invalid time format")

                # 将日期和时间组合在一起
                formatted_start_time = QDateTime(current_date, start_time_obj).toString("yyyy/MM/dd hh:mm:ss")
                formatted_end_time = QDateTime(current_date, end_time_obj).toString("yyyy/MM/dd hh:mm:ss")

                print(f'formatted_start_time: {formatted_start_time}, formatted_end_time: {formatted_end_time}')

                # 创建 MyWork 对象
                my_work = MyWork(formatted_date, formatted_start_time, formatted_end_time, self.work_content.toPlainText())

                DBOperations.add_data(my_work)
                self.show_hint('追加成功')
            elif self.action_type == 2:
                # 获取当前日期
                current_date = QDate.currentDate()
                # 获取开始时间和结束时间 (hh:mm:ss)
                start_time = self.work_start_time.currentText()
                end_time = self.work_end_time.currentText()
                print(f'start_time:{start_time}, end_time:{end_time}')

                # 将时间字符串解析为 QTime 对象
                start_time_obj = QTime.fromString(start_time, "hh:mm:ss")
                end_time_obj = QTime.fromString(end_time, "hh:mm:ss")

                # 确保时间对象有效
                if not start_time_obj.isValid():
                    raise ValueError(f"start_time_obj:{start_time_obj} Invalid time format")
                if not end_time_obj.isValid():
                    raise ValueError(f"end_time_obj:{end_time_obj} Invalid time format")

                # 将日期和时间组合在一起
                formatted_start_time = QDateTime(current_date, start_time_obj).toString("yyyy/MM/dd hh:mm:ss")
                formatted_end_time = QDateTime(current_date, end_time_obj).toString("yyyy/MM/dd hh:mm:ss")

                print(f'formatted_start_time: {formatted_start_time}, formatted_end_time: {formatted_end_time}')
                DBOperations.up_data(self.row_id, {
                    'value1': formatted_start_time,
                    'value2': formatted_end_time,
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
    chosen_date = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.show_date()
        self.calendarWidget.clicked.connect(self.show_date)
        self.okButton.clicked.connect(self.choose_date)
        self.calendarWidget.activated.connect(self.date_double_clicked)

    def show_date(self):
        # 获取选中的日期
        selected = self.calendarWidget.selectedDate()

        # 获取完整的日期字符串
        date_string = selected.toString("yyyy/MM/dd dddd")

        # 设置标签的文本
        self.choosedDateLabel.setText(SmallTools.get_date_to_jp(date_string))

    def choose_date(self):
        try:
            self.chosen_date.emit(self.choosedDateLabel.text())
            self.accept()
        except Exception as e:
            print(e)

    def date_double_clicked(self):
        try:
            # 获取选中的日期
            selected = self.calendarWidget.selectedDate()

            # 获取完整的日期字符串
            date_string = selected.toString("yyyy/MM/dd dddd")

            self.chosen_date.emit(SmallTools.get_date_to_jp(date_string))
            self.accept()
        except Exception as e:
            print(e)


class ExportThread(QThread):

    def __init__(self, export_date):
        super().__init__()
        self.export_date = export_date

    # 定义信号
    finished = pyqtSignal()

    def run(self):
        # 执行耗时操作
        try:
            excel_util = ExcelUtil()
            excel_util.export_to_excel(self.export_date)
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
