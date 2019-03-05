import json
import copy
from bokeh.plotting import figure, show
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool
from bokeh.models.graphs import from_networkx, NodesAndLinkedEdges, EdgesAndLinkedNodes, NodesOnly
from bokeh.embed import components
from flaskr import g
import networkx

from flask import (
    Blueprint,render_template, request
)

bp_connect = Blueprint('connections', __name__, url_prefix='/connections')
Spectral4 = ['#225ea8', '#41b6c4', '#a1dab4', '#ffffcc']

@bp_connect.route('/', methods=['GET'])
def connections():
    tops = g.get_actor_most_connection()
    ret = {}
    for tup in tops:
        aid = tup[1]
        ret[aid] = copy.deepcopy(g.all_actors[aid])
        del ret[aid]['connection']
        del ret[aid]['movies']
    text_ret= json.dumps(ret, sort_keys=False, indent=2)
    nx = networkx.Graph()
    for aid in g.all_actors:
        nx.add_node(aid, actor_name = aid)

    for aid in g.all_actors:
        for k in g.all_actors[aid]['connection']:
            nx.add_edge(aid, k)

    p = Plot(plot_width=800, plot_height=1000,
                x_range=Range1d(-2, 2), y_range=Range1d(-2.5, 2.5))
    p.title.text = "Graph Interaction Demonstration"
    p.add_tools(HoverTool(tooltips=[("Name", "@actor_name")]), TapTool(), BoxSelectTool())

    graph_renderer = from_networkx(nx, networkx.spring_layout, scale=7, center=(0, 0))
    #print(graph_renderer.node_renderer.data_source.data.keys())
    graph_renderer.node_renderer.glyph = Circle(size=10, fill_color=Spectral4[0])
    graph_renderer.node_renderer.selection_glyph = Circle(size=10, fill_color=Spectral4[2])
    graph_renderer.node_renderer.hover_glyph = Circle(size=10, fill_color=Spectral4[1])

    graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=1)
    graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=1)
    graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=1)

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = NodesOnly()
    p.renderers.append(graph_renderer)
    script, div = components(p)
    return render_template("connection.html", script=script, div=div,text_ret = text_ret)


bp_gross = Blueprint('gross_analysis', __name__, url_prefix='/gross_analysis')


@bp_gross.route('/')
def gross_analysis():
    feature_name = request.args.get('feature')
    feature_names = ["age", "connection", "movies"]
    if feature_name == None:
        feature_name = "age"
    actor_dict = g.all_actors
    xs = []
    ys = []
    for k, v in actor_dict.items():
        try:
            xs.append(len(v[feature_name].keys()))
        except Exception:
            if feature_name == 'movies':
                xs.append(len(v[feature_name]))
            else:
                xs.append(v[feature_name])
        ys.append(v['total_gross'])
    p = figure(width=600, height=400)
    p.circle(xs, ys)
    script, div = components(p)
    return render_template("gross.html", script=script, div=div,
                           feature_names=feature_names, current_feature_name=feature_name)

bp_visual = Blueprint('visualization', __name__, url_prefix='/v')


@bp_gross.route('/')
def gross_visual():
    feature_name = request.args.get('feature')
    feature_names = ["age", "connection", "movies"]
    if feature_name == None:
        feature_name = "age"
    actor_dict = g.all_actors
    xs = []
    ys = []
    for k, v in actor_dict.items():
        try:
            xs.append(len(v[feature_name].keys()))
        except Exception:
            if feature_name == 'movies':
                xs.append(len(v[feature_name]))
            else:
                xs.append(v[feature_name])
        ys.append(v['total_gross'])
    p = figure(width=600, height=400)
    p.circle(xs, ys)
    script, div = components(p)
    return render_template("gross.html", script=script, div=div,
                           feature_names=feature_names, current_feature_name=feature_name)