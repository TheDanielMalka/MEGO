from datetime import date, timedelta
import psycopg2.extras
from database import get_db


def _calc_seniority(hire_date_val):
    if isinstance(hire_date_val, str):
        hire = date.fromisoformat(hire_date_val)
    else:
        hire = hire_date_val
    delta = date.today() - hire
    return {
        'seniority_days': delta.days,
        'seniority_years': round(delta.days / 365.25, 1),
    }


def get_all_employees(sort_by=None, filter_dept=None, filter_office_id=None,
                      min_seniority=None, status_filter=None):
    conn = get_db()
    cur = conn.cursor()
    where_clauses = []
    params = []

    if filter_dept:
        where_clauses.append('e.department_id = %s')
        params.append(filter_dept)

    if filter_office_id:
        where_clauses.append('e.office_id = %s')
        params.append(filter_office_id)

    if min_seniority:
        cutoff = (date.today() - timedelta(days=float(min_seniority) * 365.25)).isoformat()
        where_clauses.append('e.hire_date <= %s')
        params.append(cutoff)

    if status_filter:
        where_clauses.append('e.status = %s')
        params.append(status_filter)

    where_sql = ('WHERE ' + ' AND '.join(where_clauses)) if where_clauses else ''

    order_map = {
        'name':       'e.name ASC',
        'department': 'd.name ASC',
        'hire_date':  'e.hire_date ASC',
        'seniority':  'e.hire_date ASC',
        'salary':     'e.salary DESC',
    }
    order_sql = 'ORDER BY ' + order_map.get(sort_by, 'e.id ASC')

    cur.execute(f'''
        SELECT e.id, e.name, e.department_id, d.name AS department,
               e.hire_date, e.salary, e.office_id,
               e.email, e.phone, e.status,
               o.floor AS office_floor, o.room_number AS office_room,
               COALESCE(
                   ARRAY_AGG(es.skill ORDER BY es.skill) FILTER (WHERE es.skill IS NOT NULL),
                   ARRAY[]::text[]
               ) AS skills
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN offices o ON e.office_id = o.id
        LEFT JOIN employee_skills es ON es.employee_id = e.id
        {where_sql}
        GROUP BY e.id, d.name, o.floor, o.room_number
        {order_sql}
    ''', params)
    rows = cur.fetchall()
    conn.close()

    result = []
    for row in rows:
        emp = dict(row)
        emp.update(_calc_seniority(emp['hire_date']))
        emp['hire_date'] = emp['hire_date'].isoformat() if hasattr(emp['hire_date'], 'isoformat') else emp['hire_date']
        emp['salary'] = float(emp['salary'])
        result.append(emp)
    return result


def get_employee(emp_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT e.id, e.name, e.department_id, d.name AS department,
               e.hire_date, e.salary, e.office_id,
               e.email, e.phone, e.status,
               o.floor AS office_floor, o.room_number AS office_room,
               COALESCE(
                   ARRAY_AGG(es.skill ORDER BY es.skill) FILTER (WHERE es.skill IS NOT NULL),
                   ARRAY[]::text[]
               ) AS skills
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN offices o ON e.office_id = o.id
        LEFT JOIN employee_skills es ON es.employee_id = e.id
        WHERE e.id = %s
        GROUP BY e.id, d.name, o.floor, o.room_number
    ''', (emp_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    emp = dict(row)
    emp.update(_calc_seniority(emp['hire_date']))
    emp['hire_date'] = emp['hire_date'].isoformat() if hasattr(emp['hire_date'], 'isoformat') else emp['hire_date']
    emp['salary'] = float(emp['salary'])
    return emp


def create_employee(name, department_id, hire_date, salary, office_id=None,
                    email=None, phone=None, status='active', skills=None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        '''INSERT INTO employees (name, department_id, hire_date, salary, office_id, email, phone, status)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id''',
        (name, department_id or None, hire_date, float(salary),
         office_id or None, email or None, phone or None, status or 'active')
    )
    new_id = cur.fetchone()['id']
    if skills:
        for skill in skills:
            cur.execute(
                'INSERT INTO employee_skills (employee_id, skill) VALUES (%s, %s) ON CONFLICT DO NOTHING',
                (new_id, skill)
            )
    conn.commit()
    conn.close()
    return new_id


def update_employee(emp_id, name, department_id, hire_date, salary,
                    office_id=None, email=None, phone=None, status='active', skills=None):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        '''UPDATE employees
           SET name=%s, department_id=%s, hire_date=%s, salary=%s,
               office_id=%s, email=%s, phone=%s, status=%s
           WHERE id=%s''',
        (name, department_id or None, hire_date, float(salary),
         office_id or None, email or None, phone or None, status or 'active', emp_id)
    )
    if skills is not None:
        cur.execute('DELETE FROM employee_skills WHERE employee_id = %s', (emp_id,))
        for skill in skills:
            cur.execute(
                'INSERT INTO employee_skills (employee_id, skill) VALUES (%s, %s) ON CONFLICT DO NOTHING',
                (emp_id, skill)
            )
    conn.commit()
    conn.close()


def delete_employee(emp_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM employees WHERE id = %s', (emp_id,))
    conn.commit()
    conn.close()


def get_employees_by_office(office_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT e.id, e.name, e.department_id, d.name AS department,
               e.hire_date, e.salary, e.office_id, e.email, e.phone, e.status
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        WHERE e.office_id = %s
        ORDER BY e.name ASC
    ''', (office_id,))
    rows = cur.fetchall()
    conn.close()
    result = []
    for row in rows:
        emp = dict(row)
        emp.update(_calc_seniority(emp['hire_date']))
        emp['hire_date'] = emp['hire_date'].isoformat() if hasattr(emp['hire_date'], 'isoformat') else emp['hire_date']
        emp['salary'] = float(emp['salary'])
        result.append(emp)
    return result


def get_all_departments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM departments ORDER BY name')
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_employees(q):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT e.id, e.name, e.hire_date, e.salary, e.email, e.status,
               d.name AS department,
               o.floor AS office_floor, o.room_number AS office_room
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN offices o ON e.office_id = o.id
        WHERE e.name ILIKE %s OR e.email ILIKE %s OR d.name ILIKE %s
        ORDER BY e.name ASC
        LIMIT 50
    ''', (f'%{q}%', f'%{q}%', f'%{q}%'))
    rows = cur.fetchall()
    conn.close()
    result = []
    for row in rows:
        emp = dict(row)
        emp['hire_date'] = emp['hire_date'].isoformat() if hasattr(emp['hire_date'], 'isoformat') else emp['hire_date']
        emp['salary'] = float(emp['salary'])
        result.append(emp)
    return result
