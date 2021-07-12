"""
Module initializes app
"""
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config

db = SQLAlchemy()  # done here so that db is importable
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    return app


application = create_app()
ma = Marshmallow(application)
api = Api(application)

# app = Flask(__name__)
# app.config.from_object("app.config.Config")
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
#
# ma = Marshmallow(app)
# api = Api(app)
#
#
# @app.route('/')
# def hello_world():
#     """
#     Hello Word method
#     :return:
#     """
#     return 'Hello World!!!!'


# @app.route('/foo')
# def foo():
#     return 'foo000'


# @app.route('/genres/', methods=['GET'])
# def get_genres():
#     # all_genres = Genre.query.all()
#     return 'lalala'
