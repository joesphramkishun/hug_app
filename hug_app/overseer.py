#!/usr/bin/env python
import os
from datetime import datetime
from components import Config, DataBase, Hug, ToolKit
import click

# Create the Manager subclass
class Overseer(Config, DataBase, Hug, ToolKit):

    def __init__(self):
        super(Overseer, self).__init__()
        self._config = Config()
        self._db = DataBase()
        self._hug = Hug()
        self._toolkit = ToolKit()

    @property
    def Config(self):
        return self._config

    @property
    def DataBase(self):
        return self._db

    @property
    def Hug(self):
        return self._hug

    @property
    def ToolKit(self):
        return self._toolkit

    @click.command()
    @click.option('--port', '-p', default=8080)
    @click.argument('runserver')
    def runserver(runserver, port):
        click.echo('Running on Port: {}'.format(port))
        os.system('hug -f secretary.py -p {}'.format(port))


def main():

    Overseer.runserver()

if __name__ == '__main__':

    main()
