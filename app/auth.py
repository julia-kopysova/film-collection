from typing import Union, Tuple

from flask import request, redirect, url_for, Response, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import application, User, db, login_manager


@login_manager.user_loader
def get_user(ident):
    return User.query.get(int(ident))


@application.route('/signup', methods=['POST'])
def signup() -> Union[Response, Tuple[str, int]]:
    username = request.json['username']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()

    if user:
        return 'This data already exists', 405

    new_user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=generate_password_hash(password),
        is_superuser=False)

    db.session.add(new_user)
    db.session.commit()
    return 'added', 202
    # return redirect(url_for('auth.login'))


@application.route('/login', methods=['POST'])
def login_post():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        db.session.commit()
        return jsonify({"status": 202,
                       "reason": "Log in"})
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


@application.route('/logout', methods=['POST'])
@login_required
def logout_post():
    logout_user()
    return jsonify({'result': 200, 'data': {'message': 'logout success'}})