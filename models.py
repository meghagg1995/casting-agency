from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
import datetime
from dotenv import load_dotenv

load_dotenv()
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def drop_and_create():
    db.drop_all()
    db.create_all()
    initialize_records()

# --------------------------------------#
# INITIALIZE DATABASE RECORDS
# --------------------------------------#


def initialize_records():
    actor1 = Actor(name='Tom Cruise', age=45, gender='Male')
    actor2 = Actor(name='Dwayne Johnson', age=52, gender='Male')
    actor3 = Actor(name='Matt Damon', age=34, gender='Male')
    movie1 = Movie(title='Mission Impossible', release_year=2001)
    movie2 = Movie(title='Jumanji', release_year=2020)
    movie3 = Movie(title='Jason Bourne', release_year=2016)
    actor1.insert()
    actor2.insert()
    actor3.insert()
    movie1.insert()
    movie2.insert()
    movie3.insert()
    cast1 = movie_actors.insert().values(
        actor_id=actor1.id,
        movie_id=movie3.id
    )
    cast2 = movie_actors.insert().values(
        actor_id=actor2.id,
        movie_id=movie2.id
    )
    cast3 = movie_actors.insert().values(
        actor_id=actor3.id,
        movie_id=movie3.id
    )
    cast4 = movie_actors.insert().values(
        actor_id=actor1.id,
        movie_id=movie1.id
    )
    db.session.execute(cast1)
    db.session.execute(cast2)
    db.session.execute(cast3)
    db.session.execute(cast4)
    db.session.commit()


# --------------------------------------#
# MODELS
# --------------------------------------#


# --------------------------------------#
# ASSOCIATION TABLE, MANY-TO-MANY
# --------------------------------------#

movie_actors = db.Table('movie_actors',
                        db.Column('actor_id',
                                  db.Integer,
                                  db.ForeignKey('actor.id'),
                                  primary_key=True),
                        db.Column('movie_id',
                                  db.Integer,
                                  db.ForeignKey('movie.id'),
                                  primary_key=True))


# --------------------------------------#
# ACTOR
# id: INTEGER
# name: STRING
# age: INTEGER
# gender: STRING
# --------------------------------------#

class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'age': self.age,
          'gender': self.gender,
        }

    def short_format(self):
        return {
          'id': self.id,
          'name': self.name,
        }

    def get_actor_description(self):
        formatted_actor = self.format()
        formatted_actor['movies'] = [movie.short_format()
                                     for movie in self.movies]
        return formatted_actor


# --------------------------------------#
# MOVIE
# id: INTEGER
# title: STRING
# release_year: INTEGER
# --------------------------------------#

class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    actors = db.relationship('Actor',
                             secondary=movie_actors,
                             backref=db.backref('movies', lazy=True))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'title': self.title,
          'release_year': self.release_year
        }

    def short_format(self):
        return {
          'id': self.id,
          'title': self.title,
        }

    def get_movie_description(self):
        formatted_movie = self.format()
        formatted_movie['actors'] = [actor.short_format()
                                     for actor in self.actors]
        return formatted_movie
