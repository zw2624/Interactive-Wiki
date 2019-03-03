import json

from flaskr.models import actors, films
from datetime import datetime

'''
Graph contains all films and actors objects as well as dictionaries of their connection.
Includes Query Functions
'''
class graph:

    def __init__(self):
        self.actor_to_movie = {}
        self.movie_to_actor = {}
        self.all_movies = {}
        self.all_actors = {}
        self.movie_num = 0
        self.actor_num = 0

    def add_edge(self, movie_id, actor_id, w):
        '''
        add edge for graph
        :param movie_id:
        :param actor_id:
        :param w: weight of the actor
        '''
        if movie_id not in self.movie_to_actor:
            self.movie_to_actor[movie_id] = [(actor_id, w)]
        else:
            self.movie_to_actor[movie_id].append((actor_id, w))

        if actor_id not in self.actor_to_movie:
            self.actor_to_movie[actor_id] = [(movie_id, w)]
        else:
            self.actor_to_movie[actor_id].append((movie_id, w))

        return

    def add_movie(self, movie):
        '''
        add movie to the graph movie dictionary
        '''
        if movie.id not in self.all_movies:
            self.all_movies[movie.id] = movie
            self.movie_num = self.movie_num + 1
        return

    def add_actor(self, actor):
        '''
        add actor to the graph movie dictionary
        '''
        if actor.id not in self.all_actors:
            self.all_actors[actor.id] = actor
            self.actor_num += 1
        return

    def cal_weight(self, movie, actor_id):
        '''
        calculate the weight of an actor node in a edge
        '''
        if actor_id in self.all_actors:
            actor = self.all_actors[actor_id]
            if actor is not None:
                return actor.total_gross
        else:
            return -1

    def complet_gross(self):
        '''
        used after scraper ran. add movies to actors
        '''
        for movie_id in self.all_movies:
            movie = self.all_movies[movie_id]
            for actor_id in movie.actors_id:
                if actor_id in self.all_actors:
                    self.all_actors[actor_id].add_movie(movie)

    def build_edge(self):
        '''
        build edges based on data
        '''
        for movie_id in self.all_movies:
            movie = self.all_movies[movie_id]
            for actor_id in movie.actors_id:
                w = self.cal_weight(movie, actor_id)
                self.add_edge(movie_id, actor_id, w)
        return

    def load_data(self, data_path):
        '''
        ** for assignment 2.1 **
        Load data from given file
        :param data_path: path to the data.json
        '''
        with open(data_path) as f:
            data = json.load(f)
        self.all_actors = data[0]
        self.all_movies = data[1]



    def get_movie_gross(self, movie):
        '''
        Find how much a movie has grossed
        :return:
        '''
        return self.all_movies[movie]['box office']

    def get_movie_by_actor(self, actor):
        '''
        List which movies an actor has worked in
        :param actor_name: the name of the actor
        :return: [models.films]
        '''
        return self.all_actors[actor]['movies']

    def get_movie_by_year(self, year):
        '''
        List all the movies for a given year
        :param year: selected year
        :return: [models.films]
        '''
        ret = []
        for movie_id in self.all_movies:
            movie = self.all_movies[movie_id]
            if movie.release is not None:
                try:
                    dt = datetime.strptime(str(movie.release), '%Y-%m-%d')
                    if dt.year == year:
                        ret.append(movie_id)
                except Exception:
                    pass
        return ret

    def get_actor_by_movies(self, movie_id):
        '''
        List which actors worked in a movie
        :param actor_name: the name of the movie
        :return: [models.actors]
        '''
        return self.all_movies[movie_id].actors_id

    def get_actor_most_gross(self, X):
        '''
        List the top X actors with the most total grossing value
        :param X: number of actors to be shown
        :return: [models.actors]
        '''
        mylist = []
        for actor_id in self.all_actors:
            actor = self.all_actors[actor_id]
            if actor.total_gross is not None:
                mylist.append((actor_id, int(actor.total_gross)))
        mylist.sort(key=lambda x: -x[1])
        return mylist[0:X]

    def get_actor_oldest(self, X):
        '''
        List the oldest X actors
        :param X: number of actors to be shown
        :return: [models.actors]
        '''
        mylist = []
        for actor_id in self.all_actors:
            actor = self.all_actors[actor_id]
            if actor.birth is not None:
                dt = datetime.strptime(actor.birth, '%Y-%m-%d')
                mylist.append((actor_id, dt))
        mylist.sort(key=lambda x: x[1])
        return mylist[0:X]

    def get_actor_by_year(self, year):
        '''
        List all the actors for a given year
        :param year: selected year
        :return: [models.actors]
        '''
        ret = []
        for actor_id in self.all_actors:
            actor = self.all_actors[actor_id]
            if actor.birth is not None:
                dt = datetime.strptime(actor.birth, '%Y-%m-%d')
                if dt.year == year:
                    ret.append(actor_id)
        return ret