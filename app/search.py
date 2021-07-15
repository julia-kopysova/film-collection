"""
Module for search films by title and filter films
"""
from flask import jsonify, request, Response

from app import application
from app.models import Film, Genre
from app.pagination import get_paginated_list
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
    # year_start = request.args.get('year_start', None)
    # year_end = request.args.get('year_end', None)
    # first_name = request.args.get('first_name', None)
    # last_name = request.args.get('last_name', None)
    genre_title = request.args.get('genre_title', None)
    # films = Film.query.filter(extract('year', Film.release_date).between(year_start, year_end))
    # films = Film.query.join(Director, Film.director_id == Director.director_id).filter(
    #     Director.first_name == first_name, Director.last_name == last_name)
    films = Film.query.join(Film.genres).filter(Genre.genre_title == genre_title)
    return jsonify([{
        'film_id': film.film_id,
        'film_title': film.film_title,
        'release_date': film.release_date

    } for film in films])
