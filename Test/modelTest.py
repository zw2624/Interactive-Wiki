import unittest
from Model import graph, models


class modelTest(unittest.TestCase):
    def test_actor(self):
        act = models.actors()
        film = models.films()
        self.assertTrue(act.movie_num == 0)
        act.add_movie(film)
        self.assertTrue(act.movie_num == 1)
        return

    def test_film(self):
        act = models.actors()
        film = models.films()
        self.assertTrue(film.actors_id == [])
        film.add_actor(act)
        self.assertTrue(len(film.actors_id) == 1)
        return

if __name__ == '__main__':
    unittest.main()