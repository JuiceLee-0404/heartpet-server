from socketio import Server
import socketio

sio = Server(cors_allowed_origins='*')

@sio.event
def connect(sid, environ):
    print("connect", sid)

@sio.event
def dog_action(sid, data):
    sio.emit('dog_action', data, skip_sid=sid)

if __name__ == '__main__':
    # 纯 Socket.IO，不依赖 eventlet.wsgi
    import eventlet
    eventlet.monkey_patch()
    eventlet.listen(('', 5000))
    eventlet.wsgi.server(eventlet.listen(('', 5000)), sio)
