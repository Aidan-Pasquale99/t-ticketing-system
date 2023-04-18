import pytest
from src import create_app
from flask.testing import FlaskClient


@pytest.fixture(scope='module')
def flask_app():
    app = create_app()
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(flask_app):
    app = flask_app
    ctx = flask_app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()


def test_index_page__not_logged_in(client):
    res = client.get('/')
    assert res.status_code == 401


def test_index_page__logged_in(client):
    with client:
        client.post('/login', data=dict(email='aidan@t.com', password='aidanpasquale'))
        res = client.get('/')
        assert res.status_code == 200