"""
Models of project
"""
import json

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.orm import relationship, backref

# from app import db

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    is_superuser = db.Column(db.Boolean(), default=True, nullable=False)
    films = db.relationship('Film', backref='user', lazy=True)

    def __init__(self, username, first_name, last_name, email, password, is_superuser):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_superuser = is_superuser

    def get_id(self):
        return self.user_id


class Director(db.Model):
    __tablename__ = "director"

    director_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    films = db.relationship('Film', backref='director', lazy=True)

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class Film(db.Model):
    __tablename__ = "film"

    film_id = db.Column(db.Integer, primary_key=True)
    film_title = db.Column(db.String(100), unique=False, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    poster = db.Column(db.String(256), unique=False, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id', ondelete='SET NULL'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    genres = relationship("Genre", secondary="film_has_genre")

    def __init__(self, film_title, release_date, description, rating, poster, director_id, user_id):
        self.film_title = film_title
        self.release_date = release_date
        self.description = description
        self.rating = rating
        self.poster = poster
        self.director_id = director_id
        self.user_id = user_id


class Genre(db.Model):
    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_title = db.Column(db.String(20), unique=True, nullable=False)
    users = relationship("Film", secondary="film_has_genre")

    def __init__(self, genre_title):
        self.genre_title = genre_title

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def as_dict(self):
        return {c.genre_title: getattr(self, c.genre_title) for c in self.__table__.columns}

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def find_all(cls):
        return cls.query.all()


class FilmHasGenre(db.Model):
    __tablename__ = "film_has_genre"

    film_has_genre = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=False)

    film = relationship(Film, backref=backref("film_has_genre", cascade="all, delete-orphan"))
    genre = relationship(Genre, backref=backref("film_has_genre", cascade="all, delete-orphan"))

    def __init__(self, film_id, genre_id):
        self.film_id = film_id
        self.genre_id = genre_id
