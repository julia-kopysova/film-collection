"""
Module for pagination
"""
from flask import abort


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
