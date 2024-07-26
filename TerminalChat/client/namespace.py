import socketio
from print import PrintHandler
from handlers import SessionHandler
sio = socketio.Client()

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

    
    def on_online(self, data):
        users: list= data.get('online')
        self.session.online = users.copy()
        return self.session.online
    
    def on_available_rooms(self, data):
        rooms : list = data.get('rooms')

    def on_error(self, er):
        print(er)
        exit()



def connect(session):
    sio.register_namespace(Client(session))
    sio.connect('http://localhost:8000')
