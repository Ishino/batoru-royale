import pika
import json

from flask import session, request
from flask_socketio import SocketIO, emit, join_room, rooms
from server.batoru_front import app
from battlefront.battlefront import Battlefront

socketio = SocketIO(app, message_queue='redis://localhost:6379/0')


@socketio.on('fight', namespace='/fight')
def start_fight(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='fight')

    channel.basic_publish(exchange='',
                          routing_key='fight',
                          body=json.dumps(message))

    connection.close()
    print(message['player'] + ' started: ' + message['data'] + ' in room ' + message['room'])


@socketio.on('connect', namespace='/fight')
def connect():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('fight status', {'data': 'Connected', 'count': session['receive_count']})

    front = Battlefront()
    player_list = front.get_player_list()

    emit('fight players', {'player': player_list}, broadcast=True)


@socketio.on('disconnect', namespace='/fight')
def disconnect():
    print('Client disconnected', request.sid)
    front = Battlefront()
    name = front.get_player_by_room(request.sid)
    front.remove_player(name)
    player_list = front.get_player_list()

    emit('fight status',
         {'data': str(name) + ' left the battlefield.', 'player': str(name)}, broadcast=True)

    emit('fight players', {'player': player_list}, broadcast=True)


@socketio.on('join', namespace='/fight')
def join(message):
    join_room(message['room'])
    emit('fight status', {'data': 'In rooms: ' + ', '.join(rooms())})
    emit('fight status',
         {'data': message['player'] + ' joined the battlefield.', 'player': message['player']},
         room=message['room'])

    front = Battlefront()
    front.add_player(message['player'], message['player_room'])
    player_list = front.get_player_list()

    emit('fight players', {'player': player_list}, room=message['room'], broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
