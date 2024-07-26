from prompt_toolkit import PromptSession, patch_stdout, HTML
from prompt_toolkit.completion import WordCompleter
from namespace import connect, sio, SessionHandler
from handlers import Handlers
from prompt_toolkit.shortcuts import input_dialog, radiolist_dialog, button_dialog
import time
from print import style
from prompt_toolkit.shortcuts import ProgressBar, clear


SESSION = SessionHandler()
def intro():
    words = [
        ('register', 'register'),
        ('login', 'login')
        ]
    comp = WordCompleter(words)
    comp
    ans = radiolist_dialog(
        title='lets get you in!!',
        values= words
    ).run()
    return ans
def chat_session():
    global SESSION
    sess = PromptSession(style=style)
    while True:
        set_session()
        if SESSION.current == 'chat':
            users = SESSION.online
            if users:
                friend = radiolist_dialog(
                        title='Chat with who?',
                        values= users
                    ).run()
                SESSION.friend = friend
            if not users:
                refresh = button_dialog(
                    title = 'No users',
                    text='No users found, do you want to refresh',
                    buttons= [
                        ('Try later', False),
                        ('refresh', True)
                    ]
                ).run()
                if refresh:
                    with ProgressBar(
                        title= 'Looking for online users'
                    ) as pb:
                        for i in pb(range(80)):
                            time.sleep(.01)
                    clear()
                    continue
                else:
                    exit()
            
            clear()
            print(f'-------chatting with {SESSION.friend}------------')
            answer = sio.call('load_chat', data = {'username': SESSION.friend})
            while True:
                mess: str = sess.prompt(HTML('<me><i><b> ME </b></i>>></me> '))
                if mess == 'leave':
                    clear()
                    break
                data = {
                    'username': SESSION.friend,
                    'message': mess or ''
                }
                sio.call('chat', data)
        if SESSION.current == 'room':
            rooms = sio.call('all_rooms')
            room = 'create'
            if rooms:
                room_vals = list(zip(rooms, rooms))
                room_vals.insert(0, ('create', 'create your own'))
                room = radiolist_dialog(
                    title='join a room',
                    text='room choices',
                    values=room_vals
                ).run()
            if room == 'create':
                room = input_dialog(
                            title='create a room',
                            text = 'Name of the room?'
                        ).run()
            
            ans = sio.call('enter_room', data={'room':room}, timeout=10)
            if not ans:
                print(f'error getting in room')
                continue
            SESSION.room = room
            clear()
            print(f'-------chatting in {SESSION.room}------------')
            answer = sio.call('load_room', data = {'room': SESSION.room})
            while True:
                mess: str = sess.prompt(HTML('<me><i><b> ME </b></i></me> '), style=style)
                if mess == 'leave':
                    clear()
                    break
                data = {
                    'room': SESSION.room,
                    'message': mess or ''
                }
                sio.call('room', data=data)
            


def printer(data):
    username = data.get('username')
    message = data.get('mess')
    if username == SESSION.username:
        username = 'YOU'
    print(f'{username}: {message}')
    
    

def main():
    global SESSION
    connect(session=SESSION)
    ans = intro()
    name = input_dialog(
        title='Name',
        text='whats your username').run()
    password = input_dialog(
        title='Authentication',
        text='whats your pass',
        password=True).run()
    handlers = Handlers(sio)
    SESSION.username = name
    if ans == 'register':
        res = handlers.register(name, password)
    elif ans == 'login':
        res = handlers.login(name, password)
    print(f'{res=}')
    if not res:
        print('not logged in')
        exit(9)

def set_session():
    global SESSION
    room_or_chat = radiolist_dialog(
        title='Chat Or Room',
        text='Do you want to chat with a user or join a room',
        values=[
            ('chat', 'Chat'),
            ('room', 'Room')
        ]).run()
    SESSION.current = room_or_chat
    return SESSION



if __name__ == '__main__':
    main()
    with patch_stdout.patch_stdout() as pt:
        chat_session()
    sio.wait()
