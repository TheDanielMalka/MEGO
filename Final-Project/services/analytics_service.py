from database import get_db


def get_salary_by_department():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT d.name AS department,
               ROUND(AVG(e.salary)::numeric, 2) AS avg_salary,
               COUNT(e.id) AS headcount,
               ROUND(SUM(e.salary)::numeric, 2) AS total_salary
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE e.status = 'active'
        GROUP BY d.name ORDER BY avg_salary DESC
    ''')
    rows = cur.fetchall(); conn.close()
    return [dict(r) | {'avg_salary': float(r['avg_salary']), 'total_salary': float(r['total_salary'])} for r in rows]


def get_office_utilization():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT o.id, o.floor, o.room_number, o.capacity, COUNT(e.id) AS employee_count
        FROM offices o LEFT JOIN employees e ON e.office_id = o.id
        GROUP BY o.id, o.floor, o.room_number, o.capacity
        ORDER BY o.floor, o.room_number
    ''')
    rows = cur.fetchall(); conn.close()
    return [dict(r) for r in rows]


def get_status_distribution():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT status, COUNT(*) AS count FROM employees GROUP BY status')
    rows = cur.fetchall(); conn.close()
    return [dict(r) for r in rows]


def get_headcount_by_year():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT EXTRACT(YEAR FROM hire_date)::int AS year, COUNT(*) AS count
        FROM employees GROUP BY year ORDER BY year
    ''')
    rows = cur.fetchall(); conn.close()
    return [dict(r) for r in rows]


def get_top_earners(limit=5):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT e.id, e.name, e.salary, d.name AS department, e.status
        FROM employees e LEFT JOIN departments d ON e.department_id = d.id
        ORDER BY e.salary DESC LIMIT %s
    ''', (limit,))
    rows = cur.fetchall(); conn.close()
    return [dict(r) | {'salary': float(r['salary'])} for r in rows]


def get_dashboard_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) AS c FROM employees'); total_employees = cur.fetchone()['c']
    cur.execute('SELECT COUNT(*) AS c FROM offices'); total_offices = cur.fetchone()['c']
    cur.execute('SELECT COUNT(*) AS c FROM departments'); total_departments = cur.fetchone()['c']
    cur.execute('SELECT COUNT(*) AS c FROM employees WHERE office_id IS NULL'); unassigned = cur.fetchone()['c']
    cur.execute('''SELECT COUNT(*) AS c FROM (
        SELECT o.id FROM offices o LEFT JOIN employees e ON e.office_id = o.id
        GROUP BY o.id HAVING COUNT(e.id) > o.capacity) sub''')
    overcrowded = cur.fetchone()['c']
    cur.execute('''SELECT COUNT(*) AS c FROM (
        SELECT o.id FROM offices o LEFT JOIN employees e ON e.office_id = o.id
        GROUP BY o.id HAVING COUNT(e.id) < o.capacity) sub''')
    available = cur.fetchone()['c']
    cur.execute('SELECT COALESCE(AVG(salary), 0) AS avg FROM employees WHERE status = %s', ('active',))
    avg_salary = round(float(cur.fetchone()['avg']), 2)
    conn.close()
    return {
        'total_employees': total_employees, 'total_offices': total_offices,
        'total_departments': total_departments, 'unassigned': unassigned,
        'overcrowded': overcrowded, 'available': available, 'avg_salary': avg_salary,
    }