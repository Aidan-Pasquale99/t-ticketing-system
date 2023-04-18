from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_migrate import Migrate
import pytest
from flask import Flask
from src import tickets_bp, accounts_bp, core_bp

@pytest.fixture
def client():

    

    with app.test_client() as client:
        yield client

# def test_index(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     assert b"Welcome to the t Ticketing System" in response.data

def test_login(client):
    response = client.post("/login", data=dict(
        username="aidan@t.com",
        password="aidanpasquale"
    ), follow_redirects=True)
    assert b"Logged in as aidan@t.com" in response.data
    assert response.status_code == 200