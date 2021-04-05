from flask_jwt_extended import create_access_token

from jokes import db, app
import pytest
import jwt

from jokes.db import create_user, joke_create_by_user

TEST_SECRET = 'test-secret'
BOB_JOKES = ['bob first joke', 'bob second joke']
BOB_JOKE_ID = 1

def fill_db():
    db.db.drop_all()
    db.db.create_all()
    alice_id = create_user({'login': 'alice', 'password': 'password'})
    bob_id = create_user({'login': 'bob', 'password': 'password'})
    for joke in BOB_JOKES:
        joke_create_by_user(bob_id, joke)

@pytest.fixture()
def client():
    test_app = app.create_app()
    test_app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    test_app.config["JWT_SECRET_KEY"] = TEST_SECRET
    test_app.config['TESTING'] = True
    db.db.init_app(test_app)

    with test_app.test_client() as client:
        with test_app.app_context():
            fill_db()
        yield client