from datetime import date, timedelta
from database import get_db


def _calc_seniority(hire_date_str):
    hire = date.fromisoformat(hire_date_str)
    delta = date.today() - hire
    return {
        'seniority_days': delta.days,
        'seniority_years': round(delta.days / 365.25, 1),
    }


def get_all_employees(sort_by=None, filter_dept=None, filter_office_id=None, min_seniority=None):
    conn = get_db()
    where_clauses = []
    params = []

    if filter_dept:
        where_clauses.append('e.department = ?')
        params.append(filter_dept)

    if filter_office_id:
        where_clauses.append('e.office_id = ?')
        params.append(filter_office_id)

    if min_seniority:
        cutoff = (date.today() - timedelta(days=float(min_seniority) * 365.25)).isoformat()
        where_clauses.append('e.hire_date <= ?')
        params.append(cutoff)

    where_sql = ('WHERE ' + ' AND '.join(where_clauses)) if where_clauses else ''

    order_map = {
        'name':       'e.name ASC',
        'department': 'e.department ASC',
        'hire_date':  'e.hire_date ASC',
        'seniority':  'e.hire_date ASC',
        'salary':     'e.salary DESC',
    }
    order_sql = 'ORDER BY ' + order_map.get(sort_by, 'e.id ASC')

    rows = conn.execute(f'''
        SELECT e.id, e.name, e.department, e.hire_date, e.salary, e.office_id,
               o.floor AS office_floor, o.room_number AS office_room
        FROM employees e
        LEFT JOIN offices o ON e.office_id = o.id
        {where_sql}
        {order_sql}
    ''', params).fetchall()
    conn.close()

    result = []
    for row in rows:
        emp = dict(row)
        emp.update(_calc_seniority(emp['hire_date']))
        result.append(emp)
    return result


def get_employee(emp_id):
    conn = get_db()
    row = conn.execute('''
        SELECT e.id, e.name, e.department, e.hire_date, e.salary, e.office_id,
               o.floor AS office_floor, o.room_number AS office_room
        FROM employees e
        LEFT JOIN offices o ON e.office_id = o.id
        WHERE e.id = ?
    ''', (emp_id,)).fetchone()
    conn.close()
    if not row:
        return None
    emp = dict(row)
    emp.update(_calc_seniority(emp['hire_date']))
    return emp


def create_employee(name, department, hire_date, salary, office_id=None):
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO employees (name, department, hire_date, salary, office_id) VALUES (?, ?, ?, ?, ?)',
        (name, department, hire_date, float(salary), office_id or None)
    )
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_employee(emp_id, name, department, hire_date, salary, office_id=None):
    conn = get_db()
    conn.execute(
        'UPDATE employees SET name=?, department=?, hire_date=?, salary=?, office_id=? WHERE id=?',
        (name, department, hire_date, float(salary), office_id or None, emp_id)
    )
    conn.commit()
    conn.close()


def delete_employee(emp_id):
    conn = get_db()
    conn.execute('DELETE FROM employees WHERE id=?', (emp_id,))
    conn.commit()
    conn.close()


def get_employees_by_office(office_id):
    conn = get_db()
    rows = conn.execute('''
        SELECT id, name, department, hire_date, salary, office_id
        FROM employees
        WHERE office_id = ?
        ORDER BY name ASC
    ''', (office_id,)).fetchall()
    conn.close()
    result = []
    for row in rows:
        emp = dict(row)
        emp.update(_calc_seniority(emp['hire_date']))
        result.append(emp)
    return result


def get_all_departments():
    conn = get_db()
    rows = conn.execute('SELECT DISTINCT department FROM employees ORDER BY department').fetchall()
    conn.close()
    return [r['department'] for r in rows]
