import os.path
import sqlite3
import datetime

from my_work import MyWork
from small_tools import SmallTools


class DBOperations:

    @staticmethod
    def create_table():
        if not os.path.exists('my_excel.db'):
            conn = sqlite3.connect('my_excel.db')
            c = conn.cursor()
            c.execute('''
            CREATE TABLE IF NOT EXISTS my_work(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                work_date TEXT NOT NULL, -- YYYY-MM-DD
                work_start_time TEXT NOT NULL, -- hh:mm:ss
                work_end_time TEXT NOT NULL, -- hh:mm:ss
                work_sleep_time TEXT NOT NULL,
                work_content TEXT NOT NULL,
                other TEXT NOT NULL
            )
            ''')
            conn.commit()
            conn.close()
            print('Table created successfully')

    @staticmethod
    def get_data(export_date=None):
        print(f'export_date:{export_date}')
        if export_date is None:
            first_day, last_day = SmallTools.get_current_month_first_and_last_day()
        else:
            first_day, last_day = SmallTools.get_first_and_last_day(export_date)

        conn = sqlite3.connect('my_excel.db')
        c = conn.cursor()
        cursor = c.execute('''
                            SELECT id, work_date, work_start_time, work_end_time, work_sleep_time, work_content, other
                            FROM my_work WHERE work_date BETWEEN ? AND ?
                            ''',
                           (first_day, last_day))

        data_list = []
        for row in cursor:
            temp_list = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
            data_list.append(temp_list)
        conn.close()
        return data_list

    @staticmethod
    def add_data(mywork: MyWork):
        connect = sqlite3.connect('my_excel.db')
        c = connect.cursor()
        command = '''
            INSERT INTO my_work (work_date, work_start_time, work_end_time, work_sleep_time, work_content, other)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        print(f'command:{command}')
        print(f'mywork: {mywork.work_date}, {mywork.work_start_time}, {mywork.work_end_time}, {mywork.work_sleep_time}, '
              f'{mywork.work_content}, other:{mywork.other}')
        c.execute(command, (mywork.work_date, mywork.work_start_time, mywork.work_end_time, mywork.work_sleep_time,
                  mywork.work_content, mywork.other))
        print('command executed successfully')
        connect.commit()
        connect.close()

    @staticmethod
    def del_data(row_id):
        connect = sqlite3.connect('my_excel.db')
        c = connect.cursor()
        command = '''
            DELETE FROM my_work WHERE id = ?
        '''
        print(f'command:{command}')
        print(f'id:{row_id}')
        c.execute(command, (row_id, ))
        connect.commit()
        connect.close()

    @staticmethod
    def up_data(row_id, data):
        connect = sqlite3.connect('my_excel.db')
        c = connect.cursor()
        command = '''
            UPDATE my_work
            SET work_start_time = ?, work_end_time = ?, work_content = ?
            WHERE id=?;
        '''
        print(f'command:{command}')
        print(f'id:{row_id}')
        c.execute(command, (data['value1'], data['value2'], data['value3'], row_id))
        connect.commit()
        connect.close()

    @staticmethod
    def insert_data_into_db(data_list):
        connect = sqlite3.connect('my_excel.db')
        c = connect.cursor()

        # 获取当前的年份和月份
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month

        for data in data_list:
            print(f'data: {data}')
            # 提取日期部分
            day = int(data[0].split('/')[1])  # 假设输入的日期格式为 "8/1", "8/2", 等

            # 将日期转换为当前的年/月/日
            work_date = datetime.datetime(current_year, current_month, day).strftime("%Y/%m/%d")
            work_content = " ".join(data[1:])
            work_start_time = f'{work_date} 09:00:00'
            work_end_time = f'{work_date} 18:00:00'
            work_sleep_time = "1"
            other = "默认备注"
            print(f'''
            work_date:{work_date}, work_start_time:{work_start_time}, work_end_time:{work_end_time},
            work_sleep_time:{work_sleep_time},other:{other}
            ''')
            c.execute('''
                INSERT INTO my_work (work_date, work_start_time, work_end_time, work_sleep_time, work_content, other)
                VALUES (?, ?, ?, ?, ?, ?);
            ''', (work_date, work_start_time, work_end_time, work_sleep_time, work_content, other))

        connect.commit()
        connect.close()

    @staticmethod
    def delete_data_all():
        connect = sqlite3.connect('my_excel.db')
        c = connect.cursor()
        command = '''
            DELETE FROM my_work
        '''
        c.execute(command)
        connect.commit()
        connect.close()
