import psycopg2.extras
from database import get_db


def log(entity_type, entity_id, action, details=None):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO audit_log (entity_type, entity_id, action, details) VALUES (%s, %s, %s, %s)',
            (entity_type, entity_id, action, psycopg2.extras.Json(details) if details else None)
        )
        conn.commit(); conn.close()
    except Exception:
        pass


def get_recent(limit=50):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, entity_type, entity_id, action, details, created_at FROM audit_log ORDER BY created_at DESC LIMIT %s', (limit,))
    rows = cur.fetchall(); conn.close()
    result = []
    for r in rows:
        row = dict(r)
        if row['created_at']:
            row['created_at'] = row['created_at'].isoformat()
        result.append(row)
    return result