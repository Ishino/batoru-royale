import pika
import json
from subprocess import Popen, PIPE

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fight')


def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    print(" [x] Received %r for player %r" % (message['data'], message['room']))

    Popen(["python3", "batoru/run.py", message['player'], message['data'], message['room']], stdout=PIPE, stderr=PIPE)

    print(" [x] finished %r" % message['data'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='fight')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
