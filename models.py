
class films:

    def __init__(self):
        self.id = -1
        self.name = None
        self.release = None
        self.box_office = None
        self.actors_id = []
        self.total_actors = 0


    def add_actor(self, actor):
        self.actors_id.append(actor)
        self.total_actors += 1



class actors:

    def __init__(self):
        self.id = -1
        self.name = None
        self.birth = None
        self.movie_ids = []
        self.total_gross = 0
        self.movie_num = 0

    def add_movie(self, movie):
        self.movie_num += 1
        self.total_gross += movie.gross
        self.movie_ids.append(movie.id)

    def print(self):
        print("{}, born in {},  acted in: {}".format(self.name, self.birth, self.movie_ids))

