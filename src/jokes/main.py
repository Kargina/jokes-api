from jokes import db
from jokes.app import create_app
from jokes.config import LISTEN_PORT, LISTEN_HOST


def run():

    app = create_app()
    db.db.init_app(app)
    with app.app_context():
        db.init_db()
    try:
        app.run(host=LISTEN_HOST, port=LISTEN_PORT)
    except OSError as e:
        raise Exception(f"Can't run app: {e}")


if __name__ == '__main__':
    run()
