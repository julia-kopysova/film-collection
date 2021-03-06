"""
Module for genre resources
"""
from flask import request, jsonify
from flask_login import current_user, login_required
from flask_restful import Resource

from app import db, application
from app.models import Genre
from app.schemas import GenreSchema

genre_schema = GenreSchema()


class GenreListResource(Resource):
    """
    Resource for genres
    """
    @staticmethod
    def get():
        """
        Get genres
        :return: list of JSONs
        """
        application.logger.info("Get all films")
        return [{
            'genre_id': genre.genre_id,
            'genre_title': genre.genre_title
        } for genre in Genre.query.all()]

    @staticmethod
    @login_required
    def post():
        """
        Adds a genre
        :return: JSON
        """
        if current_user.is_authenticated and current_user.is_superuser:
            new_genre = Genre(
                genre_title=request.json['genre_title']
            )
            db.session.add(new_genre)
            db.session.commit()
            application.logger.info("%s added genre", current_user.username)
            return genre_schema.dump(new_genre)
        return jsonify({
                "status": 401,
                "reason": "User is not admin"
            })


class GenreResource(Resource):
    """
    Resource for one genre
    """
    @staticmethod
    def get(genre_id):
        """
        Get genre by genre_id
        :param genre_id: id of genre
        :return: JSON
        """
        genre = Genre.query.get_or_404(genre_id)
        application.logger.info("Ged %d genre", genre_id)
        return genre_schema.dump(genre)

    @staticmethod
    @login_required
    def patch(genre_id):
        """
        Update genre by id
        :param genre_id: id of genre
        :return: JSON
        """
        if current_user.is_authenticated and current_user.is_superuser:
            genre = Genre.query.get_or_404(genre_id)
            if 'genre_title' in request.json:
                genre.genre_title = request.json['genre_title']
                application.logger.info("Update title %d genre", genre_id)
            db.session.commit()
            return genre_schema.dump(genre)
        return jsonify({
                "status": 401,
                "reason": "User is not admin"
            })

    @staticmethod
    @login_required
    def delete(genre_id):
        """
        Delete genre by id
        :param genre_id: id of genre
        :return: Response
        """
        if current_user.is_authenticated and current_user.is_superuser:
            genre = Genre.query.get_or_404(genre_id)
            db.session.delete(genre)
            db.session.commit()
            application.logger.info("Deleted %d genre", genre_id)
            return jsonify({
                "status": 204,
                "reason": "Genre was deleted"
            })
        return jsonify({
                "status": 401,
                "reason": "User is not admin"
            })
