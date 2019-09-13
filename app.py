from flask import Flask, render_template, request, jsonify
app = Flask(__name__)


@app.route('/')
def index_handler():
    return render_template('index.html', cell=(1, "x", "QQQ", 4, 5, 6, 7, 8, 9))


@app.route('/turn', methods=['POST'])
def turn_handler():
    x = request.form['x']
    y = request.form['y']
    return jsonify({'x': x, 'y': y})
