
from flask import jsonify, request

from app import app, db
from app.models import Genre, Director
from app.schemas import genre_schema, director_schema


@app.route('/director/', methods=['GET'])
def get_directors():
    all_directors = Director.query.all()
    result = director_schema.dump(all_directors)
    return jsonify(result)


# adding a genre
@app.route('/director/', methods=['POST'])
def add_director():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    my_director = Director(first_name, last_name)
    db.session.add(my_director)
    db.session.commit()

    return director_schema.jsonify(my_director)
