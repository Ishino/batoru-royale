from flask import session
from flask_socketio import SocketIO, emit
from server.batoru_front import app

socketio = SocketIO(app, message_queue='redis://localhost:6379/0')


@socketio.on('my event', namespace='/fight')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('my broadcast event', namespace='/fight')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/fight')
def test_connect():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Connected', 'count': session['receive_count']})


@socketio.on('disconnect', namespace='/fight')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True)
