import models
import json


class graph:

    actor_to_movie = {}
    movie_to_actor = {}

    all_movies = {}
    all_actors = {}

    def __init__(self):
        self.movie_num = 0
        self.actor_num = 0

    def add_edge(self, movie, actor):
        wei = self.cal_weight(movie, actor)

        try:
            actor_list = self.movie_to_actor[movie.id]
        except KeyError:
            actor_list = []
        self.movie_to_actor[movie.id] = (actor_list, wei)
        actor_list.append(actor)

        try:
            movie_list = self.actor_to_movie[actor.id]
        except KeyError:
            movie_list = []
        self.actor_to_movie[actor.id] = (movie_list, wei)
        movie_list.append(movie)

        return

    def add_movie(self, movie):
        try:
            self.all_movies[movie.id]
        except KeyError:
            self.all_movies[movie.id] = movie
            self.movie_num += 1
        return

    def add_actor(self, actor):
        try:
            self.all_actors[actor.id]
        except KeyError:
            self.all_actors[actor.id] = actor
            self.actor_num += 1
        return

    def cal_weight(self, movie, actor):
        return 1

    def write_to_json(self, path):
        with open('actors_demo.jl', 'w+') as actors_json:
            for actor in self.all_actors.values():
                line = json.dumps(actor.__dict__) + '\n'
                actors_json.write(line)
            actors_json.close()
        with open('movies_demo.jl', 'w+') as movies_json:
            for film in self.all_movies.values():
                line = json.dumps(film.__dict__) + '\n'
                movies_json.write(line)
            movies_json.close()
        with open('graph_demo.jl', 'w+') as graph_json:
            for mta in self.movie_to_actor.items():
                line = json.dumps(mta) + '\n'
                graph_json.write(line)
            for atm in self.actor_to_movie.items():
                line2 = json.dumps(atm) + '\n'
                graph_json.write(line2)
            graph_json.close()
        return

    def load_json(self, path):
        return

    def get_movie_gross(self):
        '''
        Find how much a movie has grossed
        :return:
        '''
        return

    def get_movie_by_actor(self, actor_name):
        '''
        List which movies an actor has worked in
        :param actor_name: the name of the actor
        :return: [models.films]
        '''
        return

    def get_movie_by_year(self, year):
        '''
        List all the movies for a given year
        :param year: selected year
        :return: [models.films]
        '''
        return

    def get_actor_by_movies(self, actor_name):
        '''
        List which actors worked in a movie
        :param actor_name: the name of the movie
        :return: [models.actors]
        '''
        return

    def get_actor_most_gross(self, X):
        '''
        List the top X actors with the most total grossing value
        :param X: number of actors to be shown
        :return: [models.actors]
        '''
        return

    def get_actor_oldest(self, X):
        '''
        List the oldest X actors
        :param X: number of actors to be shown
        :return: [models.actors]
        '''
        return

    def get_actor_by_year(self, year):
        '''
        List all the actors for a given year
        :param year: selected year
        :return: [models.actors]
        '''
        return