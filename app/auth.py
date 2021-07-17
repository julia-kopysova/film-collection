"""
Module for user registration, log in, log out
"""
from flask import request, Response, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import application, User, db, login_manager


@login_manager.user_loader
def get_user(ident):
    """
    Get user by id
    :param ident: id of user
    :return: user
    """
    return User.query.get(int(ident))


@application.route('/signup', methods=['POST'])
def signup() -> Response:
    """
    Registration user
    User enters username, first_name, last_name, email, password
    Password will be hashed
    User will be added in database if data is correct
    :return: Response
    """
    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).\
        first()
    if user:
        return jsonify({"status": 405,
                        "reason": "This data already exists"})
    try:
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password),
            is_superuser=False)
        application.logger.info('%s added to database', new_user.username)
    except AssertionError:
        application.logger.info('%s entered incorrect data', user.username)
        return jsonify({"status": 401,
                        "reason": "Incorrect data"})
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": 200,
                    "reason": "User was added"})


@application.route('/login', methods=['POST'])
def login_post() -> Response:
    """
    Login user
    User enter username and password
    :return: Response
    """
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        db.session.commit()
        application.logger.info('%s logged in successfully', user.username)
        return jsonify({"status": 202,
                        "reason": "Log in"})
    application.logger.info('%s failed to log in', username)
    return jsonify({"status": 401,
                    "reason": "Username or Password Error"})


@application.route('/logout', methods=['POST'])
@login_required
def logout_post() -> Response:
    """
    Logout user
    :return: Response
    """
    user = current_user
    application.logger.info('Log out')
    logout_user()
    return jsonify({"status": 200,
                    "reason": "logout success"})
