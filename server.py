# server.py  —— 极简实时同步
from socketio import Server
from aiohttp import web

sio = Server(async_mode='aiohttp', cors_allowed_origins='*')

@sio.event
def connect(sid, environ):
    print("connect", sid)

@sio.event
def dog_action(sid, data):
    # 广播给所有客户端（除自己）
    sio.emit('dog_action', data, skip_sid=sid)

app = web.Application()
sio.attach(app)
web.run_app(app, host='0.0.0.0', port=5000)