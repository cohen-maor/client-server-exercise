import socketio

sio = socketio.Client()

@sio.event
def message(data):
    print('I received a message!')
    print(data)

sio.connect('http://localhost:4000')
print('my sid is', sio.sid)
while True:
    line = input(":> ")
    if len(line) > 0:
        sio.emit('message', {'text': line})