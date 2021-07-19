import pytest

from app import User
from app.models import Film


def test_new_director(new_director):
    """
    Get a director
    Check if data is create object
    """
    assert new_director.first_name == "John"
    assert new_director.last_name == "Smith"


def test_new_user(new_user):
    """
    Get a user
    Check if data is create object
    """
    assert new_user.username == "kim_lee"
    assert new_user.first_name == "Kim"
    assert new_user.last_name == "Lee"
    assert new_user.email == "kimlee@gmail.com"
    assert new_user.password == "1234"
    assert new_user.is_superuser is False


def test_new_genre(new_genre):
    """
    Get a genre
    Check if data is create object
    """
    assert new_genre.genre_title == "Comedy"


def test_new_film(new_film_genre):
    """
    Get a user
    Check if data is create object
    """
    assert new_film_genre.genre_id == 1
    assert new_film_genre.film_id == 1


def test_new_film(new_film):
    """
    Get a director
    Check if data is create object
    """
    assert new_film.film_title == "Time"
    assert new_film.description == "description"
    assert new_film.release_date == "2020-07-11T20:45:04"
    assert new_film.rating == 8
    assert new_film.poster == "/src"
    assert new_film.director_id == 1
    assert new_film.user_id == 1


def test_validation_email():
    with pytest.raises(AssertionError):
        User("kim_lee", "Kim", "Lee", "email", "1234", False)


def test_validation_username():
    with pytest.raises(AssertionError):
        User("k", "Kim", "Lee", "email@gmail.com", "1234", False)


@pytest.mark.parametrize("rating_param", [200, -29])
def test_validation_rating(rating_param):
    with pytest.raises(AssertionError):
        Film("Time", "2020-07-11T20:45:04", "description", rating_param, "/src", 1, 1)
