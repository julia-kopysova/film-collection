
"""
Module for managing project
"""
from flask import jsonify
from flask.cli import FlaskGroup
from flask_marshmallow import Marshmallow
from flask_restful import Api
from app.resources.director_resources import DirectorListResource, DirectorResource
from app.resources.film_resources import FilmListResource, FilmResource
from app.resources.genre_resources import GenreListResource, GenreResource
from app.resources.user_resouces import UserListResource, UserResource

from app import api, application

# cli = FlaskGroup(app)

api.add_resource(GenreListResource, '/genres')
api.add_resource(GenreResource, '/genres/<int:genre_id>')

api.add_resource(DirectorListResource, '/directors')
api.add_resource(DirectorResource, '/directors/<int:director_id>')

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

api.add_resource(FilmListResource, '/films')
api.add_resource(FilmResource, '/films/<int:film_id>')


# @app.route('/')
# def hello_world():
#     """
#     Hello Word method
#     :return:
#     """
#     return 'Hello World!!!!'
# @cli.command("create_db")
# def create_db():
#     """
#     Method for creating database
#     :return:
#     """
#     db.drop_all()
#     db.create_all()
#     db.session.commit()


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

from app import models
if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0', port=5000, use_debugger=False, use_reloader=False)
