import json
from Model.models import actors, films
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


    def write_to_json(self, path):
        '''
        Load Json data into graph
        :param actor_file: path to actors data
        :param film_file: path to film data
        '''
        with open(path + 'actors_demo.jl', 'w+') as actors_json:
            for actor in self.all_actors.values():
                line = json.dumps(actor.__dict__) + '\n'
                actors_json.write(line)
            actors_json.close()
        with open(path + 'movies_demo.jl', 'w+') as movies_json:
            for film in self.all_movies.values():
                line = json.dumps(film.__dict__) + '\n'
                movies_json.write(line)
            movies_json.close()
        with open(path + 'graph_demo.jl', 'w+') as graph_json:
            for mta in self.movie_to_actor.items():
                line = json.dumps(mta) + '\n'
                graph_json.write(line)
            for atm in self.actor_to_movie.items():
                line2 = json.dumps(atm) + '\n'
                graph_json.write(line2)
            graph_json.close()
        return

    def load_json(self, actor_file, film_file):
        '''
        Load Json data into graph
        :param actor_file: path to actors data
        :param film_file: path to film data
        '''
        for line in open(film_file, 'r'):
            l = line.rstrip('\n')
            if l is '':
                break
            film = json.loads(l)
            new = films()
            new.id = film['id']
            new.name = film['name']
            new.release = film['release']
            new.box_office = film['box_office']
            new.actors_id = film['actors_id']
            new.total_actors = film['total_actors']
            self.add_movie(new)

        for line in open(actor_file, 'r'):
            l = line.rstrip('\n')
            if l is '':
                break
            actor = json.loads(l)
            new = actors()
            new.id = actor['id']
            new.name = actor['name']
            new.birth = actor['birth']
            new.movie_ids = actor['movie_ids']
            new.total_gross = actor['total_gross']
            new.movie_num = actor['movie_num']
            self.add_actor(new)

        for actor_id in self.all_actors:
            actor = self.all_actors[actor_id]
            for movie_id in actor.movie_ids:
                movie = self.all_movies[movie_id]
                wei = self.cal_weight(movie, actor)
                self.add_edge(movie_id, actor_id, wei)

        return

    def get_movie_gross(self, movie_id):
        '''
        Find how much a movie has grossed
        :return:
        '''
        return int(self.all_movies[movie_id].box_office)

    def get_movie_by_actor(self, actor_id):
        '''
        List which movies an actor has worked in
        :param actor_name: the name of the actor
        :return: [models.films]
        '''
        return self.all_actors[actor_id].movie_ids

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