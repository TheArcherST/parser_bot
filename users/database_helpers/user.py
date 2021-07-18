import sqlite3 as sql
from typing import List


class UserInfo:
    def __init__(self, user_id, username=None, first_name=None, last_name=None):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


class UsersKeeper:
    path = 'data/users.db'

    def __init__(self):
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_id INT NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT

                )""")
        connection.commit()

        cursor.close()
        connection.close()

    def update(self, user_id, username=None, first_name=None, last_name=None):
        if user_id in self.get_user_ids():
            return self.overwrite(user_id, username, first_name, last_name)
        else:
            return self.write(user_id, username, first_name, last_name)

    def overwrite(self, user_id, username=None, first_name=None, last_name=None):
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute("""UPDATE users SET username = ?, first_name = ?, last_name = ? WHERE user_id = ?""",
         (username, first_name, last_name, user_id))
        connection.commit()

        cursor.close()
        connection.close()

    def write(self, user_id, username=None, first_name=None, last_name=None):
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO users VALUES (?, ?, ?, ?)""",
         (user_id, username, first_name, last_name))
        connection.commit()

        cursor.close()
        connection.close()

    def get_info(self, user_id) -> UserInfo:
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""",
         (user_id,))
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return UserInfo(*data[0])

    def get_user_ids(self) -> List[int]:
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute(f"""SELECT (user_id) FROM users""")
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        result = [i[0] for i in data]

        return result
