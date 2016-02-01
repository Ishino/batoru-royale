import pika

from simulator.battle import Battle

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='fight')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode('utf-8'))
    fight = Battle()
    fight.simulate('Ishino', body.decode('utf-8'))
    print(" [x] finished %r" % body.decode('utf-8'))

channel.basic_consume(callback,
                      queue='fight',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
