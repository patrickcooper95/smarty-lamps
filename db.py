"""SQLAlchemy Instance for DB Interactions."""
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from config import base_configs

# engine = sqlalchemy.create_engine(base_configs['SQLALCHEMY_DATABASE_URI'])
engine = sqlalchemy.create_engine(base_configs["LOCAL_DATABASE_URI"])
# db = SQLAlchemy()
