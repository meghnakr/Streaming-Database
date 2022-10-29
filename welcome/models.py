from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

# Create your models here.
class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)