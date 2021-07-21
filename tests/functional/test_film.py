import requests


def test_search_film():
    """
    Test search film
    """
    res = requests.get(
        "http://0.0.0.0:5000/search_film?name=a"
    )
    assert res.status_code == 200


def test_pagination_search():
    """
    Test pagination in searching film
    """
    res = requests.get(
        "http://0.0.0.0:5000/search_film?name=a"
    )
    res_json = res.json()
    assert res_json["limit"] == 10
    assert res_json["start"] == 1


def test_filter_year():
    """
    Test filter films by year_start year_end
    """
    res = requests.get(
        "http://0.0.0.0:5000/films_years_filter?year_start=2020&year_end=2021"
    )
    assert res.status_code == 200

    res_1 = requests.get("http://0.0.0.0:5000/films_years_filter?year_start=2018&year_end=2018")
    assert res_1.content == b'[]\n'


def test_filter_by_director():
    """
    Test filter films by director first_name and last_name
    """
    res = requests.get(
        "http://0.0.0.0:5000/films_director_filter?first_name=Melina&last_name=Realina"
    )
    assert res.status_code == 200

    res_1 = requests.get("http://0.0.0.0:5000/films_director_filter?first_name=Alan&last_name=Badoev")
    assert res_1.content == b'[]\n'


def test_filter_films_by_genre():
    """
    Test filter films by genre title
    :return:
    """
    res = requests.get(
        "http://0.0.0.0:5000/films_genre_filter"
    )
    res_json = res.json()
    assert res_json["reason"] == "Enter genre title"

    res_1 = requests.get(
        "http://0.0.0.0:5000/films_genre_filter"
    )
    assert res_1.status_code == 200


def test_ordering():
    """
    Test ordering in get method
    """
    res = requests.get('http://0.0.0.0:5000/films?order_field=rating')
    assert res.status_code == 200

    res_1 = requests.get('http://0.0.0.0:5000/films?order_field=r')
    assert res_1.status_code == 200


def test_get_films():
    """
    Test get genres
    """
    res = requests.get('http://0.0.0.0:5000/films')
    assert res.status_code == 200


def test_get_film_by_id():
    """
    Test get film by id
    """
    res = requests.get('http://0.0.0.0:5000/films/2')
    assert res.status_code == 200


def test_director_unknown():
    """
    Test director unknown
    """
    res = requests.get('http://0.0.0.0:5000/films/2')
    res_json = res.json()
    assert res_json["director"] == "unknown"


def test_post_film():
    """
    Test post film
    """
    res = requests.post('http://0.0.0.0:5000/films', json={
        "film_title": "Bestseller",
        "release_date": "2021-07-11T20:45:04.327328422Z",
        "description": "Desc",
        "rating": 9,
        "poster": "src/",
        "director_first_name": "Alan",
        "director_last_name": "Badoev",
        "genres": ["Comedy"]
    })
    assert res.status_code == 401


def test_delete_films_by_id():
    """
    Test delete film
    """
    res = requests.delete('http://0.0.0.0:5000/films/1')
    assert res.status_code == 401


def test_patch_film():
    """
    Test patch film by id
    """
    res = requests.patch('http://0.0.0.0:5000/films/2', json={
        "film_title": "America"
    })
    assert res.status_code == 401
