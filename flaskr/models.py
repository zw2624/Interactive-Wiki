'''
    "Ten Little Indians": {
      "json_class": "Movie",
      "name": "Ten Little Indians",
      "wiki_page": "https://en.wikipedia.org/wiki/Ten_Little_Indians_(1989_film)",
      "box_office": 59405,
      "year": 1989,
      "actors": [
        "Donald Pleasence",
        "Brenda Vaccaro",
        "Frank Stallone",
        "Herbert Lom",
        "Warren Berlinger",
        "Moira Lister"
      ]
    }
'''
class films:

    def __init__(self):
        self.id = "no id"
        self.name = None
        self.wiki_page = None
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


'''

"Adrianne Palicki": {
    "json_class": "Actor",
    "name": "Adrianne Palicki",
    "age": 33,
    "total_gross": 375,
    "movies": [
        "Popstar",
        "Women in Trouble",
        "Legion",
        "Elektra Luxx",
        "Red Dawn",
        "G.I. Joe: Retaliation",
        "Coffee Town",
        "Dr. Cabbie",
        "John Wick"
    ]
}
'''
class actors:

    def __init__(self):
        self.id = "no id"
        self.name = None
        self.age = None
        self.total_gross = 0
        self.movie_ids = []
        self.connections = 0
        self.movie_num = 0

    def add_movie(self, movie):
        '''
        add a movie that the actor was in
        '''
        self.movie_num += 1
        if movie.box_office is not None:
            self.total_gross += movie.box_office
        self.movie_ids.append(movie.id)

