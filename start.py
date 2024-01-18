import time
import spriteCreation as SC
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)


players = {}
# Beispiel:
# 1234 : {'player': 1, 'ready': False}

countdown

@sio.event
def connect(sid, environ, auth):
    players[sid]['player']: 0
    players[sid]['ready']: False
    players[sid]['finsih']:False 
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
        players[sid]['player']: data['player']
        players[sid]['ready']: False
        # ohne daten senden nur accept
        sio.emit('accept', to = sid)
        sio.emit('lock', {"player": players[sid]['player']},skip_sid = sid) 

@sio.on('playerReady')
def playerReady(sid, data):
    players[sid]['ready']: True
    sio.emit('playerReady', {"player": players[sid]['player']})

    allReady = True
    for content in players.values():
        if not content['ready']:
            allReady = False
            return
    
    if allReady:
        startCountdown()

def startCountdown():
    if(countdown == 0):
        countdown = 3.0
    while(countdown > 0):
        sio.emit('countdown', countdown)
        countdown -= 0.1
        time.sleep(0.1)

@sio.on('finish')
def finish(sid, data):
    players[sid]['finish']: True
    sio.emit('finish', {"player": players[sid]['player']})

# Weiß nicht wie ich das ändern muss, aber brauchen wir ja eh nicht
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