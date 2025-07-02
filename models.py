from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Recipes(Base):
    __tablename__ = 'Recipes'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    time_cooking = Column(Integer, nullable=False)
    ingredients = Column(JSON, nullable=False)
    description = Column(String, nullable=False)
    popularity = Column(Integer, nullable=False, default=0)

