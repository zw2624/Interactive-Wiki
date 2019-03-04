'''
Reference: http://flask.pocoo.org/docs/1.0/tutorial/
'''
import os

from flask import Flask
from flaskr import actors, movies, analysis
from flaskr import graph
from flask import g

g = graph.graph()


root = ""
data_path = './data/data.json'

# global g


def create_app(test_config=None):
    # create and configure the app
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

    # global g
    # g = graph.graph()
    global g
    g.load_data(data_path)
    g.assign_connection()

    app.register_blueprint(actors.bp)
    app.register_blueprint(movies.bp)
    app.register_blueprint(analysis.bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app