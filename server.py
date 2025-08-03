# server.py
import asyncio
import socketio

sio = socketio.AsyncServer(cors_allowed_origins='*')

@sio.event
async def connect(sid, environ):
    print("connect", sid)

@sio.event
async def dog_action(sid, data):
    await sio.emit('dog_action', data, skip_sid=sid)

if __name__ == '__main__':
    asyncio.run(sio.start(asyncio AsyncWebsocketServer()))
