
"""
Module for managing project
"""
import logging

from app.resources.director_resources import DirectorListResource, DirectorResource
from app.resources.film_resources import FilmListResource, FilmResource
from app.resources.genre_resources import GenreListResource, GenreResource
from app.resources.user_resouces import UserListResource, UserResource

from app import api, application

# cli = FlaskGroup(app)
from app.swagger import swaggerui_blueprint

api.add_resource(GenreListResource, '/genres')
api.add_resource(GenreResource, '/genres/<int:genre_id>')

api.add_resource(DirectorListResource, '/directors')
api.add_resource(DirectorResource, '/directors/<int:director_id>')

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

api.add_resource(FilmListResource, '/films')
api.add_resource(FilmResource, '/films/<int:film_id>')


if __name__ == "__main__":
    application.debug = True
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    application.register_blueprint(swaggerui_blueprint)
    application.run(debug=True, host='0.0.0.0', port=5000, use_debugger=False, use_reloader=False)
