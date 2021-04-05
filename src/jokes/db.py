import hashlib
import uuid
from jokes.exceptions import *
from flask_sqlalchemy import SQLAlchemy
from jokes.config import USER_MAX_LEN, PASSWORD_MAX_LEN

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(USER_MAX_LEN), unique=True, nullable=False)
    password = db.Column(db.String(PASSWORD_MAX_LEN), unique=False, nullable=False)
    password_salt = db.Column(db.String(PASSWORD_MAX_LEN), unique=False, nullable=False)
    addresses = db.relationship('Joke', backref='user', lazy=True)

class Joke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

def hash_password(password):
    salt = str(uuid.uuid4())
    hashed_password = hashlib.sha512(password.encode() + salt.encode()).hexdigest()
    return salt, hashed_password

def check_password(login, password):
    user = User.query.filter_by(login=login).first()
    if user is None:
        return False
    salt = user.password_salt
    hashed_password = hashlib.sha512(password.encode() + salt.encode()).hexdigest()
    return user.password == hashed_password

def check_user(login):
    if len(login) > USER_MAX_LEN:
        raise JokeBadUserException(f'Login must be less than {USER_MAX_LEN} characters')
    if User.query.filter_by(login=login).first() is not None:
        raise JokeBadUserException('Login already exist')


def create_user(user):
    login = user['login']
    password = user['password']
    salt, password_hash = hash_password(password)
    check_user(login)
    u = User(login=login, password=password_hash, password_salt=salt)
    db.session.add(u)
    db.session.commit()
    return User.query.filter_by(login=login).first().id


def joke_get_all_by_user_id(user_id):
    user_jokes = Joke.query.filter_by(user_id=user_id).all()
    list_of_user_jokes = [{'id': joke.id, 'text': joke.text} for joke in user_jokes]
    return list_of_user_jokes

def joke_create_by_user(user_id, joke_text):
    joke = Joke(text=joke_text, user_id=user_id)
    db.session.add(joke)
    db.session.commit()
    return joke.id

def joke_get_by_id(user_id, joke_id):
    return Joke.query.filter_by(id=joke_id, user_id=user_id).first()

def joke_update_by_id(user_id, joke_id, joke_text):
    joke = Joke.query.filter_by(id=joke_id, user_id=user_id).first()
    if joke is not None:
        joke.text = joke_text
        db.session.commit()
    return Joke.query.filter_by(id=joke_id, user_id=user_id).first()

def get_user_id_by_login(login):
    return User.query.filter_by(login=login).first().id

def remove_user_joke(user_id, joke_id):
    joke = Joke.query.filter_by(user_id=user_id, id=joke_id).first()
    if joke is None:
        raise JokeBadJokeException('No such joke for user')
    else:
        db.session.delete(joke)
        db.session.commit()

def init_db():
    db.create_all()
