"""
import : imports the whole library.
from import imports a specific member or members of the library.
"""

from src import create_app
from src.helpers.get_movies import get_movie_list
from dotenv import load_dotenv
load_dotenv()
app = create_app()

if __name__ == '__main__':
    get_movie_list()
    app.run(debug=True, host ='0.0.0.0', port=5002)
    