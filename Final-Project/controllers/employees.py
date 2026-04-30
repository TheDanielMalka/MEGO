from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from services.employee_service import (
    get_all_employees, get_employee, create_employee,
    update_employee, delete_employee, get_employees_by_office, get_all_departments
)
from services.office_service import get_all_offices

employees_bp = Blueprint('employees', __name__)


# ──────────────────────────────────────────────
# HTML routes
# ──────────────────────────────────────────────

@employees_bp.route('/employees')
def employees_list():
    sort_by       = request.args.get('sort_by')
    filter_dept   = request.args.get('filter_dept')
    filter_office = request.args.get('filter_office')
    min_seniority = request.args.get('min_seniority')

    employees   = get_all_employees(sort_by, filter_dept, filter_office or None, min_seniority or None)
    departments = get_all_departments()
    offices     = get_all_offices()
    return render_template(
        'employees/list.html',
        employees=employees,
        departments=departments,
        offices=offices,
        sort_by=sort_by,
        filter_dept=filter_dept,
        filter_office=filter_office,
        min_seniority=min_seniority,
    )


@employees_bp.route('/employees/add', methods=['GET', 'POST'])
def employee_add():
    offices = get_all_offices()
    if request.method == 'POST':
        office_id = request.form.get('office_id') or None
        create_employee(
            name=request.form['name'],
            department=request.form['department'],
            hire_date=request.form['hire_date'],
            salary=request.form['salary'],
            office_id=int(office_id) if office_id else None,
        )
        return redirect(url_for('employees.employees_list'))
    return render_template('employees/form.html', employee=None, offices=offices, action='add')


@employees_bp.route('/employees/<int:emp_id>')
def employee_detail(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        abort(404)
    return render_template('employees/detail.html', employee=emp)


@employees_bp.route('/employees/<int:emp_id>/edit', methods=['GET', 'POST'])
def employee_edit(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        abort(404)
    offices = get_all_offices()
    if request.method == 'POST':
        office_id = request.form.get('office_id') or None
        update_employee(
            emp_id=emp_id,
            name=request.form['name'],
            department=request.form['department'],
            hire_date=request.form['hire_date'],
            salary=request.form['salary'],
            office_id=int(office_id) if office_id else None,
        )
        return redirect(url_for('employees.employee_detail', emp_id=emp_id))
    return render_template('employees/form.html', employee=emp, offices=offices, action='edit')


@employees_bp.route('/employees/<int:emp_id>/delete', methods=['POST'])
def employee_delete(emp_id):
    delete_employee(emp_id)
    return redirect(url_for('employees.employees_list'))


# ──────────────────────────────────────────────
# REST API routes
# ──────────────────────────────────────────────

@employees_bp.route('/api/employees', methods=['GET'])
def api_employees_list():
    sort_by       = request.args.get('sort_by')
    filter_dept   = request.args.get('filter_dept')
    filter_office = request.args.get('filter_office')
    min_seniority = request.args.get('min_seniority')
    employees = get_all_employees(sort_by, filter_dept, filter_office, min_seniority)
    return jsonify(employees)


@employees_bp.route('/api/employees', methods=['POST'])
def api_employee_create():
    data = request.get_json(force=True)
    new_id = create_employee(
        name=data['name'],
        department=data['department'],
        hire_date=data['hire_date'],
        salary=data['salary'],
        office_id=data.get('office_id'),
    )
    return jsonify(get_employee(new_id)), 201


@employees_bp.route('/api/employees/<int:emp_id>', methods=['GET'])
def api_employee_get(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(emp)


@employees_bp.route('/api/employees/<int:emp_id>', methods=['PUT'])
def api_employee_update(emp_id):
    if not get_employee(emp_id):
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json(force=True)
    update_employee(
        emp_id=emp_id,
        name=data['name'],
        department=data['department'],
        hire_date=data['hire_date'],
        salary=data['salary'],
        office_id=data.get('office_id'),
    )
    return jsonify(get_employee(emp_id))


@employees_bp.route('/api/employees/<int:emp_id>', methods=['DELETE'])
def api_employee_delete(emp_id):
    if not get_employee(emp_id):
        return jsonify({'error': 'Not found'}), 404
    delete_employee(emp_id)
    return jsonify({'message': 'Deleted'}), 200
