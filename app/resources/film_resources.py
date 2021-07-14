import json

from flask import request, jsonify, session
from flask_login import login_required, current_user
from flask_restful import Resource
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app import db
from app.models import Film, User, Director, Genre, FilmHasGenre
from app.pagination import get_paginated_list
from app.schemas import FilmSchema

film_schema = FilmSchema()


class FilmListResource(Resource):
    def get(self):
        order_field = request.args.get('order_field', 'film_id')
        films = Film.query.order_by(desc(order_field)).all()
        # films = Film.query.join(Director, Director.director_id == Film.director_id).\
        #     order_by(desc(order_field)).all()
        # films = db.session.query(Film, Director).filter(Film.director_id == Director.director_id).all()
        # films = session.query(*Film.__table__.columns, Director.__table__.columns). \
        #     select_from(Film). \
        #     join(Director, Film.director_id == Director.director_id). \
        #     order_by(desc(order_field)).all()
        # query = Session.query(
        #     Film.film_id,
        #     Film.film_title,
        #     Film.rating,
        #     Film.release_date,
        #     Director.first_name
        # )
        # films = query.join(Film).join(Director).all()
        film_list = [{
            'film_id': film.film_id,
            'film_title': film.film_title,
            'rating': film.rating,
            'release_date': film.release_date,
            'director': film.director_id,
            'user_id': film.user_id
        } for film in films]
        return jsonify(get_paginated_list(
            film_list,
            '/films',
            start=request.args.get('start', 1),
            limit=request.args.get('limit', 10)
        ))

    @login_required
    def post(self):
        if current_user.is_authenticated:
            film_title = request.json['film_title'],
            release_date = request.json['release_date'],
            description = request.json['description'],
            rating = request.json['rating'],
            poster = request.json['poster'],
            director_first_name = request.json['director_first_name'],
            director_last_name = request.json['director_last_name'],
            genres = request.json['genres']
            for genre in genres:
                genre_in_db = Genre.query.filter_by(genre_title=genre).first()
                if genre_in_db is None:
                    return {
                        "status": 401,
                        "reason": "Genre doesn't exist"
                    }
            director_in_db = Director.query.filter_by(first_name=director_first_name,
                                                      last_name=director_last_name).first()
            if director_in_db is None:
                director_in_db = Director(first_name=director_first_name,
                                          last_name=director_last_name)
                db.session.add(director_in_db)
                db.session.commit()
            new_film = Film(
                film_title=film_title,
                release_date=release_date,
                description=description,
                rating=rating,
                poster=poster,
                director_id=director_in_db.director_id,
                user_id=current_user.get_id()
            )
            db.session.add(new_film)
            db.session.commit()
            for genre in genres:
                genre_in_db = Genre.query.filter_by(genre_title=genre).first()
                film_has_genre = FilmHasGenre(film_id=new_film.film_id,
                                              genre_id=genre_in_db.genre_id)
                db.session.add(film_has_genre)
                db.session.commit()
            return film_schema.dump(new_film)
        else:
            return {
                "status": 401,
                "reason": "User isn't authenticated"
            }


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

    @login_required
    def delete(self, film_id):
        film = Film.query.get_or_404(film_id)
        if current_user.user_id == film.user_id or current_user.is_superuser is True:
            db.session.delete(film)
            db.session.commit()
        return '', 204
