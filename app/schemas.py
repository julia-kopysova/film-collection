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
from app.models import Genre


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


director_schema = DirectorSchema()
director_schema = DirectorSchema(many=True)
