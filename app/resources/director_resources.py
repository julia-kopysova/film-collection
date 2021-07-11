from flask import request, jsonify
from flask_restful import Resource

from app import db
from app.models import Director
from app.schemas import DirectorSchema

director_schema = DirectorSchema()


class DirectorListResource(Resource):
    def get(self):
        return jsonify([{
            'director_id': director.director_id,
            'first_name': director.first_name,
            'last_name': director.last_name,

        } for director in Director.query.all()])

    def post(self):
        new_director = Director(
            first_name=request.json["first_name"],
            last_name=request.json["last_name"]
        )
        db.session.add(new_director)
        db.session.commit()
        return director_schema.dump(new_director)


class DirectorResource(Resource):
    def get(self, director_id):
        director = Director.query.get_or_404(director_id)
        return director_schema.dump(director)

    def patch(self, director_id):
        director = Director.query.get_or_404(director_id)

        if 'first_name' in request.json:
            director.first_name = request.json['first_name']
        if 'last_name' in request.json:
            director.last_name = request.json['last_name']
        db.session.commit()
        return director_schema.dump(director)

    def delete(self, director_id):
        director = Director.query.get_or_404(director_id)
        db.session.delete(director)
        db.session.commit()
        return '', 204

# from flask import jsonify, request
#
# from app import app, db
# from app.models import Genre, Director
# from app.schemas import genre_schema, director_schema
#
#
# @app.route('/director/', methods=['GET'])
# def get_directors():
#     all_directors = Director.query.all()
#     result = director_schema.dump(all_directors)
#     return jsonify(result)
#
#
# # adding a genre
# @app.route('/director/', methods=['POST'])
# def add_director():
#     first_name = request.json['first_name']
#     last_name = request.json['last_name']
#     my_director = Director(first_name, last_name)
#     db.session.add(my_director)
#     db.session.commit()
#
#     return director_schema.jsonify(my_director)
