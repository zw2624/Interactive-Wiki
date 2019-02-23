
class graph:

    actor_to_movie = {}
    movie_to_actor = {}

    all_movies = {}
    all_actors = {}

    def add_edge(self, movie, actor):
        try:
            actor_list = self.movie_to_actor[movie.id]
        except KeyError:
            actor_list = []
            self.movie_to_actor[movie.id] = actor_list
        actor_list.append(actor)

        try:
            movie_list = self.actor_to_movie[actor.id]
        except KeyError:
            movie_list = []
            self.movie_to_actor[actor.id] = movie_list
        movie_list.append(movie)

        try:
            self.all_movies[movie.id]
        except KeyError:
            self.all_movies[movie.id] = movie

        try:
            self.all_actors[actor.id]
        except KeyError:
            self.all_actors[actor.id] = actor

        return
