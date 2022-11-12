from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from app import db


Base = declarative_base()


class Device(Base):
   __tablename__ = "devices"
   id = db.Column(db.String, primary_key=True)
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

   def __repre__(self):
      return f"Device(id={self.id}," \
             f"name={self.name}, type={self.device_type}, program={self.program}, host={self.controller_gateway}"

   def json(self):
      return {
         'id': self.id,
         'name': self.name,
         'device_type': self.device_type,
         'program': self.program,
         'host': self.controller_gateway
      }