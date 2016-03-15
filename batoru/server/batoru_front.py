from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/canvas')
def canvas():
    return render_template('canvas.html')


@app.route('/<path:filename>')
def send_static(filename):
    return send_from_directory(app.static_folder, filename)
