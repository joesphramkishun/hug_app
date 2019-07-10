import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Sequence, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

from overseer import Overseer

class User(Overseer().DataBase.base):

    __tablename__ = 'users'

    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    email_address = Column(String(25))
    first_name = Column(String(20))
    last_name = Column(String(20))
