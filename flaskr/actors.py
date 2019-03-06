from flask import (
    Blueprint, request, jsonify, abort, render_template
)
import json

from flaskr import g

bp = Blueprint('actors', __name__, url_prefix='/actors')

# https://stackoverflow.com/questions/23862406/filter-items-in-a-python-dictionary-where-keys-contain-a-specific-string
@bp.route('', methods=['GET'])
def filter():
    '''
    Usage: /actors?attr={attr_value}
    Example: /actors?name=Bob
    Filters out all actors that don’t have “Bob” in their name
    '''
    ret = list(g.all_actors.values())
    for (ke, va) in request.args.items():
        vals = va.split('|')
        filter_func = lambda x, k=ke, val=vals : any([int(val) == x[k] for val in vals]) if k == 'age' or k == 'total_gross' else any([val in x[k] for val in vals])
        ret = [x for x in ret if filter_func(x)]
    text_ret = json.dumps(ret, sort_keys=False, indent=2)
    return render_template("show_json.html",text_ret = text_ret)

@bp.route('', methods=['POST'])
def create():
    '''
    Usage: curl -i -X POST -H "Content-Type: application/json" -d'{"name":"Billy Joe"}' {API URL}/actors
    Leverage POST requests to ADD content to backend
    :return:
    '''
    global g
    actor = request.get_json()
    if actor is None or 'name' not in actor:
        abort(400)
    actor["name"] = actor["name"].replace('_', " ")
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
    '''
    Usage: actors/:{actor_name}
    Example: /actors/Bruce_Willis
    Returns the first Actor object that has name “Bruce Willis”, displays actor attributes and metadata
    '''
    actor_name = actor_name.replace('_', " ")
    if actor_name in g.all_actors:
        actor = g.all_actors[actor_name]
    else:
        abort(404)
    text_ret = json.dumps(actor, sort_keys=False, indent=2)
    return render_template("show_json.html",text_ret = text_ret), 201

@bp.route('/<actor_name>', methods=['PUT'])
def update(actor_name):
    '''
    Usage: curl -i -X PUT -H "Content-Type: application/json" -d ' {"total_gross":500}' {api url}/actors/Bruce_Willis
    Leverage PUT requests to update standing content in backend
    '''
    actor_name = actor_name.replace('_', " ")
    global g
    dict = request.get_json()
    actor = g.all_actors[actor_name]
    for k,v in dict.items():
        actor[k] = v
    text_ret = json.dumps(actor, sort_keys=False, indent=2)
    return render_template("show_json.html",text_ret = text_ret), 201

@bp.route('/<actor_name>', methods=['DELETE'])
def delete(actor_name):
    '''
    Usage: curl -i -X DELETE -H "Content-Type: application/json" {API URL}/actors/Bruce_Willis
    Leverage DELETE requests to REMOVE content from backend
    '''
    actor_name = actor_name.replace('_', " ")
    global g
    success = g.delete_actor(actor_name)
    if success:
        return "", 201
    abort(400)
