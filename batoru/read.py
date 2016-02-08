import pika
import json

from simulator.battle import Battle

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fight')


def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    print(" [x] Received %r" % message['data'])
    fight = Battle()
    fight.simulate('Ishino', message['data'], message['room'])
    print(" [x] finished %r" % message['data'])
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='fight')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
