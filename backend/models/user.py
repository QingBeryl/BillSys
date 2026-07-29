from extensions import mysql


class User:
    @staticmethod
    def login(username, password):
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT id, username, is_admin FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            user = cur.fetchone()
        finally:
            cur.close()
        return user

    @staticmethod
    def get_all():
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, username, is_admin FROM users")
            users = cur.fetchall()
        finally:
            cur.close()
        return users

    @staticmethod
    def add(username, password):
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
            mysql.connection.commit()
        finally:
            cur.close()

    @staticmethod
    def update(user_id, username, password):
        try:
            cur = mysql.connection.cursor()
            cur.execute("UPDATE users SET username=%s, password=%s WHERE id=%s", (username, password, user_id))
            mysql.connection.commit()
        finally:
            cur.close()

    @staticmethod
    def delete(user_id):
        try:
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
            mysql.connection.commit()
        finally:
            cur.close()
