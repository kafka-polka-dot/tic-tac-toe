from copy import deepcopy

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

# the state when the game is reset
GAME_START_TABLE = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# stores the current state of the game
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


@app.route('/reset', methods=['POST'])
def reset_handler():
    global table
    table = deepcopy(GAME_START_TABLE)
    return 'OK'
