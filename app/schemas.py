# from app import ma
# from app.models import Genre
#
#
# class GenreSchema(ma.Schema):
#     class Meta:
#         model = Genre
#         load_instance = True
#         include_fk = True
from app import ma
from app.models import Genre, Director, User, Film, FilmHasGenre


class GenreSchema(ma.Schema):
    class Meta:
        fields = ["genre_title"]
        model = Genre
        load_instance = True
        include_fk = True


genre_schema = GenreSchema()
genre_schema = GenreSchema(many=True)


class DirectorSchema(ma.Schema):
    class Meta:
        fields = ("first_name", "last_name")
        model = Director
        load_instance = True
        include_fk = True


director_schema = DirectorSchema()
director_schema = DirectorSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "first_name", "last_name", "email", "password", "is_superuser")
        model = User
        load_instance = True
        include_fk = True


user_schema = UserSchema()
user_schema = UserSchema(many=True)


class FilmSchema(ma.Schema):
    class Meta:
        fields = ("film_title", "release_date", "description", "rating", "poster", "director_id", "user_id")
        model = Film
        load_instance = True
        include_fk = True


film_schema = FilmSchema()
film_schema = FilmSchema(many=True)
