from database import get_db


def get_all_offices(sort_by=None, filter_status=None):
    conn = get_db()

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

    rows = conn.execute(f'''
        SELECT o.id, o.floor, o.room_number, o.capacity,
               COUNT(e.id) AS employee_count
        FROM offices o
        LEFT JOIN employees e ON e.office_id = o.id
        GROUP BY o.id
        {having_sql}
        {order_sql}
    ''').fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_office(office_id):
    conn = get_db()
    row = conn.execute('''
        SELECT o.id, o.floor, o.room_number, o.capacity,
               COUNT(e.id) AS employee_count
        FROM offices o
        LEFT JOIN employees e ON e.office_id = o.id
        WHERE o.id = ?
        GROUP BY o.id
    ''', (office_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_office(floor, room_number, capacity):
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO offices (floor, room_number, capacity) VALUES (?, ?, ?)',
        (int(floor), room_number, int(capacity))
    )
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_office(office_id, floor, room_number, capacity):
    conn = get_db()
    conn.execute(
        'UPDATE offices SET floor=?, room_number=?, capacity=? WHERE id=?',
        (int(floor), room_number, int(capacity), office_id)
    )
    conn.commit()
    conn.close()


def delete_office(office_id):
    conn = get_db()
    conn.execute('DELETE FROM offices WHERE id=?', (office_id,))
    conn.commit()
    conn.close()


def assign_employees_to_office(office_id, employee_ids):
    conn = get_db()
    conn.execute('UPDATE employees SET office_id = NULL WHERE office_id = ?', (office_id,))
    for emp_id in employee_ids:
        conn.execute('UPDATE employees SET office_id = ? WHERE id = ?', (office_id, int(emp_id)))
    conn.commit()
    conn.close()
