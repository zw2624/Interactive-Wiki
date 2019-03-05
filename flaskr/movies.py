from flask import (
    Blueprint, flash, redirect, render_template, request, abort, jsonify
)

bp = Blueprint('movies', __name__, url_prefix='/movies')

from flaskr import g

@bp.route('', methods=['GET'])
def filter_movie():
    return


@bp.route('', methods=['POST'])
def create_movie():
    movie = request.get_json()
    if movie is None or 'name' not in movie:
        abort(400)
    movie["json_class"] = "Movie"
    if 'wiki_page' not in movie:
        movie['wiki_page'] = ''
    if 'box_office' not in movie:
        movie['box_office'] = 0
    if 'year' not in movie:
        movie['year'] = -1
    if 'actors' not in movie:
        movie['actors'] = []
    g.add_movie(movie)
    return jsonify(movie), 201

@bp.route('/<movie_name>', methods=['GET'])
def get_movie(movie_name):
    if movie_name in g.all_actors:
        movie = g.all_movies[movie_name]
    else:
        abort(404)
    return jsonify(movie), 201

@bp.route('/<movie_name>', methods=['PUT'])
def update_movie(movie_name):
    return

@bp.route('/<movie_name>', methods=['DELETE'])
def delete_movie(movie_name):
    global gs
    success = g.delete_movie(movie_name)
    if success:
        return "", 201
    abort(400)