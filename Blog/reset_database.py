import sqlite3
import os

db_path = os.path.abspath("SQLite.db")
print("rebuild in:", db_path)

conn = sqlite3.connect("SQLite.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE user RENAME TO user_old")
except sqlite3.OperationalError:
    print("no old table")

c.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL
);
""")

try:
    c.execute("""
    INSERT INTO user (username, email, password_hash)
    SELECT username, email, password_hash FROM user_old
    WHERE password_hash IS NOT NULL;
    """)
except sqlite3.OperationalError:
    print("no data to copy")

try:
    c.execute("DROP TABLE IF EXISTS user_old;")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()
print("rebuilt yay")