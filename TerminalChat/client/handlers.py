import socketio


class Handlers:
    def __init__(self, sio: socketio.Client) -> None:
        self.sio = sio
        self.is_logged_in = False
        self.room_or_chat = None

    def login(self, name, password):
        data = {'name': name, 'password': password}
        res = self.sio.call('login', data=data)
        if res:
            self.is_logged_in = True
        return res

    def register(self, name, password):
        data = {'name': name, 'password': password}
        res = self.sio.call('register', data=data)
        if res:
            self.is_logged_in = True
        return res

    def chat(self, name):
        self.sio.emit('chat', data={'username': name})
        

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

class SessionHandler:
    def __init__(self) -> None:
        self.current = None
        self.friend = None
        self.room = None
        self.username = None
        self._online_users: list = []

    @property
    def online(self):
        if not self._online_users:
            return []
        try:
            users = self._online_users.copy()
            users.remove(self.username)
        except ValueError:
            pass
        users = list(zip(users, users))
        return users
    
    @online.setter
    def online(self, users):
        if not isinstance(users, list):
            raise ValueError('Online users should be a list')
        if not all(isinstance(user, str) for user in users):
            raise ValueError('All online users should be strings')
        self._online_users = users
