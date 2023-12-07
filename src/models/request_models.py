from flask_restx import reqparse

GETMOVIELIST_REQUEST_MODEL = reqparse.RequestParser()
GETMOVIELIST_REQUEST_MODEL.add_argument("records", type=int, required=False, help="Set the records howmany you want to show", default=10)
GETMOVIELIST_REQUEST_MODEL.add_argument("page", type=int, required=False, help="Enter Page No", default=1)

SEARCH_MOVIES_REQUEST_MODEL = reqparse.RequestParser()
SEARCH_MOVIES_REQUEST_MODEL.add_argument("movies", action="append", type=str, required=True, help="Enter movie names")

DELETE_MOVIES_REQUEST_MODEL = reqparse.RequestParser()
DELETE_MOVIES_REQUEST_MODEL.add_argument("movieID", action="append", type=str, required=True, help="Enter movie id")