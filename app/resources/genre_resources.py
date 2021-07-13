import json

from flask import request, jsonify
from flask_restful import Resource

from app import db
from app.models import Genre
from app.schemas import GenreSchema

genre_schema = GenreSchema()


class GenreEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Genre):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class GenreListResource(Resource):
    @staticmethod
    def get():
        # genres = Genre.query.all()
        # return json.dumps(genres, cls=GenreEncoder)
        return [{
            'genre_id': genre.genre_id,
            'genre_title': genre.genre_title
        } for genre in Genre.query.all()]
        # genres_list = []
        # for genre in genres:
        #     genres_list.append(genre.to_dict())
        # return json.dumps(genres)

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

    def patch(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)

        if 'genre_title' in request.json:
            genre.genre_title = request.json['genre_title']

        db.session.commit()
        return genre_schema.dump(genre)

    def delete(self, genre_id):
        genre = Genre.query.get_or_404(genre_id)
        db.session.delete(genre)
        db.session.commit()
        return '', 204

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
