###################### Unit Testing ############################

import unittest
from start_app import app

class TestMovies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.app = app.test_client()

    def test_add_movies(self):
        response = self.app.post(
                "movies/add_movies?movies=Inception")
        assert response.status_code == 200
        print(response)
        #assert response.text["success"] == True

    def test_add_multiple_movies(self):
        response = self.app.post(
                "movies/add_movies?movies=365&movies=Iron Man")
        assert response.status_code == 200
        print(response)

    def test_add_movies_with_wrongname(self):
        response = self.app.post(
                "movies/add_movies?movies=Inception1")
        assert response.status_code == 400

if __name__ == '__main__':
    unittest.main()