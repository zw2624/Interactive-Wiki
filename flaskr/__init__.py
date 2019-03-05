'''
Reference: http://flask.pocoo.org/docs/1.0/tutorial/
'''
import os
from flask import Flask, render_template, session
from flaskr import graph

root = ""
data_path = './data/data.json'
g = graph.graph()
g.load_data(data_path)
g.assign_connection()


from flaskr import actors, movies, analysis

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.register_blueprint(actors.bp)
    app.register_blueprint(movies.bp)
    app.register_blueprint(analysis.bp_connect)
    app.register_blueprint(analysis.bp_gross)
    app.register_blueprint(analysis.bp_visual)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('index.html')

    return app