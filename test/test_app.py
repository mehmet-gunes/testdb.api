from flask import url_for


def test_app_is_created(app):
    assert app.name == 'app'


def test_test_tube_route(app):
    """
        Testing if test_tube route exists
    """
    assert 'test_tube' in app.blueprints


def test_app(client):
    assert client.get(url_for('root.get_registered')).status_code == 200


def test_insert_product(client):
    response = client.post('/tube/', json={'email': 'user@email.com'})
    assert response.status_code == 200
