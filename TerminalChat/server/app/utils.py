import dataclasses
from app.models import Message, User
from socketio import Namespace

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
        
        messages = messages.order_by(Message.created_at.asc()).all() if messages else []
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


class SessionHandler:
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