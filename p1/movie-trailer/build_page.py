"""
This script reads the movies in the database into a list and passes the list to
'fresh_tomatoes.py' to generate the html page.
"""

from fresh_tomatoes import open_movies_page

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Movie, movie_genres

engine = create_engine('sqlite:///movies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

q = session.query(Movie)
movies = q.all()

# generate html page
open_movies_page(movies)
