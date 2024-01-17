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
    sio.emit('update', data, skip_sid=sid)

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