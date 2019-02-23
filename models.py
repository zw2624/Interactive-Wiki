
class films:

    actors_id = []
    total_actors = 0

    def __init__(self, id, name, year, gross):
        self.id = id
        self.name = name
        self.year = year
        self.gross = gross

    def add_actor(self, actor):
        self.actors_id.append(actor.id)
        self.total_actors += 1

    def add_to_json(self, d):
        d.append({
            'id': self.id,
            'name': self.name,
            'date of birth': self.birth,
            'Total Gross': self.total_gross
        })


class actors:

    movie_ids = []
    total_gross = 0
    movie_num = 0

    def __init__(self, id, name, birth):
        self.id = id
        self.name = name
        self.birth = birth

    def add_movie(self, movie):
        self.movie_num += 1
        self.total_gross += movie.gross
        self.movie_ids.append(movie.id)

    def print(self):
        print("{}, born in {},  acted in: {}".format(self.name, self.birth, self.movie_ids))


    def add_to_json(self, d):
        d.append({
            'id': self.id,
            'name': self.name,
            'date of birth': self.birth,
            'Total Gross': self.total_gross
        })
