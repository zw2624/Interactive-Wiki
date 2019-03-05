import functools

from flask import (
    Blueprint, flash, redirect, render_template, request,  url_for, jsonify, abort, session
)

from flaskr import g

bp = Blueprint('actors', __name__, url_prefix='/actors')


@bp.route('', methods=['GET'])
def filter():
    return

@bp.route('', methods=['POST'])
def create():
    global g
    actor = request.get_json()
    if actor is None or 'name' not in actor:
        abort(400)
    actor["json_class"] = "Actor"
    if 'age' not in actor:
        actor['age'] = -1
    if 'total_gross' not in actor:
        actor['total_gross'] = 0
    if 'movies' not in actor:
        actor['movies'] = []
    g.add_actor(actor)
    return "", 201

@bp.route('/<actor_name>', methods=['GET'])
def get(actor_name):
    if actor_name in g.all_actors:
        actor = g.all_actors[actor_name]
    else:
        abort(404)
    return jsonify(actor), 201

@bp.route('/<actor_name>', methods=['PUT'])
def update(actor_name):
    global g
    dict = request.get_json()
    actor = g.all_actors[actor_name]
    for k,v in dict.items():
        actor[k] = v
    return jsonify(actor), 201

@bp.route('/<actor_name>', methods=['DELETE'])
def delete(actor_name):
    global g
    success = g.delete_actor(actor_name)
    if success:
        return "", 201
    abort(400)
