from flask import (
    Blueprint, request, abort, jsonify, render_template
)
import json
bp = Blueprint('movies', __name__, url_prefix='/movies')

from flaskr import g

@bp.route('', methods=['GET'])
def filter_movie():
    ret = list(g.all_movies.values())
    args = [(k,v) for (k, v) in request.args.items()]
    for (ke, va) in args:
        vals = va.split('|')
        filter_func = lambda x, k=ke, val=vals : any(int(val) == x[k] for val in vals) if k == 'box_office' or k == 'wiki_page' else any(val in x[k] for val in vals)
        ret = [x for x in ret if filter_func(x)]
    text_ret = json.dumps(ret, sort_keys=False, indent=2)
    return render_template("show_json.html",text_ret = text_ret)


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
    return render_template("show_json.html",text_ret = movie), 201

@bp.route('/<movie_name>', methods=['GET'])
def get_movie(movie_name):
    movie_name = movie_name.replace('_', " ")
    print(movie_name)
    if movie_name in g.all_movies:
        movie = g.all_movies[movie_name]
    else:
        abort(404)
    return render_template("show_json.html",text_ret = movie), 201

@bp.route('/<movie_name>', methods=['PUT'])
def update_movie(movie_name):
    movie_name = movie_name.replace('_', " ")
    attrs = request.get_json()
    if movie_name not in g.all_movies:
        return render_template("show_json.html",text_ret = "no such movie, cannot update"), 400
    movie = g.all_movies[movie_name]
    for k,v in attrs.items():
       movie[k] = v
    text_ret = json.dumps(movie, sort_keys=False, indent=2)
    return render_template("show_json.html",text_ret = text_ret), 201

@bp.route('/<movie_name>', methods=['DELETE'])
def delete_movie(movie_name):
    movie_name = movie_name.replace('_', " ")
    global g
    success = g.delete_movie(movie_name)
    if success:
        return "", 201
    abort(400)