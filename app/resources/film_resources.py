"""
Module for film resources
"""
from flask import request, jsonify
from flask_login import login_required, current_user
from flask_restful import Resource
from sqlalchemy import desc

from app import db
from app.models import Film, Director, Genre, FilmHasGenre
from app.pagination import get_paginated_list
from app.schemas import FilmSchema

film_schema = FilmSchema()


class FilmListResource(Resource):
    """
    Resource for films
    """

    @staticmethod
    def get():
        """
        Display all films
        """
        order_field = request.args.get('order_field', 'film_id')
        films = Film.query.order_by(desc(order_field)).all()
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

    @staticmethod
    @login_required
    def post() -> Resource:
        """
        Adds one film to database
        :return: Resource
        """
        if current_user.is_authenticated:
            film_title = request.json['film_title']
            release_date = request.json['release_date']
            description = request.json['description']
            rating = request.json['rating']
            poster = request.json['poster']
            director_first_name = request.json['director_first_name']
            director_last_name = request.json['director_last_name']
            genres = request.json['genres']
            for genre in genres:
                genre_in_db = Genre.query.filter_by(genre_title=genre).first()
                if genre_in_db is None:
                    return jsonify({
                        "status": 401,
                        "reason": "Genre doesn't exist"
                    })
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
        return jsonify({
            "status": 401,
            "reason": "User isn't authenticated"
        })


class FilmResource(Resource):
    """
    Resource for one film
    """

    @staticmethod
    def get(film_id):
        """
        Get film by film_id
        :param film_id: id of film
        :return: JSON
        """
        film = Film.query.get_or_404(film_id)
        return film_schema.dump(film)

    @staticmethod
    @login_required
    def patch(film_id):
        """
        Update film
        :param film_id: id of film
        :return: JSON
        """
        film = Film.query.get_or_404(film_id)
        if current_user.is_authenticated and (
                current_user.user_id == film.user_id or
                current_user.is_superuser is True):
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
        return jsonify({
            "status": 401,
            "reason": "You aren't admin or user who added this film"
        })

    @staticmethod
    @login_required
    def delete(film_id) -> Resource:
        """
        Delete film by film_id
        :param film_id: id of film
        :return:
        """
        film = Film.query.get_or_404(film_id)
        if current_user.is_authenticated and (
                current_user.user_id == film.user_id or
                current_user.is_superuser is True):
            if film:
                db.session.delete(film)
                db.session.commit()
                return jsonify({
                    "status": 200,
                    "reason": "Film was deleted"
                })
            return jsonify({
                "status": 401,
                "reason": "Film doesn't exist"
            })
        return jsonify({
            "status": 401,
            "reason": "You aren't admin or user who added this film"
        })
