"""
Module for user resources
"""
from flask import request, jsonify
from flask_login import current_user, login_required
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from app import db
from app.models import User
from app.schemas import UserSchema

user_schema = UserSchema()


class UserListResource(Resource):
    """
    Resource for users
    """
    @staticmethod
    @login_required
    def get():
        """
        Get users
        :return: Response
        """
        if current_user.is_authenticated and current_user.is_superuser:
            return jsonify([{
                'user_id': user.user_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password
            } for user in User.query.all()])
        return jsonify({
            "status": 401,
            "reason": "You aren't admin"
        })

    @staticmethod
    @login_required
    def post():
        """
        Adds user
        :return: JSON
        """
        if current_user.is_authenticated and current_user.is_superuser:
            password = request.json['password']
            new_user = User(
                username=request.json['username'],
                first_name=request.json['first_name'],
                last_name=request.json['last_name'],
                email=request.json['email'],
                password=generate_password_hash(password),
                is_superuser=request.json['is_superuser']
            )
            db.session.add(new_user)
            db.session.commit()
            return user_schema.dump(new_user)
        return jsonify({
            "status": 401,
            "reason": "You aren't admin"
        })


class UserResource(Resource):
    """
    Resources for one user
    """
    @staticmethod
    @login_required
    def get(user_id):
        """
        Get one user
        :param user_id: id of user
        :return: JSON
        """
        if current_user.is_authenticated and (
                current_user.user_id == user_id or
                current_user.is_superuser is True):
            user = User.query.get_or_404(user_id)
            return user_schema.dump(user)
        return jsonify({
            "status": 401,
            "reason": "You aren't admin or this user"
        })

    @staticmethod
    @login_required
    def patch(user_id):
        """
        Update user
        :param user_id: id of user
        :return: JSON
        """
        if current_user.is_authenticated and (
                current_user.user_id == user_id or
                current_user.is_superuser is True):
            user = User.query.get_or_404(user_id)

            if 'username' in request.json:
                user.username = request.json['username']
            if 'first_name' in request.json:
                user.username = request.json['first_name']
            if 'last_name' in request.json:
                user.username = request.json['last_name']
            if 'email' in request.json:
                user.username = request.json['email']
            if 'password' in request.json:
                user.username = request.json['password']
            if 'is_superuser' in request.json:
                user.username = request.json['is_superuser']
            db.session.commit()
            return user_schema.dump(user)
        return jsonify({
            "status": 401,
            "reason": "You aren't admin or this user"
        })

    @staticmethod
    @login_required
    def delete(user_id):
        """
        Delete user by user_id
        :param user_id: id of user
        :return: Response
        """
        if current_user.is_authenticated and current_user.is_superuser is True:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({
                "status": 204,
                "reason": "User was deleted"
            })
        return jsonify({
            "status": 401,
            "reason": "You aren't admin"
        })
