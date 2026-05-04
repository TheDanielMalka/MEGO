from database import get_db


def get_all_departments(sort_by=None):
    conn = get_db()
    cur = conn.cursor()
    order_map = {'name': 'd.name ASC', 'budget': 'd.budget DESC', 'headcount': 'headcount DESC', 'avg_salary': 'avg_salary DESC'}
    order_sql = 'ORDER BY ' + order_map.get(sort_by, 'd.id ASC')
    cur.execute(f'''
        SELECT d.id, d.name, d.budget, d.manager_name, d.description, d.created_at,
               COUNT(e.id) AS headcount,
               COALESCE(AVG(e.salary), 0) AS avg_salary,
               COALESCE(SUM(e.salary), 0) AS total_salary
        FROM departments d LEFT JOIN employees e ON e.department_id = d.id
        GROUP BY d.id {order_sql}
    ''')
    rows = cur.fetchall(); conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d['budget'] = float(d['budget']) if d['budget'] else 0
        d['avg_salary'] = round(float(d['avg_salary']), 2)
        d['total_salary'] = float(d['total_salary'])
        if d['created_at']: d['created_at'] = d['created_at'].isoformat()
        result.append(d)
    return result


def get_department(dept_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT d.id, d.name, d.budget, d.manager_name, d.description, d.created_at,
               COUNT(e.id) AS headcount,
               COALESCE(AVG(e.salary), 0) AS avg_salary,
               COALESCE(SUM(e.salary), 0) AS total_salary
        FROM departments d LEFT JOIN employees e ON e.department_id = d.id
        WHERE d.id = %s GROUP BY d.id
    ''', (dept_id,))
    row = cur.fetchone(); conn.close()
    if not row: return None
    d = dict(row)
    d['budget'] = float(d['budget']) if d['budget'] else 0
    d['avg_salary'] = round(float(d['avg_salary']), 2)
    d['total_salary'] = float(d['total_salary'])
    if d['created_at']: d['created_at'] = d['created_at'].isoformat()
    return d


def create_department(name, budget, manager_name, description):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO departments (name, budget, manager_name, description) VALUES (%s, %s, %s, %s) RETURNING id',
                (name, float(budget or 0), manager_name or None, description or None))
    new_id = cur.fetchone()['id']; conn.commit(); conn.close()
    return new_id


def update_department(dept_id, name, budget, manager_name, description):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE departments SET name=%s, budget=%s, manager_name=%s, description=%s WHERE id=%s',
                (name, float(budget or 0), manager_name or None, description or None, dept_id))
    conn.commit(); conn.close()


def delete_department(dept_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM departments WHERE id = %s', (dept_id,))
    conn.commit(); conn.close()