from PyQt6 import QtCore
from PyQt6.QtCore import QDate, QTime, QDateTime
from PyQt6.QtWidgets import QDialog, QMessageBox

from add_dialog import Ui_Dialog
from db_op import DBOperations
from my_work import MyWork


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

