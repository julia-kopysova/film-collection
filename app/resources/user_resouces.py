from flask import request, jsonify
from flask_restful import Resource

from app import db
from app.models import User
from app.schemas import UserSchema

user_schema = UserSchema()


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return user_schema.dump(users)

    def post(self):
        new_user = User(
            username=request.json['username'],
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            email=request.json['email'],
            password=request.json['password'],
            is_superuser=request.json['is_superuser']
        )
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def patch(self, user_id):
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

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
