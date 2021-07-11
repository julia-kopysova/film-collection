
"""
Module for managing project
"""
from flask import jsonify
from flask.cli import FlaskGroup

from app import app, db, api, urls
from app.models import Genre
from app.resources.genre_resources import GenreListResource, GenreResource

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    """
    Method for creating database
    :return:
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


# @app.route('/genres/', methods=['GET'])
# def get_genres():
#     # all_genres = Genre.query.all()
#     # return 'lalala'
#     # result = genre_schema.dump(all_genres)
#     # return jsonify(result)
#     return jsonify([{
#         'genre_id': genre.genre_id,
#         'genre_title': genre.genre_title
#     } for genre in Genre.query.all()])
# api.add_resource(GenreListResource, '/genres')
# api.add_resource(GenreResource, '/genres/<int:genre_id>')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, use_debugger=False, use_reloader=False)
