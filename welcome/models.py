from operator import le
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Date, Integer, String

Base = declarative_base()

# Create your models here.
class Media(Base):
    __tablename__ = "Media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    media_type = Column(String)
    age_rating = Column(String)
    year_of_release = Column(Integer)
    language = Column(String)
    date_added = Column(Date)
    date_leaving = Column(Date)
    genre = Column(String)
    length_in_minutes = Column(Integer)
    company_id = Column(Integer)

    def __init__(self, name, media_type, age_rating, year_of_release, language, date_added, date_leaving, genre, length_in_minutes):
        self.name = name
        self.media_type = media_type
        self.age_rating = age_rating
        self.year_of_release = year_of_release
        self.language = language
        self.date_added =date_added
        self.date_leaving = date_leaving
        self.genre = genre
        self.length_in_minutes = length_in_minutes

class Actor(Base):

    __tablename__ = "actor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    country = Column(String)


class Company(Base):

    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    country = Column(String)

class Director(Base):

    __tablename__ = "director"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    country = Column(String)
