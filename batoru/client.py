import pika
import json
import ruamel.yaml as yaml

from flask import session, request
from flask_socketio import SocketIO, emit, join_room, rooms, leave_room
from server.batoru_front import app
from battlefront.battlefront import Battlefront

with open("config/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

socketio = SocketIO(app, message_queue='redis://' + cfg['redis']['host'] + ':' + str(cfg['redis']['port']) + '/0')


@socketio.on('fight', namespace='/fight')
def start_fight(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg['rabbitmq']['host']))
    channel = connection.channel()

    channel.queue_declare(queue='fight')

    channel.basic_publish(exchange='',
                          routing_key='fight',
                          body=json.dumps(message))

    connection.close()
    print(message['player'] + ' started: ' + message['data'] + ' in room ' + message['room'])


@socketio.on('command', namespace='/fight')
def send_command(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg['rabbitmq']['host']))
    channel = connection.channel()

    channel.queue_declare(queue=message['room'])

    channel.basic_publish(exchange='',
                          routing_key=message['room'],
                          body=json.dumps(message))

    connection.close()
    print(message['player'] + ' sent: ' + message['command'] + ' on queue ' + message['room'])


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


@socketio.on('leave', namespace='/fight')
def leave(message):
    leave_room(message['room'])
    emit('fight status',
         {'data': message['player'] + ' left the battlefield.', 'player': message['player']},
         room=message['room'])

    front = Battlefront()
    front.remove_player(message['player'])
    player_list = front.get_player_list()

    emit('fight players', {'player': player_list}, room=message['room'], broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
