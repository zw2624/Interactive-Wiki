import json
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
        '''
        add actor into graph
        '''
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
        '''
        add movie into graph
        '''
        mid = movie['name']
        self.all_movies[mid] = movie
        return


    def delete_movie(self, movie_name):
        '''
        Delete the movie in the graph
        Also modified the actor objects
        '''
        for k, v in self.all_movies.items():
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
        '''
        Delete the actor in the graph.
        Also remove its appearance in movie
        '''
        for k, v in self.all_actors.items():
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
        '''
        add 'connection' attribute into actors
        '''
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
            heapq.heappush(ret, (sum(actor['connection'].values()), actor['name']))
        ret = heapq.nlargest(3, ret)
        return ret