import json
from app.utils.schemas import loginschema, register_schema
from app.utils.user_utils import login, register

action_map = {
    'register': register,
    'login': login
}


def data_handler(sio, sid, data):
    payload = None
    try:
        payload = json.loads(data)
    except Exception as e:
        print(e)
        return False
    if not payload['action'] or not payload['data']:
        print(f'missing something \n {payload}')
        return False
    if payload['action'] not in action_map:
        print(f'wrong action {payload["action"]=}')
        return False
    action, data = payload['action'], payload['data']
    res = action_map[action](sio, sid, payload)
    return res
