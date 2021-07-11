from app import api
from app.resources.director_resources import DirectorListResource, DirectorResource
from app.resources.genre_resources import GenreListResource, GenreResource

api.add_resource(GenreListResource, '/genres')
api.add_resource(GenreResource, '/genres/<int:genre_id>')

api.add_resource(DirectorListResource, '/directors')
api.add_resource(DirectorResource, '/directors/<int:director_id>')
