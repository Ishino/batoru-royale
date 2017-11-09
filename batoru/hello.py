from flask import Flask
from celery import Celery
from battle import Battle

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route("/")
def hello():
    return "Eat my shorts Dave!"


@celery.task(bind=True)
def run_battle():
    Battle()


if __name__ == "__main__":
    app.run()
