from unittest import TestCase
from flaskr import graph
test_data_path = '../data/test_data.json'

class TestGraph(TestCase):

    def test_load(self):
        g = graph.graph()
        g.load_data(test_data_path)
        self.assertEqual(len(g.all_movies), 5)
        self.assertEqual(len(g.all_actors), 3)
        return

    def test_add_actor(self):
        g = graph.graph()
        g.load_data(test_data_path)
        actor =  {
            "json_class": "Actor",
            "name" : "new actor",
            "age": 12,
            "total_gross": 7,
            "movies": [
                "movie2"
                "new movie"
            ]

        }
        g.add_actor(actor)
        self.assertTrue(len(g.all_actors) == 4)
        self.assertTrue(len(g.all_movies) == 6)
        return

    def test_add_movie(self):
        g2 = graph.graph()
        film = {
            "json_class": "Movie",
            "name": "Live Free or Die Hard",
            "wiki_page": "https://en.wikipedia.org/wiki/Live_Free_or_Die_Hard",
            "box_office": 383,
            "year": 0,
            "actors": [
                "Bruce Willis",
                "Justin Long",
                "Timothy Olyphant",
                "Mary Elizabeth Winstead",
                "Maggie Q",
                "Kevin Smith"
            ]
        }
        g2.add_movie(film)
        self.assertTrue(len(g2.all_movies) == 1)
        return

    def test_delete_actor(self):
        g = graph.graph()
        g.load_data(test_data_path)
        g.delete_actor('actor1')
        self.assertTrue(len(g.all_actors) == 2)
        self.assertTrue(len(g.all_movies) == 5)
        return


    def test_delete_movie(self):
        g = graph.graph()
        g.load_data(test_data_path)
        g.delete_movie('movie1')
        self.assertTrue(len(g.all_actors) == 3)
        self.assertTrue(len(g.all_movies) == 4)
        return

    def test_connection(self):
        g = graph.graph()
        g.load_data(test_data_path)
        g.assign_connection()
        self.assertTrue(len(g.all_actors['actor1']['connection'].keys()) == 2)
        return

    def test_most_connection(self):
        g = graph.graph()
        g.load_data(test_data_path)
        g.assign_connection()
        ret = g.get_actor_most_connection()
        self.assertTrue(len(ret) == 3)

