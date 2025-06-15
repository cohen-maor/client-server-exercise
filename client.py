import socketio

from resource_summary import get_system_summary


sio = socketio.Client()
sio.connect('http://localhost:4000')

print('Socket ID: ', sio.sid)
while True:
    line = input("Type 'send' to send resource utilization to the server :> ")
    if line.lower().__eq__('send'):
        summary = get_system_summary()
        sio.emit('message', summary)
        print('SUCCESS')