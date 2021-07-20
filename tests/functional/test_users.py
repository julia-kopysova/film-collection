import requests


def test_genres():
    res = requests.get('http://0.0.0.0:5000/genres')
    assert res.status_code == 200


def test_user_login():
    res = requests.post(
        "http://0.0.0.0:5000/login",
        json={"username": "kim_lee", "password": "password"}
    )
    assert res.status_code == 200


def test_search_film():
    res = requests.get(
        "http://0.0.0.0:5000/search_film?name=a"
    )
    assert res.status_code == 200
