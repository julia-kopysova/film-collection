from flask import jsonify, request

from app import application
from app.models import Film
from app.pagination import get_paginated_list
from app.resources.genre_resources import GenreListResource


@application.route('/genres_list', methods=['GET'])
def genres_list_pagination():
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
def search_film_by_name():
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
