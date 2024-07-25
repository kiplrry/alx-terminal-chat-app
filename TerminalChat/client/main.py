import socketio
from print import PrintHandler

sio = socketio.Client()
ONLINE = []


class SessionHandler:
    def __init__(self) -> None:
        self.current = None
        self.friend = None
        self.room = None
        self.username = None

    def online(self):
            users_online = online_users()
            if not users_online:
                return False
            users_online.remove(self.username)
            users = list(zip(users_online, users_online)) if users_online else []
            return users
    


class Client(socketio.ClientNamespace):
    def __init__(self, session: SessionHandler, namespace=None):
        self.print = PrintHandler()
        self.current = None
        self.friend = None
        self.room = None
        self.session = session
        super().__init__(namespace)

    def on_connect(self):
        self.print.notice('-------------connected')

    def on_disconnect(self):
        self.print.notice('-------------disconnected')
        exit()
    
    # def on_message(self, data):
    #     username = data.get('username')
    #     message = data.get('mess')
    #     self.print.chat(message, username)
        
    def on_load_chat(self, chats):
        if not chats:
            return
        for chat in chats:
            data = {}
            data['username'] = chat[0]
            data['mess'] = chat[1]
            self.on_chat(data)

    
    def on_notice(self, data):
        self.print.notice(data)
    
    def on_chat(self, data):
        username = data.get('username')
        message = data.get('mess')
        if self.session.current == 'chat':
            if username == self.session.friend:
                self.print.recv(message, username)
            if username == self.session.username:
                self.print.send(message)
        else:
            self.print.notice(f'{username} sent a message')
    
    def on_room(self, data):
        username = data.get('username')
        message = data.get('mess')
        room = data.get('room')

        if self.session.current == 'room':
            if username == self.session.username:
                self.print.send(message, room=room)
            else:
                self.print.recv(message, username, room=room)
        else:
            self.print.notice(f'{username}@{room} sent a message ')

    def on_load_room(self, chats):
        if not chats:
            return
        for chat in chats:
            data = {}
            data['username'] = chat[0]
            data['mess'] = chat[1]
            data['room'] = self.session.room
            self.on_room(data)
    
    def on_leave_room(self):
        pass

    def on_enter_room(self):
        pass
    
    def on_online(self, data):
        users: list= data.get('online')
        global ONLINE
        ONLINE = users
        return users



def connect(session):
    sio.register_namespace(Client(session))
    sio.connect('http://localhost:8000')

class Handlers:
    def __init__(self, sio: socketio.Client) -> None:
        self.sio = sio
        self.is_logged_in = False
        self.room_or_chat = None

    def login(self, name, password):
        data = {'name': name, 'password': password}
        self.sio.emit('login', data=data, callback=self.logged_in)

    def register(self, name, password):
        data = {'name': name, 'password': password}
        self.sio.emit('register', data=data, callback=self.logged_in)

    def logged_in(self, data):
        if data == True:
            self.is_logged_in = True
        else:
            self.is_logged_in = False

    def chat(self, name):
        self.sio.emit('chat', data={'username': name})

def online_users():
    return ONLINE.copy()



class MessageHandler:
    def parse(self, message: str):
        if not message:
            return False
        split = message.split()
        first = split[0]
    
    def firstwordparse(self, word):
        if word == 'exit':
            exit()
        if word == 'leave':
            pass
        if word == '':
            pass

def load_chat(friendname):
    chats = sio.call('load_chat', data = {'username': friendname})
    print(f'{chats=}')
    print(f'-------chatting with {friendname}------------')
    if not chats:
        return
    for chat in chats:
        data = {}
        data[chat[0]] = chat[1]
        sio._trigger_event('chat', None, data)


    