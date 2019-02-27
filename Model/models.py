
class films:

    def __init__(self):
        self.id = "no id"
        self.name = None
        self.release = None
        self.box_office = None
        self.actors_id = []
        self.total_actors = 0


    def add_actor(self, actor):
        '''
        add
        :param actor:
        :return:
        '''
        self.actors_id.append(actor)
        self.total_actors += 1



class actors:

    def __init__(self):
        self.id = "no id"
        self.name = None
        self.birth = None
        self.movie_ids = []
        self.total_gross = 0
        self.movie_num = 0

    def add_movie(self, movie):
        '''
        add a movie that the actor was in
        '''
        self.movie_num += 1
        if movie.box_office is not None:
            self.total_gross += movie.box_office
        self.movie_ids.append(movie.id)

