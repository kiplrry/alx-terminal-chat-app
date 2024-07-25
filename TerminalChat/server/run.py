from app import sio, socketio
from app.views.user_view import Root


# register views


sio.register_namespace(Root('/'))
# sio.register_namespace(Chat('/chat'))

@sio.event
def error(e):
    sio.emit('err', e)

app = socketio.WSGIApp(sio)
