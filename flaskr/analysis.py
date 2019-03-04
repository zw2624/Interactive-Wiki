import flaskr.graph
import functools
import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@bp.route('/connections', methods=['GET'])
def connections():
    global g
    print(g.all_actors.itmes())
    return


@bp.route('/regression', methods=['GET'])
def regression():
    return