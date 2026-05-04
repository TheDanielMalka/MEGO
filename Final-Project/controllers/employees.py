from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, Response
import csv, io
from services.employee_service import (
    get_all_employees, get_employee, create_employee,
    update_employee, delete_employee, get_employees_by_office,
    get_all_departments
)
from services.office_service import get_all_offices
from services import audit_service

employees_bp = Blueprint('employees', __name__)


# ── HTML routes ────────────────────────────────────────────────────────────────

@employees_bp.route('/employees')
def employees_list():
    sort_by       = request.args.get('sort_by')
    filter_dept   = request.args.get('filter_dept')
    filter_office = request.args.get('filter_office')
    min_seniority = request.args.get('min_seniority')
    status_filter = request.args.get('status')

    employees   = get_all_employees(sort_by, filter_dept,
                                    filter_office or None,
                                    min_seniority or None,
                                    status_filter or None)
    departments = get_all_departments()
    offices     = get_all_offices()
    return render_template(
        'employees/list.html',
        employees=employees, departments=departments,
        offices=offices, sort_by=sort_by,
        filter_dept=filter_dept, filter_office=filter_office,
        min_seniority=min_seniority, status_filter=status_filter,
    )


@employees_bp.route('/employees/export')
def employees_export():
    employees = get_all_employees(
        request.args.get('sort_by'),
        request.args.get('filter_dept'),
        request.args.get('filter_office') or None,
        request.args.get('min_seniority') or None,
        request.args.get('status') or None,
    )
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Department', 'Hire Date', 'Seniority (yrs)',
                     'Salary', 'Email', 'Phone', 'Status', 'Office Floor', 'Office Room'])
    for e in employees:
        writer.writerow([
            e['id'], e['name'], e.get('department', ''), e['hire_date'],
            e['seniority_years'], e['salary'],
            e.get('email', ''), e.get('phone', ''),
            e.get('status', ''), e.get('office_floor', ''), e.get('office_room', ''),
        ])
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=employees.csv'},
    )


@employees_bp.route('/employees/add', methods=['GET', 'POST'])
def employee_add():
    offices     = get_all_offices()
    departments = get_all_departments()
    if request.method == 'POST':
        skills = [s.strip() for s in request.form.get('skills', '').split(',') if s.strip()]
        emp_id = create_employee(
            name=request.form['name'],
            department_id=request.form.get('department_id') or None,
            hire_date=request.form['hire_date'],
            salary=request.form['salary'],
            office_id=request.form.get('office_id') or None,
            email=request.form.get('email') or None,
            phone=request.form.get('phone') or None,
            status=request.form.get('status', 'active'),
            skills=skills,
        )
        audit_service.log('employee', emp_id, 'CREATE', {'name': request.form['name']})
        return redirect(url_for('employees.employees_list'))
    return render_template('employees/form.html', employee=None,
                           offices=offices, departments=departments, action='add')


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
    offices     = get_all_offices()
    departments = get_all_departments()
    if request.method == 'POST':
        skills = [s.strip() for s in request.form.get('skills', '').split(',') if s.strip()]
        update_employee(
            emp_id=emp_id,
            name=request.form['name'],
            department_id=request.form.get('department_id') or None,
            hire_date=request.form['hire_date'],
            salary=request.form['salary'],
            office_id=request.form.get('office_id') or None,
            email=request.form.get('email') or None,
            phone=request.form.get('phone') or None,
            status=request.form.get('status', 'active'),
            skills=skills,
        )
        audit_service.log('employee', emp_id, 'UPDATE', {'name': request.form['name']})
        return redirect(url_for('employees.employee_detail', emp_id=emp_id))
    return render_template('employees/form.html', employee=emp,
                           offices=offices, departments=departments, action='edit')


@employees_bp.route('/employees/<int:emp_id>/delete', methods=['POST'])
def employee_delete(emp_id):
    emp = get_employee(emp_id)
    if emp:
        audit_service.log('employee', emp_id, 'DELETE', {'name': emp['name']})
    delete_employee(emp_id)
    return redirect(url_for('employees.employees_list'))


# ── REST API ───────────────────────────────────────────────────────────────────

@employees_bp.route('/api/employees', methods=['GET'])
def api_employees_list():
    employees = get_all_employees(
        request.args.get('sort_by'),
        request.args.get('filter_dept'),
        request.args.get('filter_office'),
        request.args.get('min_seniority'),
        request.args.get('status'),
    )
    return jsonify(employees)


@employees_bp.route('/api/employees', methods=['POST'])
def api_employee_create():
    data = request.get_json(force=True)
    skills = data.get('skills', [])
    new_id = create_employee(
        name=data['name'],
        department_id=data.get('department_id'),
        hire_date=data['hire_date'],
        salary=data['salary'],
        office_id=data.get('office_id'),
        email=data.get('email'),
        phone=data.get('phone'),
        status=data.get('status', 'active'),
        skills=skills,
    )
    audit_service.log('employee', new_id, 'CREATE', {'name': data['name']})
    return jsonify(get_employee(new_id)), 201


@employees_bp.route('/api/employees/<int:emp_id>', methods=['GET'])
def api_employee_get(emp_id):
    emp = get_employee(emp_id)
    return jsonify(emp) if emp else (jsonify({'error': 'Not found'}), 404)


@employees_bp.route('/api/employees/<int:emp_id>', methods=['PUT'])
def api_employee_update(emp_id):
    if not get_employee(emp_id):
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json(force=True)
    skills = data.get('skills', [])
    update_employee(
        emp_id=emp_id,
        name=data['name'],
        department_id=data.get('department_id'),
        hire_date=data['hire_date'],
        salary=data['salary'],
        office_id=data.get('office_id'),
        email=data.get('email'),
        phone=data.get('phone'),
        status=data.get('status', 'active'),
        skills=skills,
    )
    audit_service.log('employee', emp_id, 'UPDATE', {'name': data['name']})
    return jsonify(get_employee(emp_id))


@employees_bp.route('/api/employees/<int:emp_id>', methods=['DELETE'])
def api_employee_delete(emp_id):
    emp = get_employee(emp_id)
    if not emp:
        return jsonify({'error': 'Not found'}), 404
    audit_service.log('employee', emp_id, 'DELETE', {'name': emp['name']})
    delete_employee(emp_id)
    return jsonify({'message': 'Deleted'}), 200
