# import hug
# import click
# import os
# from datetime import datetime
#
# @hug.get('/')
# def user_root():
#     # Return Full user object as dict
#     return 'Hello from user_root!'
#
# @hug.get('/signup')
# def user_signup():
#     # Creates a new user an signs them in
#     return 'Hello from user_signup!'
#
# @hug.get('/login')
# def user_login():
#     # Logs user in and makes them current user
#     return 'Hello from user_login!'
#
# @hug.get('/logout')
# def user_logout():
#     # Logs the user out
#     return 'Hello from user_logout!'
#
# @hug.get('/reset-password')
# def user_reset_password():
#     # resets the password for a user
#     return 'Hello from user_reset_password!'

#register a user and gives login token for that new user


logging.basicConfig(level=logging.DEBUG)

ENGINE = create_engine(
    'postgresql+psycopg2://{}:{}@pgdb:5432/bigger_commerce'.format(
        os.getenv("BIGGER_COMMERCE_USER"),
        os.getenv("BIGGER_COMMERCE_PASS")),
    echo=False,
    echo_pool=False)
SESSION = sessionmaker(bind=ENGINE)


@hug.post('/register')
def test(response, body=None):

    logging.debug("inputting first user ")
    session = SESSION()

    data = body

    try:
        user = session.query(alembic.Users) \
            .filter(alembic.Users.email == str(data['email'])) \
            .one()

        return str(user.email) + ' already exists'

    except: pass

    password_hash = generate_password_hash(str(data['password']))

    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']
    phone = data['phone']

    new_user = alembic.Users(
        email=email,
        password_hash=str(password_hash),
        first_name=first_name,
        last_name=last_name,
        phone=phone
    )
    try:
        logging.debug("attempting to add user")
        session.add(new_user)
        session.commit()
    except:
        logging.error('no go')
        session.rollback()
        message = {"code": "500",
                   "message": "something broke, blame obama"}
        return message

    user = session.query(alembic.Users) \
        .filter(alembic.Users.email == str(data['email'])) \
        .one()

    set_cookie(response, user.uid)

    resp = create_user(user)

    print (resp)

    user.bc_id = resp

    session.add(user)
    session.commit()
    session.close()

    return {"code": "user created",
            "BC_response": resp}
#logs in user and gives login token
@hug.post('/login')
def get_peep(response, body=None):
    session = SESSION()

    data = body

    try:
        user = session.query(alembic.Users) \
            .filter(alembic.Users.email == str(data['email'])) \
            .one()
    except:
        return 'no user found'

    if check_password_hash(user.password_hash, str(data['password'])):
        set_cookie(response, user.uid)
        return 'logged in'
    else:
        return 'that aint it chief'
#checks to see if user is logged in by returning their name
@hug.get('/dashboard')
def dashboard(request,logged_in=None):

    test = request.cookies
    print (test)

    logged_in = get_cookie(request)
    try:
        print (logged_in.first_name)
        name = str(logged_in.first_name)
    except:
        logged_in = None
        name = None

    if logged_in:
        return 'hello {}'.format(name)
    else:
        return 'Please Login'
#logs out user and takes away login token
@hug.get('/logout')
def call_logout(response):

    response.unset_cookie('cookie')
    return True
#gets info on sepcific user when given a uid
@hug.get('/get_peep')
def get_peep(body=None):

    session = SESSION()
    data = body

    try:
        user  = session.query(alembic.Users) \
            .filter(alembic.Users.email == data['email']) \
            .one()
    except:
        return False

    print (user.bc_id)
    session.close()
    return user.bc_id

