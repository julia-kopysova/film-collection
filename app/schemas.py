"""
Module for schemas
"""
from app import ma
from app.models import Genre, Director, User, Film


class GenreSchema(ma.Schema):
    """
    Schema for Genre model
    """

    class Meta:
        """
        Meta class
        """
        fields = ["genre_title"]
        model = Genre
        load_instance = True
        include_fk = True


genre_schema = GenreSchema()
genre_schema = GenreSchema(many=True)


class DirectorSchema(ma.Schema):
    """
    Schema for Director model
    """
    class Meta:
        """
        Meta class
        """
        fields = ("first_name", "last_name")
        model = Director
        load_instance = True
        include_fk = True


director_schema = DirectorSchema()
director_schema = DirectorSchema(many=True)


class UserSchema(ma.Schema):
    """
    Schema for User model
    """
    class Meta:
        """
        Meta class
        """
        fields = ("username", "first_name", "last_name", "email", "password", "is_superuser")
        model = User
        load_instance = True
        include_fk = True


user_schema = UserSchema()
user_schema = UserSchema(many=True)


class FilmSchema(ma.Schema):
    """
    Schema for Film model
    """
    class Meta:
        """
        Meta class
        """
        fields = ("film_title", "release_date", "description",
                  "rating", "poster", "director_id", "user_id")
        model = Film
        load_instance = True
        include_fk = True


film_schema = FilmSchema()
film_schema = FilmSchema(many=True)
