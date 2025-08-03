# server.py  —— Render 兼容版
from socketio import Server
import eventlet
import eventlet.wsgi

sio = Server(cors_allowed_origins='*')   # 去掉 async_mode

@sio.event
def connect(sid, environ):
    print("connect", sid)

@sio.event
def dog_action(sid, data):
    sio.emit('dog_action', data, skip_sid=sid)

if __name__ == '__main__':
    app = eventlet.wsgi.server(eventlet.listen(('', 5000)), sio)
