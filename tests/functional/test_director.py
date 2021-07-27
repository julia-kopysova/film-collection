import requests


def test_get_directors():
    """
    Test get directors
    """
    res = requests.get('http://0.0.0.0:5000/directors')
    assert res.status_code == 200


def test_get_id_director():
    """
    Test get director by id
    """
    res = requests.get('http://0.0.0.0:5000/directors/1')
    assert res.status_code == 404

    res_1 = requests.get('http://0.0.0.0:5000/directors/3')
    res_json = res_1.json()
    assert res_1.status_code == 200
    assert res_json["first_name"] == "Melina"
    assert res_json["last_name"] == "Realina"


def test_post_directors():
    """
    Test post directors
    :return:
    """
    res = requests.post('http://0.0.0.0:5000/directors', json={"first_name": "Ann",
                                                               "last_name": "Ivanova"})
    assert res.status_code == 401


def test_delete_directors():
    """
    Test delete directors
    """
    res = requests.delete('http://0.0.0.0:5000/directors/3')
    assert res.status_code == 401


def test_patch_directors():
    """
    Test patch directors
    """
    res = requests.patch('http://0.0.0.0:5000/directors/3', json={"first_name": "Alan"})
    assert res.status_code == 401
