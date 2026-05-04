"""
Test fixtures – spin up the Flask test client against a real PostgreSQL
test database (separate DB from dev so data is isolated).

Required env var:  TEST_DATABASE_URL
Fallback:          postgresql://mego:mego@localhost:5432/mego_test
"""
import os
import pytest

# Point config at the test database BEFORE importing the app
os.environ.setdefault(
    'DATABASE_URL',
    'postgresql://mego:mego@localhost:5432/mego_test'
)
os.environ.setdefault('SECRET_KEY', 'test-secret-key')

from database import init_db, get_db  # noqa: E402 – must come after env var
from app import app as flask_app      # noqa: E402


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    """Create tables once per test session."""
    init_db()
    yield
    # Teardown: wipe all rows so tests are repeatable
    conn = get_db()
    cur = conn.cursor()
    cur.execute('TRUNCATE audit_log, employee_skills, employees, offices, departments RESTART IDENTITY CASCADE')
    conn.commit()
    conn.close()


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False
    with flask_app.test_client() as c:
        yield c
