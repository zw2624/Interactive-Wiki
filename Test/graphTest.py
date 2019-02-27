import unittest
from Model import graph, models


class graphTest(unittest.TestCase):

    def test_add_actor(self):
        g = graph.graph()
        actor = models.actors()
        g.add_actor(actor)
        self.assertTrue(len(g.all_actors) == 1)
        self.assertTrue(g.actor_num == 1)
        return

    def test_add_movie(self):
        g2 = graph.graph()
        film = models.films()
        g2.add_movie(film)
        self.assertTrue(len(g2.all_movies) == 1)
        self.assertEqual(g2.movie_num, 1)
        return


    def test_add_edge(self):
        g3 = graph.graph()
        film2 = models.films()
        actor2 = models.actors()
        g3.add_actor(actor2)
        g3.add_movie(film2)
        g3.add_edge(film2.id, actor2.id, 0)
        self.assertIsNotNone(g3.actor_to_movie[actor2.id])
        self.assertIsNotNone(g3.movie_to_actor[film2.id])
        return

    def test_load(self):
        g4 = graph.graph()
        g4.load_json('test_data_actor.jl', 'test_data_movie.jl')
        self.assertEqual(len(g4.all_movies),3)
        self.assertEqual(len(g4.all_actors),5)
        return


    def test_write(self):
        g_loaded = graph.graph()
        g_loaded.load_json('test_data_actor.jl', 'test_data_movie.jl')
        g_loaded.write_to_json('test_')
        g_new = graph.graph()
        g_new.load_json('test_actors_demo.jl', 'test_movies_demo.jl')
        self.assertEqual(len(g_new.all_actors), len(g_loaded.all_actors))
        return

    def test_get_movie_gross(self):
        g5 = graph.graph()
        g5.load_json('test_data_actor.jl', 'test_data_movie.jl')
        b1 = g5.get_movie_gross('m1')
        self.assertEqual(110000000, b1)
        return

    def test_get_movie_by_actor(self):
        g6 = graph.graph()
        g6.load_json('test_data_actor.jl', 'test_data_movie.jl')
        movies = g6.get_movie_by_actor('a_1')
        self.assertTrue(len(movies) == 1)
        return

    def test_get_movie_by_year(self):
        g7 = graph.graph()
        g7.load_json('test_data_actor.jl', 'test_data_movie.jl')
        movies = g7.get_movie_by_year(2011)
        self.assertTrue(len(movies) == 1)
        return

    def test_get_actor_by_movies(self):
        g8 = graph.graph()
        g8.load_json('test_data_actor.jl', 'test_data_movie.jl')
        actors = g8.get_actor_by_movies('m2')
        self.assertTrue(len(actors) == 3)
        return

    def test_get_actor_most_gross(self):
        g9 = graph.graph()
        g9.load_json('test_data_actor.jl', 'test_data_movie.jl')
        actors = g9.get_actor_most_gross(2)
        self.assertTrue(len(actors) == 2)
        self.assertEqual(actors[0][0], 'a_4')
        return

    def test_get_actor_oldest(self):
        g10 = graph.graph()
        g10.load_json('test_data_actor.jl', 'test_data_movie.jl')
        actors = g10.get_actor_oldest(2)
        self.assertTrue(len(actors) == 2)
        self.assertEqual(actors[0][0], 'a_1')
        return

    def test_get_actor_by_year(self):
        g11 = graph.graph()
        g11.load_json('test_data_actor.jl', 'test_data_movie.jl')
        actors = g11.get_actor_by_year(1953)
        self.assertTrue(len(actors) == 1)
        return


if __name__ == '__main__':
    unittest.main()