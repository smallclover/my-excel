import datetime

from PIL import Image, ImageDraw, ImageFont
from PyQt6 import QtCore
from PyQt6.QtCore import QDate, QThread, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QProgressDialog

from ui_cls.add_dialog_cls import AddDialog
from ui_cls.calendar_dialog_cls import CalendarDialog
from ui_cls.import_dialog_cls import ImportDialog
from db_op import DBOperations
from excel_util import ExcelUtil
from main import Ui_MainWindow
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
        self.clearButton.clicked.connect(self.clear_table)

        self.genImageButton.clicked.connect(self.gen_img)

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

    def clear_table(self):
        try:
            hint_msg = QMessageBox()
            hint_msg.setText('是否确定要清空！！！！')
            hint_msg.setWindowTitle("提示")
            hint_msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

            # 显示消息框并等待用户输入
            user_response = hint_msg.exec()

            # 如果用户点击“确定”按钮，执行清空操作
            if user_response == QMessageBox.StandardButton.Ok:
                DBOperations.delete_data_all()
                self.refresh_table()
            else:
                print("操作已取消")
        except Exception as e:
            print(e)


    def show_hint(self, message):
        hint_msg = QMessageBox()
        hint_msg.setText(message)
        hint_msg.setWindowTitle("提示")
        hint_msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        hint_msg.exec()

    def gen_img(self):
        try:
            # 读取图片
            image_path = 'syonin_2.png'
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            # 设置字体（你需要指定一个系统上存在的字体路径）
            font_path = "C:/Windows/Fonts/SimHei.ttf"
            font_size = 30
            font = ImageFont.truetype(font_path, font_size)

            # 写入日期 (yyyy/MM/dd) 在中间区域
            date_text = "2024/08/15"  # 替换为你需要的日期
            date_position = (30, 95)  # 根据实际位置调整
            draw.text(date_position, date_text, font=font, fill="red")

            # 写入名字在下半区域
            name_text = "三页半"  # 替换为你需要的名字
            name_position = (60, 140)  # 宽度60根据两个或者三个人名需要细微调整
            draw.text(name_position, name_text,font=font,fill="red")

            # 获取图像DPI
            dpi = img.info.get('dpi', (300, 300))  # 如果未指定DPI，默认为300

            # 计算所需的宽度
            cm_to_inch = 0.393701
            width_cm = 2.16
            width_inch = width_cm * cm_to_inch
            new_width = int(width_inch * dpi[0])

            # 计算新高度保持比例
            width_percent = (new_width / float(img.size[0]))
            new_height = int((float(img.size[1]) * width_percent))

            # 调整图像大小
            img = img.resize((new_width, new_height), Image.LANCZOS)
            # 保存修改并缩放后的图片
            resized_output_image_path = 'modified_stamp_1.png'
            img.save(resized_output_image_path)
            print("已保存带有参考线的图像")
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
