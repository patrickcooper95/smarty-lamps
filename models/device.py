from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from app import db


Base = declarative_base()


class Device(Base):
   __tablename__ = "devices"
   id = db.Column(db.String, primary_key = True)
   name = db.Column(db.String, nullable=True)
   device_type = db.Column(db.String, nullable=True)
   program = db.Column(db.String, nullable=True)
   controller_gateway = db.Column(db.String, nullable=True)

   def __init__(self, id, name, device_type, program, controller_gateway):
      self.id = id
      self.name = name
      self.device_type = device_type
      self.program = program
      self.controller_gateway = controller_gateway
   #
   # def __repr__(self):
   #    return f"Program(name={self.name}," \
   #           f"red={self.red},green={self.green}, blue={self.blue}," \
   #           f"dynamic={self.dynamic}, callable_path={self.callable_path})"
   #
   # def json(self):
   #    return {
   #       'name': self.name,
   #       'red': self.red,
   #       'green': self.green,
   #       'blue': self.blue,
   #       'dynamic': self.dynamic,
   #       'callable_path': self.callable_path
   #    }