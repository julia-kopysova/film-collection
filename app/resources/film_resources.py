from flask import request, jsonify
from flask_restful import Resource

from app import db
from app.models import Film
from app.schemas import FilmSchema

film_schema = FilmSchema()


class FilmListResource(Resource):
    def get(self):
        return jsonify([{
            'film_id': film.film_id,
            'film_title': film.film_title
        } for film in Film.query.all()])

    def post(self):
        new_film = Film(
            film_title=request.json['film_title'],
            release_date=request.json['release_date'],
            description=request.json['description'],
            rating=request.json['rating'],
            poster=request.json['poster'],
            director_id=request.json['director_id'],
            user_id=request.json['user_id']
        )
        db.session.add(new_film)
        db.session.commit()
        return film_schema.dump(new_film)


class FilmResource(Resource):
    def get(self, film_id):
        film = Film.query.get_or_404(film_id)
        return film_schema.dump(film)

    def patch(self, film_id):
        film = Film.query.get_or_404(film_id)

        if 'film_title' in request.json:
            film.film_title = request.json['film_title']
        if 'release_date' in request.json:
            film.release_date = request.json['release_date']
        if 'description' in request.json:
            film.description = request.json['description']
        if 'rating' in request.json:
            film.rating = request.json['rating']
        if 'poster' in request.json:
            film.poster = request.json['poster']
        if 'user_id' in request.json:
            film.user_id = request.json['user_id']
        if 'director_id' in request.json:
            film.director_id = request.json['director_id']
        db.session.commit()
        return film_schema.dump(film)

    def delete(self, film_id):
        film = Film.query.get_or_404(film_id)
        db.session.delete(film)
        db.session.commit()
        return '', 204
