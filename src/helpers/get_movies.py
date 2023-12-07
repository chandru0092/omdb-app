import os
import requests
from src import db, Movies

db.drop_all()
db.create_all()

def get_movie_list():
    apikey = os.getenv("apikey")
    for i in range(1, 11):
        response = requests.get(f"https://www.omdbapi.com/?apikey={apikey}&s=*bat&page={i}")
        output = response.json()
        for movie in output["Search"]:
            Title = movie["Title"]
            Year = movie["Year"]
            MovieID = movie["imdbID"]
            dbentry = Movies(MovieID=MovieID, Title=Title, Year=Year)
            db.session.add(dbentry)
            db.session.commit()

def add_movies(movies):
    apikey = os.getenv("apikey")
    for movie in movies:
        response = requests.get(f"https://www.omdbapi.com/?apikey={apikey}&s={movie}")
        output = response.json()
        import pdb
        pdb.set_trace()
        for movie in output["Search"]:
            Title = movie["Title"]
            Year = movie["Year"]
            MovieID = movie["imdbID"]
            dbentry = Movies(MovieID=MovieID, Title=Title, Year=Year)
            movie_exists = db.session.query.filter(Title==Title).first()
            if not movie_exists:
                db.session.addall(dbentry)
                db.session.commit()