from unittest import TestCase
import json
from flaskr import *


test_data_path = '../data/test_data.json'

class TestAPI(TestCase):

    def setUp(self):
        app = create_app({
            'DATA_PATH': test_data_path
        })
        self.client = app.test_client()

    def test_filter_actor(self):
        rv = self.client.get('/actors?name=actor1&age=10')
        self.assertTrue('actor1' in str(rv.data))
        self.assertTrue('10' in str(rv.data))

    def test_filter_movie(self):
        rv = self.client.get('/movies?name=movie')
        self.assertTrue('movie1' in str(rv.data))
        self.assertTrue('movie2' in str(rv.data))
        self.assertTrue('movie3' in str(rv.data))

    def test_create_actor(self):
        data = {'name': 'new actor'}
        header = {'content-type': 'application/json'}
        rv = self.client.post('/actors', data=json.dumps(data), headers=header)
        self.assertTrue(201 == rv.status_code)
        rv = self.client.get('/actors/new_actor')
        self.assertTrue('new actor' in str(rv.data))
        self.assertTrue('-1' in str(rv.data))

    def test_create_movie(self):
        data = {'name': 'new movie'}
        header = {'content-type': 'application/json'}
        rv = self.client.post('/movies', data=json.dumps(data), headers=header)
        self.assertTrue(201 == rv.status_code)
        rv = self.client.get('/movies/new_movie')
        self.assertTrue('new movie' in str(rv.data))
        self.assertTrue('-1' in str(rv.data))


    def test_get_actor(self):
        rv = self.client.get('/actors/actor1')
        self.assertTrue('actor1' in str(rv.data))
        self.assertTrue(201 == rv.status_code)
        rv = self.client.get('/actors/randomName')
        self.assertTrue(404 == rv.status_code)

    def test_get_movie(self):
        rv = self.client.get('/movies/movie1')
        self.assertTrue('movie1' in str(rv.data))
        self.assertTrue(201 == rv.status_code)
        rv = self.client.get('/movies/randomName')
        self.assertTrue(404 == rv.status_code)

    def test_update_actor(self):
        data = {'name': 'new actor2'}
        header = {'content-type': 'application/json'}
        self.client.post('/actors', data=json.dumps(data), headers=header)
        data = {'age': 12}
        header = {'content-type': 'application/json'}
        rv = self.client.put('/actors/new_actor2', data=json.dumps(data), headers=header)
        self.assertTrue(201 == rv.status_code)
        rv = self.client.get('/actors/new_actor2')
        self.assertTrue('new actor2' in str(rv.data))
        self.assertTrue('12' in str(rv.data))

    def test_update_movie(self):
        data = {'year': 2018}
        header = {'content-type': 'application/json'}
        rv = self.client.put('/movies/no_such_movie', data=json.dumps(data), headers=header)
        self.assertTrue(400 == rv.status_code)
        rv = self.client.put('/movies/movie2', data=json.dumps(data), headers=header)
        self.assertTrue(201 == rv.status_code)
        rv = self.client.get('/movies/movie2')
        self.assertTrue('movie2' in str(rv.data))
        self.assertTrue('2018' in str(rv.data))

    def test_delete_actor(self):
        data = {'name': 'new actor2'}
        header = {'content-type': 'application/json'}
        self.client.post('/actors', data=json.dumps(data), headers=header)
        rv = self.client.delete('/actors/new_actor2', data=json.dumps(data), headers=header)
        self.assertTrue(201 == rv.status_code)
        rv = self.client.get('/actors/new_actor2')
        self.assertTrue(404 == rv.status_code)

    def test_delete_movie(self):
        data = {'name': 'new movie2'}
        header = {'content-type': 'application/json'}
        self.client.post('/movies', data=json.dumps(data), headers=header)
        rv = self.client.delete('/movies/new_movie2', data=json.dumps(data), headers=header)
        self.assertTrue(201 == rv.status_code)
        rv = self.client.get('/movies/new_movie2')
        self.assertTrue(404 == rv.status_code)
