"""Tests: Department CRUD through REST API."""
import json


def test_create_department(client):
    resp = client.post('/api/departments', json={
        'name': 'Engineering',
        'budget': 500000,
        'manager_name': 'Alice Cohen',
        'description': 'Software engineering team',
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['name'] == 'Engineering'
    assert data['id'] is not None
    return data['id']


def test_list_departments(client):
    resp = client.get('/api/departments')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    names = [d['name'] for d in data]
    assert 'Engineering' in names


def test_get_department(client):
    # Create first
    create = client.post('/api/departments', json={'name': 'QA', 'budget': 100000})
    dept_id = create.get_json()['id']

    resp = client.get(f'/api/departments/{dept_id}')
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'QA'


def test_update_department(client):
    create = client.post('/api/departments', json={'name': 'Marketing'})
    dept_id = create.get_json()['id']

    resp = client.put(f'/api/departments/{dept_id}', json={
        'name': 'Marketing & Sales',
        'budget': 200000,
        'manager_name': 'Bob Levi',
    })
    assert resp.status_code == 200
    assert resp.get_json()['name'] == 'Marketing & Sales'


def test_delete_department(client):
    create = client.post('/api/departments', json={'name': 'Temp Dept'})
    dept_id = create.get_json()['id']

    del_resp = client.delete(f'/api/departments/{dept_id}')
    assert del_resp.status_code == 200

    get_resp = client.get(f'/api/departments/{dept_id}')
    assert get_resp.status_code == 404


def test_department_not_found(client):
    resp = client.get('/api/departments/999999')
    assert resp.status_code == 404
