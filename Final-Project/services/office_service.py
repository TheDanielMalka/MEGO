from database import get_db


def get_all_offices(sort_by=None, filter_status=None):
    conn = get_db()
    cur = conn.cursor()

    having_map = {
        'empty':       'COUNT(e.id) = 0',
        'available':   'COUNT(e.id) < o.capacity',
        'overcrowded': 'COUNT(e.id) > o.capacity',
    }
    having_sql = ('HAVING ' + having_map[filter_status]) if filter_status in having_map else ''

    order_map = {
        'floor':          'o.floor ASC',
        'room_number':    'o.room_number ASC',
        'capacity':       'o.capacity DESC',
        'employee_count': 'employee_count DESC',
    }
    order_sql = 'ORDER BY ' + order_map.get(sort_by, 'o.id ASC')

    cur.execute(f'''
        SELECT o.id, o.floor, o.room_number, o.capacity,
               COUNT(e.id) AS employee_count
        FROM offices o
        LEFT JOIN employees e ON e.office_id = o.id
        GROUP BY o.id, o.floor, o.room_number, o.capacity
        {having_sql}
        {order_sql}
    ''')
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_office(office_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT o.id, o.floor, o.room_number, o.capacity,
               COUNT(e.id) AS employee_count
        FROM offices o
        LEFT JOIN employees e ON e.office_id = o.id
        WHERE o.id = %s
        GROUP BY o.id, o.floor, o.room_number, o.capacity
    ''', (office_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_office(floor, room_number, capacity):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO offices (floor, room_number, capacity) VALUES (%s, %s, %s) RETURNING id',
        (int(floor), room_number, int(capacity))
    )
    new_id = cur.fetchone()['id']
    conn.commit()
    conn.close()
    return new_id


def update_office(office_id, floor, room_number, capacity):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        'UPDATE offices SET floor=%s, room_number=%s, capacity=%s WHERE id=%s',
        (int(floor), room_number, int(capacity), office_id)
    )
    conn.commit()
    conn.close()


def delete_office(office_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM offices WHERE id = %s', (office_id,))
    conn.commit()
    conn.close()


def search_offices(q):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT o.id, o.floor, o.room_number, o.capacity, COUNT(e.id) AS employee_count
        FROM offices o
        LEFT JOIN employees e ON e.office_id = o.id
        WHERE CAST(o.floor AS TEXT) ILIKE %s OR o.room_number ILIKE %s
        GROUP BY o.id, o.floor, o.room_number, o.capacity
        ORDER BY o.floor, o.room_number
        LIMIT 50
    ''', (f'%{q}%', f'%{q}%'))
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def assign_employees_to_office(office_id, employee_ids):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE employees SET office_id = NULL WHERE office_id = %s', (office_id,))
    for emp_id in employee_ids:
        cur.execute('UPDATE employees SET office_id = %s WHERE id = %s', (office_id, int(emp_id)))
    conn.commit()
    conn.close()
