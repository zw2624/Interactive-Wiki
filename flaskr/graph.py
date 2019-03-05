import json
from datetime import datetime
import networkx


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
        self.nx = networkx.Graph()

    def add_actor(self, actor):
        aid = actor['name']
        self.all_actors[aid] = actor
        for mid in actor['movies']:
            if mid in self.all_movies:
                movie = self.all_movies[mid]
                if aid not in movie['actors']:
                    movie['actors'].append(aid)
            else:
                movie = {}
                movie['json_class'] = "Movie"
                movie['name'] = mid
                movie["wiki_page"] = ""
                movie['box_office'] = 0
                movie['year'] = 0
                movie['actors'] = [aid]
                self.all_movies[mid] = movie
        return

    def add_movie(self, movie):
        return


    def delete_movie(self, movie_name):
        for k, v in self.all_movies:
            if v['name'] == movie_name:
                box = v['box_office']
                for aid in v['actors']:
                    try:
                        actor = self.all_actors[aid]
                        actor['total_gross'] -= box
                        actor['movies'].remove(movie_name)
                    except Exception:
                        pass
                del self.all_movies[k]
                return True
        return False

    def delete_actor(self, actor_name):
        for k, v in self.all_actors:
            if v['name'] == actor_name:
                for mid in v['movies']:
                    try:
                        movie = self.all_movies[mid]
                        movie['actors'].remove(actor_name)
                    except Exception:
                        pass
                del self.all_actors[k]
                return True
        return False


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

    def assign_connection(self):
        for k, v in self.all_actors.items():
            v['connection'] = {}
        for k, v in self.all_movies.items():
            aids = v['actors']
            for target in aids:
                try:
                    actor = self.all_actors[target]
                    for aid in aids:
                        if target == aid:
                            continue
                        if aid not in self.all_actors:
                            continue
                        if aid in actor['connection']:
                            actor['connection'][aid] += 1
                        else:
                            actor['connection'][aid] = 1
                except Exception:
                    continue

    def get_actor_most_connection(self):
        '''
        get 5 actors who has most connections
        '''
        import heapq
        ret = []
        for actor_id in self.all_actors:
            actor = self.all_actors[actor_id]
            heapq.heappush(ret, (len(actor['connection']), actor['name']))
        ret = heapq.nlargest(5, ret)
        return ret


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
        ret = {}
        for k, v in self.all_movies.items():
            if v['year'] == year:
                ret[k] = v
        return ret

    def get_actor_by_movies(self, movie_id):
        '''
        List which actors worked in a movie
        :param actor_name: the name of the movie
        :return: [models.actors]
        '''
        return self.all_movies[movie_id]['actors']

    def get_actor_most_gross(self, X):
        '''
        List the top X actors with the most total grossing value
        :param X: number of actors to be shown
        :return: [models.actors]
        '''
        import heapq
        ret = []
        for actor_id in self.all_actors:
            actor = self.all_actors[actor_id]
            heapq.heappush(ret, (actor['total_gross'], actor['name']))
        ret = heapq.nlargest(X, ret)
        return ret

    def get_actor_oldest(self, X):
        '''
        List the oldest X actors
        :param X: number of actors to be shown
        :return: [models.actors]
        '''
        import heapq
        ret = []
        for actor_id in self.all_actors:
            actor = self.all_actors[actor_id]
            heapq.heappush(ret, (actor['age'], actor['name']))
        ret = heapq.nlargest(X, ret)
        return ret

    def get_actor_by_year(self, year):
        '''
        List all the actors for a given year
        :param year: selected year
        :return: [models.actors]
        '''
        ret = {}
        for k, v in self.all_actors.items():
            if v['age'] == 2019 - year:
                ret[k] = v
        return ret