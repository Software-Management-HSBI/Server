import spriteCreation as SC
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

players = []

@sio.event
def connect(sid, environ, auth):
    players.append(sid)
    print('connect ', sid)
    
@sio.event
def disconnect(sid):
    players.remove(sid)
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
    if players[0] == sid:
        segments = data['segments']
        segmentLength = data['segmentLength']
        maxSpeed = data['maxSpeed']
        cars = SC.create_cars(segments, segmentLength, maxSpeed)
        sio.emit('cars', cars)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('ec2-18-159-61-52.eu-central-1.compute.amazonaws.com', 3000)), app)