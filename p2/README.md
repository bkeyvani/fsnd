# Tournament Results

## Project Description
In this project, you will be writing a Python module that uses the PostgreSQL
database to keep track of players and matches in a game tournament.  Project 2
was designed to teach you how to create and use databases through the use of
database schemas and how to manipulate the data inside the database. This
project has two parts:
- Defining the database schema (SQL table definitions) in `tournament.sql`, and
- Writing code that will use it to track a Swiss tournament in `tournament.py`

**NOTE:** It is recommended and a good practice to use [virtualenv][1] or
[virtualenvwrapper][2] to create a virtual environment for testing this and
any other python projects.

Running this project requires a [PostgreSQL database][3]. A vagrant
envirnoment with PostgreSQL already setup is provided in the project
description page.  Please refer to the [project description][4] for
instructions on how to get started.

## Running the code

After forking and cloning Udacity's [fullstack-nanodegree-vm repo][5], follow
these steps:

1. Change into `/vagrant/tournament` directory of the above cloned repo.

  ```Shell
  cd path/to/fullstack-nanodegree-vm/vagrant/tournament
  ```

2. In this directory you should find the following template files from
   Udacity's repository:

  - `tournament.py`
  - `tournament.sql`
  - `tournament_test.py`

3. You can safely delete the above files as the completed files are included
   in the project directory from [this repository][6].

4. Clone this repo inside the `/vagrant/tournament` directory

  ```Shell
  git clone https://github.com/bkeyvani/fsnd.git fsnd
  ```

5. At this point it is recommmended to use the vagrant virtual machine
   according to the guidelines described in the [project description
document][4] or activate a `virtualenv` if you have Postgres installed and
setup on your machine. Setting up and provisioning Postgres is outside the
scope of this project.

6. Boot up the vagrant machine and navigate into the project directory:

  **Note:** You might need  to first navigate to the `/vagrant` directory
(where the `Vagrantfile` is located) in order to run the `vagrant up` command.

  ```Shell
  vagrant up
  vagrant ssh
  cd /vagrant/tournament/fsnd/p2/
  ```

7. (Optional) Install Requirements. The Vagrant machine has an older version
   of `psycopg2` already installed.

  ```Shell
  pip install requirements.txt
  ```

  This will install `psycopg2 v2.6.1`.

8. In addition to the original files mentioned in **step 2**, I've added a
   `populate.py` file. This file populates the database with 16 players who
are matched at random. You may run this file by:

  ```Shell
  python populate.py
  ```

[1]: https://virtualenv.pypa.io/en/latest/
[2]: https://virtualenvwrapper.readthedocs.org/en/latest/
[3]: http://www.postgresql.org/
[4]: https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true
[5]: https://github.com/udacity/fullstack-nanodegree-vm
[6]: https://github.com/bkeyvani/fsnd/
