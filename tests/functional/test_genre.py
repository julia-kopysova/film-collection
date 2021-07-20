import requests


def test_get_genres():
    """
    Test get genres
    """
    res = requests.get('http://0.0.0.0:5000/genres')
    assert res.status_code == 200


def test_get_id_genre():
    """
    Test get id genre
    """
    res = requests.get('http://0.0.0.0:5000/genres/1')
    res_json = res.json()
    assert res.status_code == 200
    assert res_json["genre_title"] == "Comedy"


def test_post_genres():
    """
    Test post genres
    :return:
    """
    res = requests.post('http://0.0.0.0:5000/genres', json={"genre_title": "Family"})
    assert res.status_code == 401


def test_delete_genres():
    """
    Test delete genres
    """
    res = requests.delete('http://0.0.0.0:5000/genres/1')
    assert res.status_code == 401


def test_patch_genres():
    """
    Test patch genres
    """
    res = requests.patch('http://0.0.0.0:5000/genres/1', json={"genre_title": "Horror"})
    assert res.status_code == 401
