#!/usr/bin/env python
import os
from datetime import datetime
import click

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Sequence, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from models import User


class Config(object):

    def __init__(self):
        self._site_version = '0.0.0.0'
        self._database_uri = (os.environ.get('DEV_DATABASE_URL') or usage_warning('DATABASE_URL not configured.'))
        self._secret_key = (os.environ.get('SECRET_KEY') or usage_warning('SECRET_KEY not configured.'))

    @property
    def site_version(self):
        return self._site_version

    @property
    def database_uri(self):
        return self._database_uri

    @property
    def secret_key(self):
        return self._secret_key

class DataBase(object, User):

    def __init__(self):
        self._engine = create_engine(os.environ.get('DEV_DATABASE_URL'), echo = True)
        self._base = declarative_base()
        self._session = sessionmaker()
        self._user = User()

    @property
    def engine(self):
        return self._engine

    @property
    def base(self):
        return self._base

    @property
    def session(self):
        self._session.configure(bind=self._engine)
        return self._session()

    @property
    def User(self):

        u = _user
        u.query = 'Hello'

        return u


    def migrate(self):
        return self._base.metadata.create_all(self._engine)

class Hug(object):

    def __init__(self):
        pass

class ToolKit(object):

    def __init__(self):
        pass
