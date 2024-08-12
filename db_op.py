import os.path
import sqlite3

from my_work import MyWork


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
    def get_data():
        conn = sqlite3.connect('my_excel.db')
        c = conn.cursor()
        cursor = c.execute('SELECT * FROM my_work')

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

        for data in data_list:
            work_date = data[0]
            work_content = " ".join(data[1:])
            work_start_time = "09:00"
            work_end_time = "18:00"
            work_sleep_time = "1"
            other = "默认备注"

            c.execute('''
                INSERT INTO my_work (work_date, work_start_time, work_end_time, work_sleep_time, work_content, other)
                VALUES (?, ?, ?, ?, ?, ?);
            ''', (work_date, work_start_time, work_end_time, work_sleep_time, work_content, other))

        connect.commit()
        connect.close()
