import socketio
from app.models import storage

storage.reload()
sio = socketio.Server()
