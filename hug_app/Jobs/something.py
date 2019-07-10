#!/usr/bin/env python
import hug
import click
import os
from datetime import datetime


@hug.get('/')
def say_hi():
    return 'hello from something'


@hug.get('/second')
def second():
    return 'second'



@hug.extend_api('/again')
def third():
    return {second()}
