###################### Unit Testing ############################
import os
import unittest
from start_app import app
from requests.auth import HTTPBasicAuth

username = os.getenv("user")
password = os.getenv("password")

headers = {
    'accept': 'application/json',
    'authorization':HTTPBasicAuth(username=username, password=password)
}

class TestMovies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.app = app.test_client()

    def test_delete_movies(self):
        response = self.app.delete(
            "movies/delete_movies?movieID=tt1375666", auth=(username, password))
        assert response.status_code == 200

    def test_delete_movies_with_wrongid(self):
        response = self.app.delete(
            "movies/delete_movies?movieID=tt212768789")
        assert response.status_code == 400
        print(response)

if __name__ == '__main__':
    unittest.main()