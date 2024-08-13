from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog

from calendar_dialog import Ui_CalenderDialog
from small_tools import SmallTools


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

