"""
Module for director resources
"""
from flask import request, jsonify
from flask_login import current_user, login_required
from flask_restful import Resource

from app import db, application
from app.models import Director
from app.schemas import DirectorSchema

director_schema = DirectorSchema()


class DirectorListResource(Resource):
    """
    Resources for directors
    """
    @staticmethod
    def get():
        """
        Get directors
        :return: Response
        """
        return jsonify([{
            'director_id': director.director_id,
            'first_name': director.first_name,
            'last_name': director.last_name,

        } for director in Director.query.all()])

    @staticmethod
    @login_required
    def post():
        """
        Adds a director
        :return:
        """
        if current_user.is_authenticated and current_user.is_superuser:
            new_director = Director(
                first_name=request.json["first_name"],
                last_name=request.json["last_name"]
            )
            db.session.add(new_director)
            db.session.commit()
            return director_schema.dump(new_director)
        return jsonify({
            "status": 401,
            "reason": "User is not admin"
        })


class DirectorResource(Resource):
    """
    Resource for one director
    """
    @staticmethod
    def get(director_id):
        """
        Get onr director
        :param director_id: id of director
        :return: JSON
        """
        director = Director.query.get_or_404(director_id)
        return director_schema.dump(director)

    @staticmethod
    @login_required
    def patch(director_id):
        """
        Updates a director
        :param director_id: id of director
        :return: JSON
        """
        if current_user.is_authenticated and current_user.is_superuser:
            director = Director.query.get_or_404(director_id)

            if 'first_name' in request.json:
                director.first_name = request.json['first_name']
            if 'last_name' in request.json:
                director.last_name = request.json['last_name']
            db.session.commit()
            return director_schema.dump(director)
        return jsonify({
            "status": 401,
            "reason": "User is not admin"
        })

    @staticmethod
    @login_required
    def delete(director_id):
        """
        Delete director
        :param director_id: id of director
        :return: Response
        """
        if current_user.is_authenticated and current_user.is_superuser:
            director = Director.query.get_or_404(director_id)
            db.session.delete(director)
            db.session.commit()
            application.logger.info('%s deletes director %s', current_user.username, director_id)
            return jsonify({
                "status": 204,
                "reason": "Director was deleted"
            })

        return jsonify({
                "status": 401,
                "reason": "User is not admin"
            })
