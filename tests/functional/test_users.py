def test_films(client):
    res = client.get('/genres_list')
    assert res.status_code == 200
