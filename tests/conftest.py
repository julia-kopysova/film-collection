import pytest

from app import application, create_app
from app.models import Director, User, Genre, FilmHasGenre, Film


@pytest.fixture
def application():
    application = create_app()
    return application


@pytest.fixture
def client():
    with application.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def new_director():
    director = Director("John", "Smith")
    return director


@pytest.fixture(scope="module")
def new_user():
    user = User("kim_lee", "Kim", "Lee", "kimlee@gmail.com", "1234", False)
    return user


@pytest.fixture(scope="module")
def new_genre():
    genre = Genre("Comedy")
    return genre


@pytest.fixture(scope="module")
def new_film_genre():
    film_has_genre = FilmHasGenre(1, 1)
    return film_has_genre


@pytest.fixture(scope="module")
def new_film():
    film = Film("Time", "2020-07-11T20:45:04", "description", 8, "/src", 1, 1)
    return film
