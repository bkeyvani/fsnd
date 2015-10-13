# Movie Trailer Website

## Project Description
In this project you will build a Movie Trailer Website where users can see your
favorite movies and watch the trailers. You'll be writing server side code to
store a list of movie titles, box art, poster images, and movie trailer URLs.
The data will then be expressed on the web page and allow users to review the
movies and watch the trailers.  (Here's a hint: The data for the movies will be
stored using Classes!)

The data is created using `SQLAlchemy` ORM. For this project the data will be
stored in a `sqlite3` database.

**NOTE:** It is recommended and a good practice to use
[virtualenv](https://virtualenv.pypa.io/en/latest/) or
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) to
create a virtual environment for testing this and any other python projects.

## Running the code

1. Clone Repo

  ```Shell
  git clone https://github.com/bkeyvani/fsnd.git
  ```

2. Change Directory into Project

  ```Shell
  cd fsnd/p1/
  ```

3. Install Requirements

  ```Shell
  pip install requirements.txt
  ```

  This will install `SQLAlchemy`.

4. Generate Database

  ```Shell
  cd movie-trailer/
  python populate_movies.py
  ```

  This will create a `movies.db` file inside the project
`movie-trailer/` directory.

5. Generate HTML File

  ```Shell
  python build_page.py
  ```

  This will create the `fresh_tomatoes.html` file using my modified version of
[Udacity's](https://github.com/adarsh0806/ud036_StarterCode)
`fresh_tomatoes.py` script, and will lunch a browser to display the result.
