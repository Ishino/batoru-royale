import pika
from flask import Flask


app = Flask(__name__)


@app.route("/run")
def hello():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='fight')

    channel.basic_publish(exchange='',
                          routing_key='fight',
                          body='Hello World!')

    connection.close()
    return " [x] Sent 'Hello World!'"

if __name__ == "__main__":
    app.run()
