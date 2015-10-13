"""
Populate `movies.db` with favorite movies.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Movie, Genre, MPAARatings, movie_genres
import datetime

engine = create_engine('sqlite:///movies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

genres = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "Game-Show", "History", "Horror", "Music", "Musical", "Mystery", "News", "Reality-TV", "Romance", "Sci-Fi", "Sitcom", "Sport", "Talk-Show", "Thriller", "War", "Western",]
ratings = ["G", "PG", "PG-13", "R", "NC-17"]

# Add genres
for i, g in enumerate(genres):
    new_g = Genre(genre=g)
    session.add(new_g)
    session.commit()

# Add Movie Ratings
for i, r in enumerate(ratings):
    new_r = MPAARatings(rating=r)
    session.add(new_r)
    session.commit()

# genre query object
gq = session.query(Genre)

# Add Movies
m1 = Movie(
    title="The Dark Knight",
    poster_image_url="https://upload.wikimedia.org/wikipedia/en/8/8a/Dark_Knight.jpg",
    trailer_youtube_url="https://www.youtube.com/watch?v=EXeTwQWrcwY",
    storyline="When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, the caped crusader must come to terms with one of the greatest psychological tests of his ability to fight injustice.",
    mpaa_rating_id=3,
    duration=152,
    release_date=datetime.date(2008, 7, 18),
    imdb_id="tt0468569",
    rotten_id="the_dark_knight")

# Add Genres
m1.genres.append(gq.filter_by(genre='Action').one())
m1.genres.append(gq.filter_by(genre='Crime').one())
m1.genres.append(gq.filter_by(genre='Drama').one())

m2 = Movie(
    title="Watchmen",
    poster_image_url="https://upload.wikimedia.org/wikipedia/en/b/bc/Watchmen_film_poster.jpg",
    trailer_youtube_url="https://www.youtube.com/watch?v=Rm_qeIyGFxQ",
    storyline="In an alternate 1985 where former superheroes exist, the murder of a colleague sends active vigilante Rorschach into his own sprawling investigation, uncovering something that could completely change the course of history as we know it.",
    mpaa_rating_id=4,
    duration=162,
    release_date=datetime.date(2009, 3, 6),
    imdb_id="tt0409459",
    rotten_id="watchmen")

# Add Genres
m2.genres.append(gq.filter_by(genre='Action').one())
m2.genres.append(gq.filter_by(genre='Mystery').one())
m2.genres.append(gq.filter_by(genre='Sci-Fi').one())

m3 = Movie(
    title="The Shawshank Redemption",
    poster_image_url="https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
    trailer_youtube_url="https://www.youtube.com/watch?v=NmzuHjWmXOc",
    storyline="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    mpaa_rating_id=4,
    duration=142,
    release_date=datetime.date(1994, 10, 14),
    imdb_id="tt0111161",
    rotten_id="shawshank_redemption")

# Add Genres
m3.genres.append(gq.filter_by(genre='Crime').one())
m3.genres.append(gq.filter_by(genre='Drama').one())

m4 = Movie(
    title="The Prestige",
    poster_image_url="https://upload.wikimedia.org/wikipedia/en/d/d2/Prestige_poster.jpg",
    trailer_youtube_url="https://www.youtube.com/watch?v=o4gHCmTQDVI",
    storyline="Two stage magicians engage in competitive one-upmanship in an attempt to create the ultimate stage illusion.",
    mpaa_rating_id=3,
    duration=130,
    release_date=datetime.date(2006, 10, 20),
    imdb_id="tt0482571",
    rotten_id="prestige")

# Add Genres
m4.genres.append(gq.filter_by(genre='Drama').one())
m4.genres.append(gq.filter_by(genre='Mystery').one())
m4.genres.append(gq.filter_by(genre='Thriller').one())

m5 = Movie(
    title="The Illusionist",
    poster_image_url="https://upload.wikimedia.org/wikipedia/en/6/6a/The_Illusionist_Poster.jpg",
    trailer_youtube_url="https://www.youtube.com/watch?v=i0xO64icGSY",
    storyline="In turn-of-the-century Vienna, a magician uses his abilities to secure the love of a woman far above his social standing.",
    mpaa_rating_id=3,
    duration=110,
    release_date=datetime.date(2006, 9, 1),
    imdb_id="tt0443543",
    rotten_id="illusionist")

# Add Genres
m5.genres.append(gq.filter_by(genre='Drama').one())
m5.genres.append(gq.filter_by(genre='Mystery').one())
m5.genres.append(gq.filter_by(genre='Romance').one())

m6 = Movie(
    title="Sherlock Holmes: A Game of Shadows",
    poster_image_url="https://upload.wikimedia.org/wikipedia/en/5/53/Sherlock_Holmes2Poster.jpg",
    trailer_youtube_url="https://www.youtube.com/watch?v=NMP4-yyAyDc",
    storyline="Sherlock Holmes and his sidekick Dr. Watson join forces to outwit and bring down their fiercest adversary, Professor Moriarty.",
    mpaa_rating_id=3,
    duration=129,
    release_date=datetime.date(2011, 12, 16),
    imdb_id="tt1515091",
    rotten_id="sherlock_holmes_a_game_of_shadows")

# Add Genres
m6.genres.append(gq.filter_by(genre='Action').one())
m6.genres.append(gq.filter_by(genre='Adventure').one())
m6.genres.append(gq.filter_by(genre='Crime').one())

session.add_all([m1, m2, m3, m4, m5, m6])
session.commit()
