<<<<<<< HEAD
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS logs
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                result TEXT,
                confidence REAL)''')

    conn.commit()
=======
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS logs
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                result TEXT,
                confidence REAL)''')

    conn.commit()
>>>>>>> ff7d1f8aeb76fd3585a1b833f713ba1743e2d869
    conn.close()