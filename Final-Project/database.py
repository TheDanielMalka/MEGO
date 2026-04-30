import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS offices (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            floor       INTEGER NOT NULL,
            room_number TEXT    NOT NULL,
            capacity    INTEGER NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            department  TEXT    NOT NULL,
            hire_date   TEXT    NOT NULL,
            salary      REAL    NOT NULL,
            office_id   INTEGER,
            FOREIGN KEY (office_id) REFERENCES offices(id) ON DELETE SET NULL
        )
    ''')
    conn.commit()
    conn.close()
