import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('actors', __name__, url_prefix='/actors')


@bp.route('', methods=['GET'])
def filter():
    return

@bp.route('', methods=['POST'])
def create():
    return

@bp.route('/<actor_name>', methods=['GET'])
def get(actor_name):
    return

@bp.route('/<actor_name>', methods=['PUT'])
def update(actor_name):
    return

@bp.route('/<actor_name>', methods=['DELETE'])
def delete(actor_name):
    return
