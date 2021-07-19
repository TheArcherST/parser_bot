import sqlite3 as sql
from typing import List


class UserConfig:
    def __init__(self, spce = None):
        if spce is None:
            spce = False

        self.spce = spce


class UserConfigsKeeper:
    path = 'data/users.db'

    def __init__(self):
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS configs (
                    user_id INT NOT NULL,
                    spce BOOLEAN DEFAULT false
                )""")
        connection.commit()

        cursor.close()
        connection.close()

    def update(self, user_id, spce: bool = None):
        if user_id in self.get_user_ids():
            return self.overwrite(user_id, spce)
        else:
            return self.write(user_id, spce)

    def overwrite(self, user_id, spce: bool = None):
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute("""UPDATE configs SET spce = ? WHERE user_id = ?""",
         (spce, user_id))
        connection.commit()

        cursor.close()
        connection.close()

    def write(self, user_id, spce: bool = None):
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO configs VALUES (?, ?)""",
         (user_id, spce))
        connection.commit()

        cursor.close()
        connection.close()

    def get_config(self, user_id) -> UserConfig:
        if user_id not in self.get_user_ids():
            self.write(user_id)

        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute(f"""SELECT * FROM configs WHERE user_id = ?""",
         (user_id,))
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        return UserConfig(*data[1:])

    def get_user_ids(self) -> List[int]:
        connection = sql.connect(self.path)
        cursor = connection.cursor()

        cursor.execute(f"""SELECT (user_id) FROM configs""")
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        result = [i[0] for i in data]

        return result
