import json
import jsonschema
from app.utils.schemas import loginschema, register_schema
from app.models import User
from sqlalchemy.exc import IntegrityError

def login(sio, sid, payload):
    try:
        jsonschema.validate(payload, schema=loginschema)
    except jsonschema.ValidationError as e:
        print(e.message)
        return False
    data = payload['data']
    user = User.filter(username = data['username'])[0]
    if not user:
        print('user not found')
        return False
    with sio.session(sid) as session:
        session['username'] = user.username
        sio.save_session()
    sio.emit('recv', f'login {user.username}')
    return user

    ## todo: login the user using db and save to session

def register(sio, sid, payload):
    try:
        jsonschema.validate(payload, schema=register_schema)
    except jsonschema.ValidationError as e:
        print(e.message)
    data = payload['data']
    user = None
    try:
        user = User(username = data['username'], password = data['password'])
        id = user.save()
    except IntegrityError as IE:
        print('errrrrrrrrrr')
        sio.emit('err', f'{IE.detail}')
        return False

    with sio.session(sid) as session:
        session['username'] = user.username
    sio.emit(event='recv', data=f'register {user.username}')
    return user

{"action" : "login", "data" : {"username": "larry", "password":"kilo"}}