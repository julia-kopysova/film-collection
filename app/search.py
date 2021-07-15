"""
Module for search films by title and filter films
"""
from flask import jsonify, request, Response
from sqlalchemy import extract

from app import application
from app.models import Film, Genre, Director
from app.pagination import get_paginated_list
from app.resources.film_resources import FilmListResource
from app.resources.genre_resources import GenreListResource


@application.route('/genres_list', methods=['GET'])
def genres_list_pagination() -> Response:
    """
    Paginated genres
    :return: jsonify
    """
    return jsonify(get_paginated_list(
        GenreListResource.get(),
        '/genres_list',
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 3)
    ))


@application.route('/search_film', methods=['GET'])
def search_film_by_name() -> Response:
    """
    Search film by partial coincidence
    :return: paginated jsonify
    """
    part_name = request.args.get('name')
    search = "%{}%".format(part_name)
    films = Film.query.filter(Film.film_title.like(search)).all()
    film_list = [{
        'film_id': film.film_id,
        'film_title': film.film_title
    } for film in films]

    return jsonify(get_paginated_list(
        film_list,
        '/search_film',
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 10),
        name=part_name
    ))


@application.route('/films_filter', methods=['GET'])
def filter_films() -> Response:
    """
    Filters films by parameters
    :return: jsonify
    """
    year_start = request.args.get('year_start', default=1900)
    year_end = request.args.get('year_end', default=2030)
    first_name = request.args.get('first_name', None)
    last_name = request.args.get('last_name', None)
    genre_title = request.args.get('genre_title', None)
    if genre_title is None and year_end is None and year_start is None \
            and first_name is None and last_name is None:
        return FilmListResource.get()
    elif genre_title and year_start and year_end and first_name and last_name:
        films = Film.query.join(Film.genres).filter(Genre.genre_title == genre_title).\
            join(Director, Film.director_id == Director.director_id).\
            filter(Director.first_name == first_name, Director.last_name == last_name).\
            filter(extract('year', Film.release_date).between(year_start, year_end))
    elif genre_title and year_end and year_start:
        films = Film.query.join(Film.genres).filter(Genre.genre_title == genre_title). \
            filter(extract('year', Film.release_date).between(year_start, year_end))
    elif first_name and last_name and year_end and year_start:
        films = Film.query.join(Director, Film.director_id == Director.director_id). \
            filter(Director.first_name == first_name, Director.last_name == last_name). \
            filter(extract('year', Film.release_date).between(year_start, year_end))
    elif first_name and last_name and genre_title:
        films = Film.query.join(Director, Film.director_id == Director.director_id). \
            filter(Director.first_name == first_name, Director.last_name == last_name). \
            join(Film.genres).filter(Genre.genre_title == genre_title)
    elif first_name and last_name:
        films = Film.query.join(Director, Film.director_id == Director.director_id).\
            filter(Director.first_name == first_name, Director.last_name == last_name)
    elif year_end and year_start:
        films = Film.query.filter(extract('year', Film.release_date).between(year_start, year_end))
    elif genre_title:
        films = Film.query.join(Film.genres).filter(Genre.genre_title == genre_title)
    else:
        return jsonify({
            "status": 401,
            "reason": "Filtering data is set incorrectly"
        })

    return jsonify([{
        'film_id': film.film_id,
        'film_title': film.film_title,
        'release_date': film.release_date,
        'rating': film.rating,
        'poster': film.poster

    } for film in films])
