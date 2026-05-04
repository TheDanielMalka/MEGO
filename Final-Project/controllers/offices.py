from flask import Blueprint, render_template, request, redirect, url_for, jsonify, abort, Response
import csv, io
from services.office_service import (
    get_all_offices, get_office, create_office,
    update_office, delete_office, assign_employees_to_office
)
from services.employee_service import get_all_employees, get_employees_by_office
from services import audit_service

offices_bp = Blueprint('offices', __name__)


# ── HTML routes ────────────────────────────────────────────────────────────────

@offices_bp.route('/offices')
def offices_list():
    sort_by       = request.args.get('sort_by')
    filter_status = request.args.get('filter_status')
    offices = get_all_offices(sort_by, filter_status)
    return render_template('offices/list.html', offices=offices,
                           sort_by=sort_by, filter_status=filter_status)


@offices_bp.route('/offices/export')
def offices_export():
    offices = get_all_offices()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Floor', 'Room Number', 'Capacity', 'Employees', 'Status'])
    for o in offices:
        if o['employee_count'] > o['capacity']:
            status = 'Overcrowded'
        elif o['employee_count'] == 0:
            status = 'Empty'
        elif o['employee_count'] < o['capacity']:
            status = 'Available'
        else:
            status = 'Full'
        writer.writerow([o['id'], o['floor'], o['room_number'],
                         o['capacity'], o['employee_count'], status])
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=offices.csv'},
    )


@offices_bp.route('/offices/add', methods=['GET', 'POST'])
def office_add():
    if request.method == 'POST':
        new_id = create_office(
            floor=request.form['floor'],
            room_number=request.form['room_number'],
            capacity=request.form['capacity'],
        )
        audit_service.log('office', new_id, 'CREATE',
                          {'room': request.form['room_number']})
        return redirect(url_for('offices.offices_list'))
    return render_template('offices/form.html', office=None, action='add')


@offices_bp.route('/offices/<int:office_id>')
def office_detail(office_id):
    office = get_office(office_id)
    if not office:
        abort(404)
    employees = get_employees_by_office(office_id)
    return render_template('offices/detail.html', office=office, employees=employees)


@offices_bp.route('/offices/<int:office_id>/edit', methods=['GET', 'POST'])
def office_edit(office_id):
    office = get_office(office_id)
    if not office:
        abort(404)
    if request.method == 'POST':
        update_office(
            office_id=office_id,
            floor=request.form['floor'],
            room_number=request.form['room_number'],
            capacity=request.form['capacity'],
        )
        audit_service.log('office', office_id, 'UPDATE',
                          {'room': request.form['room_number']})
        return redirect(url_for('offices.office_detail', office_id=office_id))
    return render_template('offices/form.html', office=office, action='edit')


@offices_bp.route('/offices/<int:office_id>/delete', methods=['POST'])
def office_delete(office_id):
    office = get_office(office_id)
    if office:
        audit_service.log('office', office_id, 'DELETE',
                          {'room': office['room_number']})
    delete_office(office_id)
    return redirect(url_for('offices.offices_list'))


@offices_bp.route('/offices/<int:office_id>/assign', methods=['GET', 'POST'])
def office_assign(office_id):
    office = get_office(office_id)
    if not office:
        abort(404)
    all_employees = get_all_employees()
    current_ids   = {e['id'] for e in get_employees_by_office(office_id)}
    if request.method == 'POST':
        selected_ids = request.form.getlist('employee_ids')
        assign_employees_to_office(office_id, selected_ids)
        audit_service.log('office', office_id, 'ASSIGN',
                          {'employee_ids': selected_ids})
        return redirect(url_for('offices.office_detail', office_id=office_id))
    return render_template('offices/assign.html', office=office,
                           all_employees=all_employees,
                           current_employee_ids=current_ids)


# ── REST API ───────────────────────────────────────────────────────────────────

@offices_bp.route('/api/offices', methods=['GET'])
def api_offices_list():
    return jsonify(get_all_offices(request.args.get('sort_by'),
                                   request.args.get('filter_status')))


@offices_bp.route('/api/offices', methods=['POST'])
def api_office_create():
    data = request.get_json(force=True)
    new_id = create_office(data['floor'], data['room_number'], data['capacity'])
    audit_service.log('office', new_id, 'CREATE', {'room': data['room_number']})
    return jsonify(get_office(new_id)), 201


@offices_bp.route('/api/offices/<int:office_id>', methods=['GET'])
def api_office_get(office_id):
    office = get_office(office_id)
    return jsonify(office) if office else (jsonify({'error': 'Not found'}), 404)


@offices_bp.route('/api/offices/<int:office_id>', methods=['PUT'])
def api_office_update(office_id):
    if not get_office(office_id):
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json(force=True)
    update_office(office_id, data['floor'], data['room_number'], data['capacity'])
    audit_service.log('office', office_id, 'UPDATE', {'room': data['room_number']})
    return jsonify(get_office(office_id))


@offices_bp.route('/api/offices/<int:office_id>', methods=['DELETE'])
def api_office_delete(office_id):
    office = get_office(office_id)
    if not office:
        return jsonify({'error': 'Not found'}), 404
    audit_service.log('office', office_id, 'DELETE',
                      {'room': office['room_number']})
    delete_office(office_id)
    return jsonify({'message': 'Deleted'}), 200


@offices_bp.route('/api/offices/<int:office_id>/employees', methods=['GET'])
def api_office_employees(office_id):
    if not get_office(office_id):
        return jsonify({'error': 'Not found'}), 404
    return jsonify(get_employees_by_office(office_id))


@offices_bp.route('/api/offices/<int:office_id>/assign', methods=['POST'])
def api_office_assign(office_id):
    if not get_office(office_id):
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json(force=True)
    emp_ids = data.get('employee_ids', [])
    assign_employees_to_office(office_id, emp_ids)
    audit_service.log('office', office_id, 'ASSIGN', {'employee_ids': emp_ids})
    return jsonify({'message': 'Assigned', 'office_id': office_id,
                    'employee_ids': emp_ids})
