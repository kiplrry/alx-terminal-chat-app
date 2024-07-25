from prompt_toolkit import PromptSession, print_formatted_text as print, HTML
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.styles import Style


style = Style.from_dict({
    'notice': 'fg:#888888',
    'chat': 'fg:#00aa00',
    'err': 'fg:#ff0000',
    'success': 'fg:#00ff00',
    'room': 'fg:#a020f0',
    'user': 'fg:#FFFF00',
    'me': 'fg:#0dbcfc'
})


class PrintHandler():

    def __init__(self) -> None:
        self.style = Style.from_dict({
    'notice': 'fg:#888888',
    'chat': 'fg:#00aa00',
    'err': 'fg:#ff0000',
    'success': 'fg:#00ff00',
    'room': 'fg:#a020f0',
    'user': 'fg:#FFFF00',
    'me': 'fg:#0dbcfc'
})

    def notice(self, message):
        print(HTML(f'<notice>{message}</notice>'), style=self.style)

    def error(self, message):
        print(HTML(f'<error>{message}</error>'), style=self.style)

    def success(self, message):
        print(HTML(f'<success>{message}</success>'), style=self.style)

    def recv(self, message,  username: str, room=None):
        username = username.upper()
        if room:
            print(HTML(f'<user>{username}</user>@<room>{room} >></room> {message}'), style=self.style)
        else:
            print(HTML(f'<user><>{username} >></user> {message}'), style=self.style)

    def send(self, message, room=None):
        if room:
            print(HTML(f'<me><i><b> ME </b></i>@<room>{room} >></room></me> {message}'), style=self.style)
        else:
            print(HTML(f'<me><i><b> ME </b></i>>></me> {message}'), style=self.style)        