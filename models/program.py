from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from app import db


Base = declarative_base()


class Program(Base):
   __tablename__ = "colors"
   name = Column(String, primary_key = True)
   red = Column(Integer, name="r", nullable=True)
   green = Column(Integer, name="g", nullable=True)
   blue = Column(Integer, name="b", nullable=True)
   dynamic = Column(Integer, nullable=True)
   callable_path = Column(String, nullable=True)

   def __init__(self, name, red, green, blue, dynamic, callable_path):
      self.name = name
      self.red = red
      self.green = green
      self.blue = blue
      self.dynamic = dynamic
      self.callable_path = callable_path

   def __repr__(self):
      return f"Program(name={self.name}," \
             f"red={self.red},green={self.green}, blue={self.blue}," \
             f"dynamic={self.dynamic}, callable_path={self.callable_path})"

   def json(self):
      return {
         'name': self.name,
         'red': self.red,
         'green': self.green,
         'blue': self.blue,
         'dynamic': self.dynamic,
         'callable_path': self.callable_path
      }