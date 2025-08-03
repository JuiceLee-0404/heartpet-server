# server.py  —— Render 兼容版（Python 3.11，无 eventlet）
import asyncio
import socketio
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='aiohttp')
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print("connect", sid)

@sio.event
async def dog_action(sid, data):
    await sio.emit('dog_action', data, skip_sid=sid)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
