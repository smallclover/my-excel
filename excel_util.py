import os

import openpyxl
import jpholiday
from datetime import datetime, timedelta
import win32com.client as win32
from openpyxl.utils import get_column_letter

from db_op import DBOperations


class ExcelUtil:

    def export_to_excel(self, input_file='template_1.xlsm', output_file='./wangshun.xlsx', sheet_name='勤務報告'):
        # 读取现有工作簿
        wb = openpyxl.load_workbook(input_file)
        ws = wb.active

        if sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
        else:
            raise ValueError(f"Sheet '{sheet_name}' does not exist in the workbook.")

        # 获取当前日期
        today = datetime.today()
        first_day = today.replace(day=1)
        next_month = first_day.replace(day=28) + timedelta(days=4)
        last_day = next_month - timedelta(days=next_month.day)

        # 获取开始单元格的行和列
        start_row, start_col = openpyxl.utils.cell.coordinate_to_tuple('B10')

        # 获取源单元格的格式
        source_date_cell = ws.cell(row=start_row, column=start_col)
        source_weekday_cell = ws.cell(row=start_row, column=start_col + 1)
        source_relax_cell = ws.cell(row=start_row, column=start_col + 2)

        # 定义日本曜日列表
        japanese_weekdays = ['月', '火', '水', '木', '金', '土', '日']

        def get_relax_cell_value(date, name):
            """根据日期和星期名称获取D列单元格的值"""
            if jpholiday.is_holiday(date):
                return '祝日'  # 节假日
            elif name in ['土', '日']:
                return '休日'  # 周六或周日
            else:
                return ''  # 空白

        def copy_cell_format(source_cell, target_cell):
            target_cell.font = source_cell.font.copy()
            target_cell.fill = source_cell.fill.copy()
            target_cell.border = source_cell.border.copy()
            target_cell.alignment = source_cell.alignment.copy()

        current_date = first_day
        while current_date <= last_day:
            date_cell = ws.cell(row=start_row, column=start_col, value=current_date)
            copy_cell_format(source_date_cell, date_cell)
            date_cell.number_format = source_date_cell.number_format

            # 填写对应的日本曜日
            weekday_cell_val = japanese_weekdays[current_date.weekday()]
            weekday_cell = ws.cell(row=start_row, column=start_col + 1, value=weekday_cell_val)
            copy_cell_format(source_weekday_cell, weekday_cell)

            # 获取D列的值
            relax_cell_val = get_relax_cell_value(current_date, weekday_cell_val)
            relax_cell = ws.cell(row=start_row, column=start_col + 2, value=relax_cell_val)
            copy_cell_format(source_relax_cell, relax_cell)

            current_date += timedelta(days=1)
            start_row += 1  # 向下移动到下一行

        # 获取合并单元格的起始单元格
        e2_cell = ws['E2']

        # 将值设置为 datetime 对象
        # 如果是设置字符串他并不会对格式生效
        # 值的类型会影响到格式，请注意
        e2_cell.value = datetime.strptime(first_day.strftime('%Y/%m/%d'), '%Y/%m/%d')

        # 恢复样式
        e2_cell.font = e2_cell.font.copy()
        e2_cell.fill = e2_cell.fill.copy()
        e2_cell.border = e2_cell.border.copy()
        e2_cell.alignment = e2_cell.alignment.copy()
        e2_cell.number_format = '[$-411]ggge"年"m"月"'
        print(e2_cell.number_format)

        data_list = DBOperations.get_data()
        e_col = []
        f_col = []
        g_col = []
        i_col = []
        j_col = []

        for row in data_list:
            # 根据实际的数据结构调整索引
            e_col.append(row[2])  # 开始时间
            f_col.append(row[3])  # 结束时间
            g_col.append(row[4])  # 休息时间

            try:
                start_time = datetime.strptime(row[2], "%H:%M:%S")
                end_time = datetime.strptime(row[3], "%H:%M:%S")
                time_diff = end_time - start_time
                # 将时间差转换为小时数（取整数）
                time_diff_hours = time_diff.seconds // 3600  # 转换为小时并取整
                # 休息时间
                rest_hours = int(row[4]) if row[4] else 0
                i_col.append(str(time_diff_hours-rest_hours))  # 转换为字符串并添加到列表
            except ValueError:
                i_col.append("")

            j_col.append(row[5])  # 内容

        for idx, (e_value, f_value, g_value, i_value, j_value) in enumerate(
                zip(e_col, f_col, g_col, i_col, j_col)):
            ws.cell(row=10 + idx, column=openpyxl.utils.cell.column_index_from_string('E'), value=e_value)
            ws.cell(row=10 + idx, column=openpyxl.utils.cell.column_index_from_string('F'), value=f_value)
            ws.cell(row=10 + idx, column=openpyxl.utils.cell.column_index_from_string('G'), value=g_value)
            ws.cell(row=10 + idx, column=openpyxl.utils.cell.column_index_from_string('I'), value=i_value)
            ws.cell(row=10 + idx, column=openpyxl.utils.cell.column_index_from_string('J'), value=j_value)

        # 保存到新的文件
        wb.save(output_file)

        self.excel_to_pdf('wangshun.xlsx', '勤務報告', 'output.pdf')


    def excel_to_pdf(self, excel_file, sheet_name, pdf_file):
        # 获取当前工作目录
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # 组合文件的完整路径
        excel_path = os.path.join(current_directory, excel_file)
        pdf_path = os.path.join(current_directory, pdf_file)

        # 创建Excel应用程序对象
        excel = win32.Dispatch('Excel.Application')

        # 打开Excel文件
        workbook = excel.Workbooks.Open(excel_path)

        # 获取指定的工作表
        sheet = workbook.Sheets(sheet_name)

        # 禁用Excel的警告弹窗
        excel.DisplayAlerts = False

        # 将工作表导出为PDF
        sheet.ExportAsFixedFormat(0, pdf_path)

        # 关闭工作簿
        workbook.Close(SaveChanges=False)

        # 退出Excel应用程序
        excel.Quit()


