"""
Module for search films by title and filter films
"""
from datetime import date

from flask import jsonify, request, Response
from sqlalchemy import extract

from app import application
from app.models import Film, Genre, Director
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
    films = Film.query.filter(Film.film_title.ilike(search)).all()
    film_list = [{
        'film_id': film.film_id,
        'film_title': film.film_title,
        'rating': film.rating,
        'release_date': film.release_date
    } for film in films]
    application.logger.info('Searching by %s', part_name)
    return jsonify(get_paginated_list(
        film_list,
        '/search_film',
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 10),
        name=part_name
    ))


@application.route('/films_years_filter', methods=['GET'])
def filter_films_by_years() -> Response:
    """
    Filters films between years
    :return: jsonify
    """
    todays_date = date.today()
    year_start = request.args.get('year_start', default=1900, type=int)
    year_end = request.args.get('year_end', default=todays_date.year, type=int)
    films = Film.query.filter(extract('year', Film.release_date).between(year_start, year_end))
    application.logger.info("Filter by years: %d and %d",
                            year_start, year_end)
    return jsonify([{
            'film_id': film.film_id,
            'film_title': film.film_title,
            'release_date': film.release_date,
            'rating': film.rating,
            'poster': film.poster
        } for film in films])


@application.route('/films_director_filter', methods=['GET'])
def filter_films_by_director() -> Response:
    """
    Filters films by director
    :return: jsonify
    """
    first_name = request.args.get('first_name', type=str)
    last_name = request.args.get('last_name', type=str)
    if first_name and last_name:
        films = Film.query.join(Director, Film.director_id == Director.director_id). \
                    filter(Director.first_name == first_name, Director.last_name == last_name)
        application.logger.info("Filter by director: %s and %s",
                                first_name, last_name)
        return jsonify([{
                'film_id': film.film_id,
                'film_title': film.film_title,
                'release_date': film.release_date,
                'rating': film.rating,
                'poster': film.poster
            } for film in films])
    return jsonify({"status": 401,
                    "reason": "Enter first name and last name"})


@application.route('/films_genre_filter', methods=['GET'])
def filter_films_by_genre() -> Response:
    """
    Filters films by genre
    :return: jsonify
    """
    genre_title = request.args.get('genre_title', None, type=str)
    if genre_title:
        films = Film.query.join(Film.genres).filter(Genre.genre_title == genre_title)
        application.logger.info("Filter by genre: %s",
                                genre_title)
        return jsonify([{
                'film_id': film.film_id,
                'film_title': film.film_title,
                'release_date': film.release_date,
                'rating': film.rating,
                'poster': film.poster

            } for film in films])
    return jsonify({
            "status": 404,
            "reason": "Enter genre title"
        })
