import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('actors', __name__, url_prefix='/actors')


@bp.route('', methods=['GET'])
def filter():
    return

@bp.route('', methods=['POST'])
def create():
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
    return jsonify(actor), 201

@bp.route('/<actor_name>', methods=['GET'])
def get(actor_name):
    return

@bp.route('/<actor_name>', methods=['PUT'])
def update(actor_name):
    return

@bp.route('/<actor_name>', methods=['DELETE'])
def delete(actor_name):
    return
