import json
import socketio

from aiohttp import web

from excel_handler import save_or_update_socket_summary

sio = socketio.AsyncServer(cors_allowed_origins='*', aync_mode='aiohttp')
app = web.Application()

sio.attach(app)

@sio.on('message')
async def message(sid, data):
    print("Socket ID: " , sid)
    print("Received resource summary:", data)

    save_or_update_socket_summary(sid, data)
    print(f"Excel updated for socket {sid}")

if __name__ == '__main__':
    web.run_app(app, port=4000)