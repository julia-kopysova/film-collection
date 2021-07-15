"""
Models of project
"""
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref


db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    Class represents User model
    Method:
        get_id: returns id of user
    """
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
        """
        Initializes User
        :param username: username unique
        :param first_name: first name of user
        :param last_name: last name of user
        :param email: email of user
        :param password: password in hash representation
        :param is_superuser: is admin or not
        """
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_superuser = is_superuser

    def __repr__(self):
        """
        String representation
        :return: string
        """
        return '<User: first_name = {first_name}, last_name = {last_name}>'.format(
            first_name=self.first_name,
            last_name=self.last_name)

    def get_id(self) -> int:
        """
        Returns if of user
        :return: int
        """
        return self.user_id


class Director(db.Model):
    """
    Class represents Director model
    """
    __tablename__ = "director"

    director_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    films = db.relationship('Film', backref='director', lazy=True)

    def __init__(self, first_name, last_name):
        """
        Initializes Director
        :param first_name: first name of director
        :param last_name: last name of director
        """
        self.first_name = first_name
        self.last_name = last_name


class Film(db.Model):
    """
    Class represents Film model
    """
    __tablename__ = "film"

    film_id = db.Column(db.Integer, primary_key=True)
    film_title = db.Column(db.String(100), unique=False, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    rating = db.Column(db.Integer, unique=False, nullable=False)
    poster = db.Column(db.String(256), unique=False, nullable=False)
    director_id = db.Column(db.Integer,
                            db.ForeignKey('director.director_id', ondelete='SET NULL'),
                            nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    genres = relationship("Genre", secondary="film_has_genre")

    def __init__(self, film_title, release_date, description, rating, poster, director_id, user_id):
        """
        Initializes Film
        :param film_title: film title
        :param release_date: date when film was released
        :param description: description of
        :param rating: rating of film
        :param poster: link on poster
        :param director_id: fk on director
        :param user_id: fk on user that added film
        """
        self.film_title = film_title
        self.release_date = release_date
        self.description = description
        self.rating = rating
        self.poster = poster
        self.director_id = director_id
        self.user_id = user_id


class Genre(db.Model):
    """
    Class represents Genre model
    """
    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_title = db.Column(db.String(20), unique=True, nullable=False)
    users = relationship("Film", secondary="film_has_genre")

    def __init__(self, genre_title):
        """
        Initializes genre
        :param genre_title: title of genre
        """
        self.genre_title = genre_title


class FilmHasGenre(db.Model):
    """
    Model for associative table between Genre and Film
    """
    __tablename__ = "film_has_genre"

    film_has_genre = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=False)

    film = relationship(Film, backref=backref("film_has_genre", cascade="all, delete-orphan"))
    genre = relationship(Genre, backref=backref("film_has_genre", cascade="all, delete-orphan"))

    def __init__(self, film_id, genre_id):
        """
        Initializes film and genre
        :param film_id: fk on film
        :param genre_id: fk on genre
        """
        self.film_id = film_id
        self.genre_id = genre_id
