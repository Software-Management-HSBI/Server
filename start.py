import spriteCreation as SC
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

player1 = None
players = []

@sio.event
def connect(sid, environ, auth):
    players.append(sid)
    if player1 is None:
        player1 = sid
    print('connect ', sid)
    
@sio.event
def disconnect(sid):
    players.remove(sid)
    if player1 == sid:
        player1 = players[0] if players else None
    print('disconnect ', sid)

@sio.on('update')
def update(sid, data):
    for session_id, socket in sio.sockets.items():
        if session_id != sid:
            socket.emit('update', data)

@sio.on('start')
def start(sid, data):
    road = SC.get_random_road()
    sio.emit('road', road)

@sio.on('segment')
def segment(sid, data):
    if player1 == sid:
        segments = data['segments']
        segmentLength = data['segmentLength']
        maxSpeed = data['maxSpeed']
        cars = SC.create_cars(segments, segmentLength, maxSpeed)
        sio.emit('cars', cars)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('localhost', 3000)), app)