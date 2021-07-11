from flask import request, jsonify
from flask_restful import Resource

from app import db
from app.models import Genre
from app.schemas import GenreSchema

genre_schema = GenreSchema()


class GenreListResource(Resource):
    def get(self):
        return jsonify([{
            'genre_id': genre.genre_id,
            'genre_title': genre.genre_title
        } for genre in Genre.query.all()])

    def post(self):
        new_genre = Genre(
            genre_title=request.json['genre_title']
        )
        db.session.add(new_genre)
        db.session.commit()
        return genre_schema.dump(new_genre)


class GenreResource(Resource):
    def get(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        return genre_schema.dump(genre)

# from flask import jsonify, request
#
# from app import app, db
# from app.models import Genre
# from app.schemas import genre_schema
#
#
# @app.route('/genres/', methods=['GET'])
# def get_genres():
#     # all_genres = Genre.query.all()
#     # return 'lalala'
#     # result = genre_schema.dump(all_genres)
#     # return jsonify(result)
#     return jsonify([{
#         'genre_id': genre.genre_id,
#         'genre_title': genre.genre_title
#     } for genre in Genre.query.all()])


# adding a genre
# @app.route('/genre/', methods=['POST'])
# def add_genre():
#     genre_title = request.json['genre_title']
#
#     my_genre = Genre(genre_title)
#     db.session.add(my_genre)
#     db.session.commit()
#
#     return genre_schema.jsonify(my_genre)
