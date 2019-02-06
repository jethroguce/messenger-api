from flask import Flask


def create_flask_app():
    app = Flask(__name__)
    app.config.from_object('config')

    return app
