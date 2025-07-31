
import sqlite3
from passlib.hash import pbkdf2_sha256

def db_init():

    users = [
        ('admin', pbkdf2_sha256.encrypt('123456')),
        ('john', pbkdf2_sha256.encrypt('Password')),
        ('tim', pbkdf2_sha256.encrypt('Vaider2'))
    ]

    conn = sqlite3.connect('users.sqlite')
    c = conn.cursor()
    c.execute("DROP TABLE users")
    c.execute("CREATE TABLE users (user text, password text, failures int)")

    for u,p in users:
        qlite3
        slib.hash import pbkdf2_sha256
        nit():
        s = [
        ('admin', pbkdf2_sha256.encrypt('123456')),
        ('john', pbkdf2_sha256.encrypt('Password')),
        ('tim', pbkdf2_sha256.encrypt('Vaider2'))
        
         = sqlite3.connect('users.sqlite')
        conn.cursor()
        ecute("DROP TABLE users")
        ecute("CREATE TABLE users (user text, password text, failures int)")
        u,p in users:
        c.execute("INSERT INTO users (user, password, failures) VALUES (?, ?, ?)", (u, p, 0))
        .commit()
        .close()
        e__ == '__main__':
        nit()

    conn.commit()
    conn.close()


if __name__ == '__main__':
    db_init()


