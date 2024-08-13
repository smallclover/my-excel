import calendar
import datetime

import jpholiday
from PyQt6.QtCore import QDate


class SmallTools:

    @staticmethod
    def get_date_to_jp(target_date=None):

        if target_date is None:
            current_date = QDate.currentDate()
            target_date = current_date.toString("yyyy/MM/dd dddd")

        # 替换星期几为 "曜日"
        weekday_map = {
            "Monday": "月曜日",
            "Tuesday": "火曜日",
            "Wednesday": "水曜日",
            "Thursday": "木曜日",
            "Friday": "金曜日",
            "Saturday": "土曜日",
            "Sunday": "日曜日"
        }

        # 替换英文星期几为对应的日文"曜日"
        for eng_day, jp_day in weekday_map.items():
            if eng_day in target_date:
                target_date = target_date.replace(eng_day, jp_day)
                break
        return target_date

    @staticmethod
    def get_first_and_last_day(date_str):
        # 解析字符串得到年份和月份
        year, month = map(int, date_str.split('/'))

        # 获取指定月份的第一天
        first_day = datetime.date(year, month, 1)

        # 获取指定月份的最后一天
        last_day = datetime.date(year, month, calendar.monthrange(year, month)[1])

        return SmallTools.format_date(first_day), SmallTools.format_date(last_day)

    @staticmethod
    def get_current_month_first_and_last_day():
        # 获取当前日期
        today = datetime.date.today()

        # 获取当前月份的第一天
        first_day = datetime.date(today.year, today.month, 1)

        # 获取当前月份的最后一天
        last_day = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        return SmallTools.format_date(first_day), SmallTools.format_date(last_day)

    @staticmethod
    def format_date(date):
        return date.strftime("%Y/%m/%d")

    @staticmethod
    def is_holiday_or_weekend(date):
        # 判断是否是周末
        if date.weekday() >= 5:  # 5表示周六，6表示周日
            return True
        # 判断是否是祝日
        if jpholiday.is_holiday(date):
            return True
        return False
