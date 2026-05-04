"""Tests: Office CRUD through REST API."""


def test_create_office(client):
    resp = client.post('/api/offices', json={
        'floor': 3,
        'room_number': 'A301',
        'capacity': 10,
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['floor'] == 3
    assert data['room_number'] == 'A301'
    assert data['capacity'] == 10


def test_list_offices(client):
    resp = client.get('/api/offices')
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)


def test_get_office(client):
    create = client.post('/api/offices', json={'floor': 1, 'room_number': 'B101', 'capacity': 5})
    office_id = create.get_json()['id']

    resp = client.get(f'/api/offices/{office_id}')
    assert resp.status_code == 200
    assert resp.get_json()['room_number'] == 'B101'


def test_update_office(client):
    create = client.post('/api/offices', json={'floor': 2, 'room_number': 'C201', 'capacity': 8})
    office_id = create.get_json()['id']

    resp = client.put(f'/api/offices/{office_id}', json={
        'floor': 2, 'room_number': 'C201-Updated', 'capacity': 12
    })
    assert resp.status_code == 200
    assert resp.get_json()['capacity'] == 12


def test_delete_office(client):
    create = client.post('/api/offices', json={'floor': 9, 'room_number': 'DELETE-ME', 'capacity': 1})
    office_id = create.get_json()['id']

    assert client.delete(f'/api/offices/{office_id}').status_code == 200
    assert client.get(f'/api/offices/{office_id}').status_code == 404


def test_filter_offices_empty(client):
    resp = client.get('/api/offices?filter_status=empty')
    assert resp.status_code == 200
    data = resp.get_json()
    for office in data:
        assert office['employee_count'] == 0


def test_office_not_found(client):
    assert client.get('/api/offices/999999').status_code == 404
