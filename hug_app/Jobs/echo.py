import hug


@hug.get('/')
def hello():
    print('Hello')
