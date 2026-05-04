from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort
from services.department_service import (
    get_all_departments, get_department, create_department,
    update_department, delete_department
)
from services.employee_service import get_all_employees
from services import audit_service

departments_bp = Blueprint('departments', __name__)


# ── HTML routes ────────────────────────────────────────────────────────────────

@departments_bp.route('/departments')
def departments_list():
    sort_by = request.args.get('sort_by')
    depts = get_all_departments(sort_by)
    return render_template('departments/list.html', departments=depts, sort_by=sort_by)


@departments_bp.route('/departments/add', methods=['GET', 'POST'])
def department_add():
    if request.method == 'POST':
        new_id = create_department(
            name=request.form['name'],
            budget=request.form.get('budget') or 0,
            manager_name=request.form.get('manager_name'),
            description=request.form.get('description'),
        )
        audit_service.log('department', new_id, 'CREATE', {'name': request.form['name']})
        return redirect(url_for('departments.departments_list'))
    return render_template('departments/form.html', department=None, action='add')


@departments_bp.route('/departments/<int:dept_id>')
def department_detail(dept_id):
    dept = get_department(dept_id)
    if not dept:
        abort(404)
    employees = [e for e in get_all_employees() if e.get('department_id') == dept_id]
    return render_template('departments/detail.html', department=dept, employees=employees)


@departments_bp.route('/departments/<int:dept_id>/edit', methods=['GET', 'POST'])
def department_edit(dept_id):
    dept = get_department(dept_id)
    if not dept:
        abort(404)
    if request.method == 'POST':
        update_department(
            dept_id=dept_id,
            name=request.form['name'],
            budget=request.form.get('budget') or 0,
            manager_name=request.form.get('manager_name'),
            description=request.form.get('description'),
        )
        audit_service.log('department', dept_id, 'UPDATE', {'name': request.form['name']})
        return redirect(url_for('departments.department_detail', dept_id=dept_id))
    return render_template('departments/form.html', department=dept, action='edit')


@departments_bp.route('/departments/<int:dept_id>/delete', methods=['POST'])
def department_delete(dept_id):
    dept = get_department(dept_id)
    if dept:
        audit_service.log('department', dept_id, 'DELETE', {'name': dept['name']})
    delete_department(dept_id)
    return redirect(url_for('departments.departments_list'))


# ── REST API ───────────────────────────────────────────────────────────────────

@departments_bp.route('/api/departments', methods=['GET'])
def api_departments_list():
    return jsonify(get_all_departments(request.args.get('sort_by')))


@departments_bp.route('/api/departments', methods=['POST'])
def api_department_create():
    data = request.get_json(force=True)
    new_id = create_department(data['name'], data.get('budget', 0),
                               data.get('manager_name'), data.get('description'))
    audit_service.log('department', new_id, 'CREATE', {'name': data['name']})
    return jsonify(get_department(new_id)), 201


@departments_bp.route('/api/departments/<int:dept_id>', methods=['GET'])
def api_department_get(dept_id):
    dept = get_department(dept_id)
    return jsonify(dept) if dept else (jsonify({'error': 'Not found'}), 404)


@departments_bp.route('/api/departments/<int:dept_id>', methods=['PUT'])
def api_department_update(dept_id):
    if not get_department(dept_id):
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json(force=True)
    update_department(dept_id, data['name'], data.get('budget', 0),
                      data.get('manager_name'), data.get('description'))
    audit_service.log('department', dept_id, 'UPDATE', {'name': data['name']})
    return jsonify(get_department(dept_id))


@departments_bp.route('/api/departments/<int:dept_id>', methods=['DELETE'])
def api_department_delete(dept_id):
    dept = get_department(dept_id)
    if not dept:
        return jsonify({'error': 'Not found'}), 404
    audit_service.log('department', dept_id, 'DELETE', {'name': dept['name']})
    delete_department(dept_id)
    return jsonify({'message': 'Deleted'}), 200
