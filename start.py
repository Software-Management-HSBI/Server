import time
import spriteCreation as SC
import socketio
from engineio.payload import Payload

Payload.max_decode_packets = 500

sio = socketio.Server()
app = socketio.WSGIApp(sio)

players = {}
# Beispiel:
# 1234 : {'player': 1, 'ready': False}

@sio.event
def connect(sid, environ, auth):
    players[sid] = {'player': 0, 'ready': False, 'finish': False}
    print('connect ', sid)
    
@sio.event
def disconnect(sid):
    sio.emit('unlock', {'player': players[sid]['player']})
    players.pop(sid)
    print('disconnect ', sid)

@sio.on('update')
def update(sid, data):
    sio.emit('update', data, skip_sid=sid)

@sio.on('register')
def register(sid, data):
    contains = False
    for content in players.values():
        if content['player'] == data['player']:
            contains = True
            break
    if not contains:
        players[sid]['player'] = data['player']
        players[sid]['ready'] = False
        sio.emit('accept', {"player": players[sid]['player']}, to = sid)
        sio.emit('lock', {"player": players[sid]['player']}, skip_sid = sid) 

@sio.on('playerReady')
def playerReady(sid, data):
    players[sid]['ready'] = True
    sio.emit('playerReady', {"player": players[sid]['player']})

    allReady = True
    for content in players.values():
        if not content['ready']:
            allReady = False
            return
    
    if allReady:
        startCountdown()

def startCountdown():
    countdown = 3
    while(countdown > 0):
        sio.emit('countdown', {'timer': countdown})
        countdown -= 0.1
        time.sleep(0.1)

@sio.on('finish')
def finish(sid, data):
    players[sid]['finish'] = True
    sio.emit('finish', {"player": players[sid]['player']})

@sio.on('segment')
def segment(sid, data):
    if players[0] == sid:
        segments = data['segments']
        segmentLength = data['segmentLength']
        maxSpeed = data['maxSpeed']
        cars = SC.create_cars(segments, segmentLength, maxSpeed)
        sio.emit('cars', cars)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('ec2-18-159-61-52.eu-central-1.compute.amazonaws.com', 3000)), app)