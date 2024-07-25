# from app import sio , socketio
from socketio import Namespace
from app.utils.user_utils import login
from app.models import User, Message, Room
from time import sleep
import dataclasses
# from pprint import pprint as print


@dataclasses.dataclass
class MessageHandler:
    def new_message(self, from_user: User, content: str = '',to_user: User =None, room=None) -> Message:
        mess = Message()
        mess.from_id = from_user.id
        if to_user:
            mess.to_id = to_user.id
        if room:
            mess.room_id = room.id
        mess.content = content or ' '
        return mess
    
    def load_messages(self, user1: User = None, user2: User = None, room=None) -> list[Message]:
        messages = None
        if room:
            messages = Message.query().filter(Message.room_id == room.id)
        elif user1 and user2:
            messages = Message.query().filter(Message.to_id.in_([user1.id, user2.id]),
                                  Message.from_id.in_([user1.id, user2.id]))
        
        messages = messages.order_by(Message.created_at.desc()).all() if messages else []
        return messages

    def parse_chat_messages(self, messages: list[Message]):
        if not messages:
            return []
        parsed = []
        try:
            for message in messages:
                username = message.from_user.username
                content = message.content
                parsed.append([username, content])
            return parsed
        except Exception as e:
            print('error occored parsing messages\n', e)



class Session:
    def __init__(self, sio: Namespace) -> None:
        self.sio  = sio

    def add_user(self, sid, user):
        with self.sio.session(sid) as ss:
            ss['user'] = user
        user.update(sid=sid)
        return user

    def rem_user(self, sid):
        with self.sio.session(sid) as ss:
            user = ss.get('user')
            if user:
                user.sid = None
                user.save()

    def add_friend(self, sid, user):
        with self.sio.session(sid) as ss:
            ss['friend'] = user

    def get(self, sid, key):

        return self.sio.get_session(sid).get(key)
    

class Root(Namespace):
    online = {}

    def __init__(self, namespace=None):
        self.session_h = Session(self)
        self.message_h = MessageHandler()
        self._rooms = {}
        super().__init__(namespace)

    def on_connect(self, sid, environ):
        print(f'{sid} connected')

    def on_disconnect(self, sid):
        user = self.session_h.get(sid, 'user')
        try:
            self.online.pop(user.username)
            self.emit('online', data={'online': list(self.online.keys())})
        except:
            pass
        print(f'{sid} disconnected')


    def on_login(self, sid, data: dict):
        name = data.get('name')
        password = data.get('password')
        users = User.filter(username = name)
        if not users:
            return False
        user = users[0]
        self.online[user.username] = sid
        self.session_h.add_user(sid, user)
        print(f'login {sid}>> {user}')
        self.emit('online', data={'online': list(self.online.keys())})
        return True


    def on_logout(self, sid, data):
        self.session_h.rem_user(sid)

    def on_register(self, sid, data):
        print(f'register {sid}>> {data}')
        name = data.get('name')
        password = data.get('password')
        try:
            user = User(username=name, password= password)
            user.save()
            if not user:
                return False
            self.session_h.add_user(sid, user)
            self.online[user.username] = sid
            # online(self)
            self.emit('online', data={'online': list(self.online.keys())})
            return True
        except Exception as e:
            print(e)
            return False

    
    def on_chat(self, sid, data: dict):
        username = data.get('username')
        friend = get_user(username)
        if not friend:
            self.call('notice', 'invalid user', sid=sid)
            print(f'user not found')
            return
        if friend.username not in self.online :
            self.call('notice', 's_friend not online', sid=sid)
            print(f'{friend} unavailable')
            return
        self.session_h.add_friend(sid, friend)
        user: User = self.session_h.get(sid, 'user')
        friend: User= self.session_h.get(sid, 'friend')
        if not user:
            self.call('notice', data={'mess': 'not logged in'}, sid=sid)
            return False
        mess = data.get('message')
        message = self.message_h.new_message(from_user=user, to_user=friend,
                                   content=mess)
        message.save()
        mess = message.content
        data = {'username': user.username, 'mess': mess}
        # message = self.message_h.new_message(from_user=user, mess)
        # self.emit('message', data, skip_sid=sid)
        self.call('chat', data, sid=self.online.get(friend.username))
        
        
    def on_enter_room(self, sid, data):
        user: User = self.session_h.get(sid, 'user')
        if not user:
            self.call('notice', data={'mess': 'not logged in'}, sid=sid)
            return False
        roomname = data.get('room')
        rooms = Room.filter(name=roomname)
        room = get_room(roomname)
        room.save()
        room.users.append(user)
        self.enter_room(sid=sid, room=roomname)
        self.emit('notice', data=f'{user.username} joined the room', room=roomname)
        return True
        
    def on_room(self, sid, data):
        user = self.user_check(sid)
        if not user:
            return
        roomname = data.get('room')
        if roomname not in self.rooms(sid):
            return {'mess': 'invalid room'}
        room = get_room(roomname)
        room.save()
        username = user.username
        mess = data.get('message')
        message = self.message_h.new_message(from_user=user, room=room,
                                   content=mess)
        message.save()
        mess = message.content
        data = {'username': user.username, 'mess': mess, 'room': room.name}
        print(f'sent to room {data}')
        self.emit('room', data = data, room=roomname, skip_sid=sid)


        
    def user_check(self, sid):
        user: User = self.session_h.get(sid, 'user')
        if not user:
            self.call('notice', data={'mess': 'not logged in'}, sid=sid)
            return False
        return user
        
    def on_leave_room(self, sid, data):
        pass

    def on_load_chat(self, sid, data):
        user: User = self.session_h.get(sid, 'user')
        if not user:
            self.call('notice', data={'mess': 'not logged in'}, sid=sid)
            print({'mess': 'not loged in'})
            return False
        friendname = data.get('username')
        print(f'got {data=}')
        if not friendname:
            self.call('notice', data={'mess': 'no friend'}, sid=sid)
            return False
        friend: User= get_user(friendname)
        messages = self.message_h.load_messages(user1=user, user2=friend)
        print(f'{messages=}')
        messages = self.message_h.parse_chat_messages(messages)
        print(f'parsed{messages=}')
        self.call('load_chat', messages, sid=sid)

    def on_load_room(self, sid, data):
        user = self.user_check(sid)
        if not user:
            return False
        roomname = data.get('room')
        if not roomname:
            self.call('notice', data={'mess': 'no room'}, sid=sid)
            return False
        rooms = Room.filter(name=roomname)
        if not rooms:
            return False
        room = rooms[0]
        messages = self.message_h.load_messages(room=room)
        print(f'{messages=}')
        messages = self.message_h.parse_chat_messages(messages)
        print(f'parsed{messages=}')
        self.call('load_room', messages, sid=sid)


def user_online(username):
    users: list[User] = User.query().filter(User.sid.isnot(None)).all()
    if users:
        usernames = [un.username for un in users]
        return username in usernames
    return False

def get_user(username) -> User:
    users = User.filter(username=username)
    if not users:
        return False
    return users[0]

def users_in_room(sio: Root, roomname):
    rooms = Room.filter(name=roomname)
    if not rooms:
        return False

    in_room = []
    for user, sid in sio.online.items():
        sio.rooms(sid=sid)
        if roomname in rooms:
            in_room.append(user)
         
    
def user_in_room(sio: Root, roomname):
    rooms = Room.filter(name=roomname)
    if not rooms:
        return False
    # room: Room= rooms[0]
    # all_users = room.users
    # online_users = list(set(sio.online).intersection(set(all_users)))

def get_room(roomname) -> Room:
    rooms = Room.filter(name=roomname)
    if rooms:
        room: Room= rooms[0]
    else:
        room = Room(name=roomname)
    return room