import sqlite3
import bcrypt


def login(username, password):

    conn = sqlite3.connect('db_users.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    user = c.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user['username']
        else:
            return False
    else:
        return False


def create(username, password):

    conn = sqlite3.connect('db_users.sqlite')
    c = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    c.execute("INSERT INTO users (username, password, failures, mfa_enabled, mfa_secret) VALUES (?, ?, ?, ?, ?)", (username, hashed_password, 0, 0, ''))

    conn.commit()
    conn.close()


def userlist():

    conn = sqlite3.connect('db_users.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    users = c.execute("SELECT * FROM users").fetchall()

    if not users:
        return []
    else:
        return [ user['username'] for user in users ]


def password_change(username, password):

    conn = sqlite3.connect('db_users.sqlite')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()

    return True


def password_complexity(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    return True