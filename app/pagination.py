from flask import jsonify, request, abort

from app import application
from app.models import Film
from app.resources.genre_resources import GenreListResource


def get_paginated_list(results, url, start, limit, name=None):
    """
    Function for pagination
    :param results: collection of json-objects
    :param url: url that will be used
    :param start: number element from that sequence will be start
    :param limit: elements on page
    :param name: default=None,
    :return: obj
    """
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start:
        abort(404)
    obj = {'start': start, 'limit': limit, 'count': count}
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d&name=%s' % (start_copy, limit_copy, name)
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d&name=%s' % (start_copy, limit, name)
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj


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
