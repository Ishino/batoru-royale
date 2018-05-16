import pika
import json
import ruamel.yaml as yaml

from subprocess import Popen, PIPE

with open("config/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg['rabbitmq']['host'],
                                                               port=cfg['rabbitmq']['port'],
                                                               connection_attempts=cfg['rabbitmq']['connection_attempts'],
                                                               retry_delay=cfg['rabbitmq']['retry_delay']))
channel = connection.channel()
print(' [*] Connected to Rabbit MQ')

channel.queue_declare(queue='fight')


def callback(ch, method, properties, body):
    message = json.loads(body.decode('utf-8'))
    print(" [x] Received %r for player %r" % (message['data'], message['room']))

    Popen(["python", "run.py", message['player'], message['data'], message['room']], stdout=PIPE, stderr=PIPE)

    print(" [x] finished %r" % message['data'])
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='fight')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
