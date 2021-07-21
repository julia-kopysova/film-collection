import requests


def test_user_login():
    """
    Test log in
    """
    res = requests.post(
        "http://0.0.0.0:5000/login",
        json={"username": "kim_lee", "password": "password"}
    )
    assert res.status_code == 200


def test_get_users():
    """
    Test get users
    """
    res = requests.get('http://0.0.0.0:5000/users')
    assert res.status_code == 401


def test_user_sign_up():
    """
    Test Sign UP
    """
    res = requests.post(
        "http://0.0.0.0:5000/signup",
        json={"username": "albina", "first_name": "Albina", "last_name": "Ahohohoh",
              "email": "albina@gmail.com", "password": "password"}
    )
    assert res.status_code == 200


def test_get_users():
    """
    Test get users
    """
    res = requests.get('http://0.0.0.0:5000/users')
    assert res.status_code == 401


def test_get_user_by_id():
    """
    Test get user by id
    """
    res = requests.get('http://0.0.0.0:5000/users/1')
    assert res.status_code == 401


def test_post_users():
    """
    Test post users
    """
    res = requests.post(
        "http://0.0.0.0:5000/users",
        json={"username": "albina", "first_name": "Albina", "last_name": "Ahohohoh",
              "email": "albina@gmail.com", "password": "password"}
    )
    assert res.status_code == 401


def test_patch_user():
    """
    Test update user by user_id
    """
    res = requests.patch(
        "http://0.0.0.0:5000/users/1",
        json={"username": "amalia"}
    )
    assert res.status_code == 401


def test_delete_user():
    """
    Test delete user
    """
    res = requests.delete(
        "http://0.0.0.0:5000/users/1"
    )
    assert res.status_code == 401
