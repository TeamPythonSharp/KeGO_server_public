import sqlite3


class SqlStudents:

    def __init__(self):
        self.connect = sqlite3.connect('Data_users.db', check_same_thread=False)

    def log_in(self, info):
        cursor = self.connect.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Students (
            chat_id INTEGER PRIMARY KEY,
            Name_Student TEXT,
            Email TEXT,
            ws_id INTEGER,
            expectations TEXT
        )""")
        # cursor.execute("""ALTER TABLE Students ADD Name_Student TEXT""")
        self.connect.commit()
        chat_id = info[0]
        name_user = info[1]
        email = info[2]
        cursor.execute(f"SELECT chat_id FROM Students WHERE chat_id = {chat_id}")
        data = cursor.fetchone()
        if data is None:
            cursor.execute(f"""INSERT INTO Students (chat_id,Name_Student,Email) 
            VALUES({chat_id},'{name_user}','{email}');""")

            self.connect.commit()
            return 'новый пользователь'
        else:
            cursor.execute(f"""UPDATE Students SET 
                        Name_Student = '{name_user}', Email = '{email}'
                        WHERE chat_id = {chat_id};""")
            self.connect.commit()
            return 'такой пользователь есть в бд'

    def check_up(self, chat_id):
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT chat_id FROM Students WHERE chat_id = {chat_id}")
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            cursor.execute(f"SELECT Name_Student FROM Students WHERE chat_id = {chat_id}")
            name = cursor.fetchone()
            return name[0]

    def update_data_in_table(self, info, column, chat_id):
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT '{column}' FROM Students WHERE chat_id = {chat_id}")
        cursor.execute(f"""UPDATE Students SET 
                                '{column}' = '{info}'
                                WHERE chat_id = {chat_id};""")
        self.connect.commit()

    def get_data_in_table(self, column, chat_id):
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT {column} FROM Students WHERE chat_id = {chat_id}")
        data = cursor.fetchone()
        return data


class ReportsId:

    def __init__(self, chat_id):
        self.connect = sqlite3.connect('Data_users.db', check_same_thread=False)
        self.chat_id = chat_id

    def task_update(self, task, Report):
        cursor = self.connect.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS id_{self.chat_id} (
            Tasks TEXT PRIMARY KEY,
            Method TEXT,
            Report TEXT
        )""")
        self.connect.commit()

        cursor.execute(f"SELECT tasks FROM id_{self.chat_id} WHERE tasks = '{task}'")
        data = cursor.fetchone()
        if data is None:
            cursor.execute(f"""INSERT INTO id_{self.chat_id} (Tasks,Method,Report) 
            VALUES('{task}','suitcase','{Report}');""")

            self.connect.commit()
            # return 'новый пользователь'
        else:
            cursor.execute(f"""UPDATE id_{self.chat_id} SET 
                        Tasks = '{task}', Method = 'suitcase', Report = '{Report}'
                        WHERE Tasks = '{task}';""")
            self.connect.commit()
            # return 'такой пользователь есть в бд'

    def get_all_tasks(self):
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT Tasks FROM id_{self.chat_id}")
        data = cursor.fetchall()
        return data

    def get_all_reports(self):
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT Report FROM id_{self.chat_id}")
        data = cursor.fetchall()
        return data
