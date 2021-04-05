import sys

from flask import Flask, has_request_context, request
from werkzeug.contrib.fixers import ProxyFix

from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from jokes.config import DB_DSN

from jokes.views import api

import logging
from logging.handlers import RotatingFileHandler


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.user_id = get_jwt_identity()
        else:
            record.user_id = None

        return super().format(record)

def create_app():
    file_handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    stdout_handler = logging.StreamHandler(sys.stdout)
    formatter = RequestFormatter(
        '%(asctime)s %(levelname)s: [user_id=%(user_id)s] %(message)s'
    )
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)
    logging.basicConfig(handlers=[file_handler, stdout_handler], level=logging.INFO)

    app = Flask(__name__)

    @app.before_request
    def before_request_func():
        verify_jwt_in_request(optional=True)
        logging.info(f'Got request {request.environ["REQUEST_URI"]} '
                     f'from {request.remote_addr}, method: {request.method} ')

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config['RESTX_VALIDATE'] = True
    app.config['RESTX_MASK_SWAGGER'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_DSN

    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_IDENTITY_CLAIM"] = "user_id"
    app.config["PROPAGATE_EXCEPTIONS"] = True

    jwt = JWTManager(app)

    api.init_app(app)

    return app

