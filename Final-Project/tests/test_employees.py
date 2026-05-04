"""Tests: Employee CRUD + assign through REST API.

Flow:  create dept → create office → create employee → read → update → delete
"""
import pytest


@pytest.fixture(scope='module')
def dept_id(client):
    resp = client.post('/api/departments', json={'name': 'TestDept', 'budget': 999999})
    return resp.get_json()['id']


@pytest.fixture(scope='module')
def office_id(client):
    resp = client.post('/api/offices', json={'floor': 5, 'room_number': 'TEST-501', 'capacity': 20})
    return resp.get_json()['id']


def test_create_employee(client, dept_id, office_id):
    resp = client.post('/api/employees', json={
        'name': 'Daniel Malka',
        'department_id': dept_id,
        'hire_date': '2022-01-15',
        'salary': 18000,
        'office_id': office_id,
        'email': 'daniel@mego.hr',
        'phone': '+972-50-1234567',
        'status': 'active',
        'skills': ['Python', 'Flask', 'Docker'],
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['name'] == 'Daniel Malka'
    assert data['email'] == 'daniel@mego.hr'
    assert 'Python' in data['skills']
    assert data['seniority_years'] > 0


def test_list_employees(client):
    resp = client.get('/api/employees')
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)
    assert len(resp.get_json()) > 0


def test_get_employee(client, dept_id, office_id):
    create = client.post('/api/employees', json={
        'name': 'Sara Levi',
        'department_id': dept_id,
        'hire_date': '2021-06-01',
        'salary': 15000,
        'status': 'active',
    })
    emp_id = create.get_json()['id']

    resp = client.get(f'/api/employees/{emp_id}')
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'Sara Levi'


def test_filter_employees_by_status(client, dept_id):
    resp = client.get('/api/employees?status=active')
    assert resp.status_code == 200
    for emp in resp.get_json():
        assert emp['status'] == 'active'


def test_update_employee(client, dept_id, office_id):
    create = client.post('/api/employees', json={
        'name': 'Old Name',
        'department_id': dept_id,
        'hire_date': '2020-03-10',
        'salary': 12000,
        'status': 'active',
    })
    emp_id = create.get_json()['id']

    resp = client.put(f'/api/employees/{emp_id}', json={
        'name': 'New Name',
        'department_id': dept_id,
        'hire_date': '2020-03-10',
        'salary': 14000,
        'status': 'on_leave',
        'skills': ['Leadership'],
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['name'] == 'New Name'
    assert data['salary'] == 14000.0
    assert data['status'] == 'on_leave'
    assert 'Leadership' in data['skills']


def test_assign_employees_to_office(client, dept_id, office_id):
    emp1 = client.post('/api/employees', json={
        'name': 'Assign Test 1', 'department_id': dept_id,
        'hire_date': '2023-01-01', 'salary': 10000, 'status': 'active',
    }).get_json()['id']

    resp = client.post(f'/api/offices/{office_id}/assign',
                       json={'employee_ids': [emp1]})
    assert resp.status_code == 200

    office_emps = client.get(f'/api/offices/{office_id}/employees').get_json()
    ids = [e['id'] for e in office_emps]
    assert emp1 in ids


def test_delete_employee(client, dept_id):
    create = client.post('/api/employees', json={
        'name': 'To Delete', 'department_id': dept_id,
        'hire_date': '2023-06-01', 'salary': 9000, 'status': 'active',
    })
    emp_id = create.get_json()['id']

    assert client.delete(f'/api/employees/{emp_id}').status_code == 200
    assert client.get(f'/api/employees/{emp_id}').status_code == 404


def test_employee_not_found(client):
    assert client.get('/api/employees/999999').status_code == 404


def test_health_endpoint(client):
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'ok'
