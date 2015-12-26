# Tournament Results

## Project Description
In this project, you will be writing a Python module that uses the PostgreSQL
database to keep track of players and matches in a game tournament.  Project 2
was designed to teach you how to create and use databases through the use of
database schemas and how to manipulate the data inside the database. This
project has two parts:
- Defining the database schema (SQL table definitions) in `tournament.sql`, &
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

### Setting up the Database
1. In order to create the database, import the `tournament.sql` file located
   inside the `touranament-planner` directory.

  ```Shell
  cd tournament-planner
  psql -f tournament.sql

  ```

  **Note:** The above command will drop any existing `tournament` database,
creates the database again with the following tables and views.

  ```
  matches           # table
  players           # table
  players_id_seq    # sequence
  v_nummatches      # view
  v_numwins         # view
  v_playerstandings # view
  ```

2. **Alternatively** you can create the tournament database by importing the
   `tournament.sql` file using Postgres interactive shell.

  ```
  psql

  # Inside Postgres interactive shell
  vagrant=> \i tournament.sql

  ... # Postgres imports the file, creates the DB & its associated relations

  # quit psql to get back to OS shell
  vagrant=> \q
  ```

  **Note:** Running the `psql` command should put you inside Postgres
interactive shell logged in as the `vagrant` user.

### Testing the database
1. Run the `tournament_test.py` file to test the specified functionality of
   the DB for this project.

  ```Shell
  python tournament_test.py
  ```

  This should run the initial tests for this project and you should see all 8
tests passing with a success message.

### Extra Credit activities
1. In addition to the original files mentioned in **step 2** of [Running the
   code section][7], I've added a
   `populate.py` file. This file populates the database with 64 players who
are matched using the Swiss Pairing method. You may run this file by:

  ```Shell
  python populate.py
  ```

2. I have also tackled the following extra credit tasks for this project so
   far.

  - Prevent rematches between players

  I will submit the repo for review in the future upon successfully
adding/solving more extra credit tasks.

[1]: https://virtualenv.pypa.io/en/latest/
[2]: https://virtualenvwrapper.readthedocs.org/en/latest/
[3]: http://www.postgresql.org/
[4]: https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true
[5]: https://github.com/udacity/fullstack-nanodegree-vm
[6]: https://github.com/bkeyvani/fsnd/
[7]: #running-the-code
