import psycopg2
import psycopg2.extras
from config import DATABASE_URL


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id           SERIAL PRIMARY KEY,
            name         VARCHAR(100) NOT NULL UNIQUE,
            budget       DECIMAL(14,2) DEFAULT 0,
            manager_name VARCHAR(100),
            description  TEXT,
            created_at   TIMESTAMP DEFAULT NOW()
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS offices (
            id          SERIAL PRIMARY KEY,
            floor       INTEGER      NOT NULL,
            room_number VARCHAR(20)  NOT NULL,
            capacity    INTEGER      NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id            SERIAL PRIMARY KEY,
            name          VARCHAR(100) NOT NULL,
            department_id INTEGER      REFERENCES departments(id) ON DELETE SET NULL,
            hire_date     DATE         NOT NULL,
            salary        DECIMAL(12,2) NOT NULL,
            office_id     INTEGER      REFERENCES offices(id) ON DELETE SET NULL,
            email         VARCHAR(150),
            phone         VARCHAR(30),
            status        VARCHAR(20)  DEFAULT 'active'
                          CHECK (status IN ('active','inactive','on_leave'))
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS employee_skills (
            id          SERIAL PRIMARY KEY,
            employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
            skill       VARCHAR(80) NOT NULL,
            UNIQUE (employee_id, skill)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id          SERIAL PRIMARY KEY,
            entity_type VARCHAR(30)  NOT NULL,
            entity_id   INTEGER,
            action      VARCHAR(20)  NOT NULL,
            details     JSONB,
            created_at  TIMESTAMP DEFAULT NOW()
        )
    ''')
    conn.commit()
    conn.close()