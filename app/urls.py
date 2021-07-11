from app import api
from app.resources.genre_resources import GenreListResource, GenreResource

api.add_resource(GenreListResource, '/genres')
api.add_resource(GenreResource, '/genres/<int:genre_id>')
