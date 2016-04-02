from flask import Flask, render_template, send_from_directory
from battlefront.player import Player

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/canvas')
def canvas():
    return render_template('canvas.html')

@app.route('/player/<name>')
def player(name):
    player = Player()
    player.load_player(name)
    return render_template('player.html', player=player)

@app.route('/<path:filename>')
def send_static(filename):
    return send_from_directory(app.static_folder, filename)
