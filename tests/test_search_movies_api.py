###################### Unit Testing ############################

import unittest
from start_app import app

class TestMovies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.app = app.test_client()

    def test_search_movies(self):
        response = self.app.get(
                "movies/search_movies?movies=Iron Man")
        assert response.status_code == 200
        print(response)

    def test_search_movies_with_wrongname(self):
        response = self.app.get(
                "movies/search_movies?movies=Inception1")
        assert response.status_code == 400
        print(response)

if __name__ == '__main__':
    unittest.main()