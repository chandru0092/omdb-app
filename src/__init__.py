import os
import requests
from werkzeug.exceptions import NotFound
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Namespace, fields, Resource, Api
from .models.request_models import *
from authorizations import token_required, authorizations

app = Flask(__name__)

# Expand the Swagger UI when it is loaded: list or full
app.config["SWAGGER_UI_DOC_EXPANSION"] = "list"
# Globally enable validating
app.config["RESTPLUS_VALIDATE"] = True
# Enable or disable the mask field, by default X-Fields
app.config["RESTPLUS_MASK_SWAGGER"] = False
#To connect sqlalchemy db and cofiguration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =  True

db = SQLAlchemy(app=app)

class Movies(db.Model):
    __tablename__ = 'movies'

    ID = db.Column(db.Integer, primary_key=True)
    MovieID = db.Column(db.String(), nullable=False)
    Title = db.Column(db.String(), nullable=False)
    Year = db.Column(db.Integer, nullable=False)

    def __init__(self, MovieID, Title, Year):
        self.MovieID = MovieID
        self.Title = Title
        self.Year = Year        

    def format(self):
        return {
            'ID': self.ID,
            'MovieID': self.MovieID,
            'Title': self.Title,
            'Year': self.Year
        }
    
def get_movie_namespace(app_api):

    movie_namespace = Namespace("movies", description = "Online Movie Database Application")

    ERROR_RESPONSE_MODEL = movie_namespace.model('ErrorModel', {
        'success': fields.String(required=True, description='Result of the API Ex:True or False'),
        'error': fields.String(required=True, description='API Error message')
    })
    
    @movie_namespace.route("/get_movies")
    class GetMoviesResource(Resource):
        @movie_namespace.doc(parser=GETMOVIELIST_REQUEST_MODEL, \
                description = "Get Movies from OMDB application")
        @movie_namespace.response(500, 'INTERNAL SERVER ERROR',ERROR_RESPONSE_MODEL)
        @movie_namespace.response(400, 'BAD REQUEST',ERROR_RESPONSE_MODEL)
        def get(self):
            """Get Movie List"""
            args = GETMOVIELIST_REQUEST_MODEL.parse_args()
            records = args["records"]
            pageno = args["page"]
            pagination = Movies.query.paginate(page=1, per_page=records)
            pagenos = []
            for number in pagination.iter_pages():
                pagenos.append(number)
            if pagenos[0] <= pageno <= pagenos[-1]:
                movieresults = Movies.query.order_by(Movies.Title).\
                        paginate(page=pageno, per_page=records, error_out=True)
                results = [movie.format() for movie in movieresults.items]
                return jsonify({
                    'success':True,
                    'movies':results,
                    'count':len(results),
                    'totalMovies':movieresults.total
                })
            return {
                'success':False,
                'error':f'Please enter valid page number.Pagenumber should be between 1 and {pagenos[-1]}'
                }, 400
        
    @movie_namespace.route("/search_movies")
    class SearchMovieResource(Resource):
        @movie_namespace.doc(parser=SEARCH_MOVIES_REQUEST_MODEL, \
                description = "Search Movies from OMDB application")
        @movie_namespace.response(500, 'INTERNAL SERVER ERROR',ERROR_RESPONSE_MODEL)
        @movie_namespace.response(400, 'BAD REQUEST',ERROR_RESPONSE_MODEL)
        def get(self):
            """Search Movies"""
            args = SEARCH_MOVIES_REQUEST_MODEL.parse_args()
            movies = args["movies"]
            results = []
            for movie in movies:
                movieresults= Movies.query.filter(Movies.Title==movie).all()
                if movieresults == []:
                    return {
                        'success':False,
                        'error':f'{movie} movie is not found in OMDB'
                        }, 400
                for movieres in movieresults:
                    results.append(movieres.format())
            return jsonify({
                        'success':True, 
                        'results':results,
                        'count':len(results)
                    })

    @movie_namespace.route("/add_movies")
    class AddMovieResource(Resource):
        @movie_namespace.doc(parser=SEARCH_MOVIES_REQUEST_MODEL,\
                description = "Addind Movies into OMDB application")
        @movie_namespace.response(500, 'INTERNAL SERVER ERROR',ERROR_RESPONSE_MODEL)
        @movie_namespace.response(400, 'BAD REQUEST',ERROR_RESPONSE_MODEL)
        def post(self):
            """Add Movies"""
            args = SEARCH_MOVIES_REQUEST_MODEL.parse_args()
            movies = args["movies"]
            apikey = os.getenv("apikey")
            for moviename in movies:
                response = requests.get(f"https://www.omdbapi.com/?apikey={apikey}&t={moviename}")
                output = response.json()
                if "Error" not in output:
                    Title = output["Title"]
                    Year = output["Year"]
                    MovieID = output["imdbID"]
                    movie_exists = Movies.query.filter(Movies.Title==Title).first()
                    if not movie_exists:
                        dbentry = Movies(MovieID=MovieID, Title=Title, Year=Year)
                        db.session.add(dbentry)
                        db.session.commit()
                else:
                    return {
                        'success':False,
                        'error':f'{moviename} {output["Error"]}'
                    }, 400
            movieresults = Movies.query.order_by(Movies.Title).paginate(page=1, per_page=10)
            results = [movie.format() for movie in movieresults.items]
            return jsonify({
                'success':True,
                'movies':results,
                'count':len(results),
                'totalMovies':movieresults.total
            })
        
    @movie_namespace.route("/delete_movies")
    class DeleteMovieResource(Resource):
        @movie_namespace.doc(security = 'BasicAuth',\
                parser=DELETE_MOVIES_REQUEST_MODEL, \
                description = "Delete Movies from OMDB application")
        @token_required
        @movie_namespace.response(500, 'INTERNAL SERVER ERROR',ERROR_RESPONSE_MODEL)
        @movie_namespace.response(400, 'BAD REQUEST',ERROR_RESPONSE_MODEL)
        def delete(self):
            """Delete Movies"""
            args = DELETE_MOVIES_REQUEST_MODEL.parse_args()
            movieIDs = args["movieID"]
            findmovies = Movies.query.filter(Movies.MovieID.in_(movieIDs)).all()
            results = [movie.format() for movie in findmovies]
            for movieid in movieIDs:
                movieresults= Movies.query.filter(Movies.MovieID==movieid).first()
                if movieresults is None:
                    return {
                        'success':False,
                        'error':f'{movieid} ID is not found in OMDB'
                        }, 400
                db.session.delete(movieresults)
                db.session.commit()
            totalmovies = Movies.query.order_by(Movies.Title).paginate(page=1, per_page=10)
            return jsonify({
                'success':True,
                'deletedMovies':results,
                'count':len(results),
                'totalMovies':totalmovies.total
            })
        
    @app.route("/contact")
    def contact():
        return "Please send us an email for any support"

    return movie_namespace

def create_app():

    app_api = Api(
        app=app,
        version='1.0',
        authorizations=authorizations,
        title='OMDB API',
        contact='OMDB Support',
        description='The OMDb API is a RESTful web service to obtain movie information,\
            and all content on the site are contributed and maintained by our users.',
        contact_url='/contact'
        )
    app_api.add_namespace(get_movie_namespace(app_api))

    return app
