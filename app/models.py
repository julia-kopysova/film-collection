from app import db


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_superuser = db.Column(db.Boolean(), default=True, nullable=False)
    films = db.relationship('Film', backref='user', lazy=True)

    def __init__(self, username, first_name, last_name, email, password, is_superuser):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_superuser = is_superuser


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
    rating = db.Column(db.Numeric(2, 2), unique=False, nullable=False)
    poster = db.Column(db.String(100), unique=False, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.director_id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    film_has_genres = db.relationship('FilmHasGenre', backref='film', lazy=True)


class FilmHasGenre(db.Model):
    __tablename__ = "film_has_genre"

    film_has_genre = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.film_id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'), nullable=False)


class Genre(db.Model):
    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_title = db.Column(db.String(20), unique=True, nullable=False)
    film_has_genres = db.relationship('FilmHasGenre', backref='genre', lazy=True)

