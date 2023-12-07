###################### Unit Testing ############################

import unittest
from start_app import app

class TestMovies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.app = app.test_client()

    def test_get_movies(self):
        response = self.app.get(
                "movies/get_movies")
        assert response.status_code == 200
        print(response)

    def test_get_movies_page0(self):
        response = self.app.get(
                "movies/get_movies?page=0")
        assert response.status_code == 400
        print(response)

    def test_get_movies_page1(self):
        response = self.app.get(
                "movies/get_movies?page=1")
        assert response.status_code == 200
        print(response)

    def test_get_movies_page11(self):
        response = self.app.get(
                "movies/get_movies?page=11")
        assert response.status_code == 400
        print(response)

if __name__ == '__main__':
    unittest.main()