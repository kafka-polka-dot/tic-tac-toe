from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

table = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8]
]


@app.route('/')
def index_handler():
    return render_template('index.html', cell=(1, "x", "QQQ", 4, 5, 6, 7, 8, 9))


@app.route('/turn', methods=['POST'])
def turn_handler():
    x = int(request.form['x'])
    y = int(request.form['y'])
    table[x][y] = -1
    return jsonify({'x': x, 'y': y, 'table': str(table)})

