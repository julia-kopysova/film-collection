import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL",
                                    "postgresql://postgres:postgres_password@db_film_collection:5432/hello_flask_dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
