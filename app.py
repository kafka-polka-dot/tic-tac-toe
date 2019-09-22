from copy import deepcopy

from flask import Flask, render_template, request, jsonify
import numpy

app = Flask(__name__)

X = 'X'
O = 'O'
N = 'N'

# stores the current state of the game
table = [
    [N, N, N],
    [N, N, N],
    [N, N, N]
]


@app.route('/')
def index_handler():
    flat_table = tuple(''.join([''.join(e) for e in table]))
    return render_template('index.html', cell=flat_table)


@app.route('/turn', methods=['POST'])
def turn_handler():
    x = int(request.form['x'])
    y = int(request.form['y'])
    table[y][x] = X

    # check if somebody won
    rotated = numpy.rot90(deepcopy(table))
    check_list = [
        table[0], table[1], table[2],                   # rows
        rotated[0], rotated[1], rotated[2],             # columns
        numpy.diagonal(table), numpy.diagonal(rotated)  # diagonals
    ]

    winner = None
    for l in check_list:
        if ''.join(l) == 'XXX':
            winner = X
        elif ''.join(l) == 'OOO':
            winner = O

    # FIXME: actual last turn
    result = {'last_turn': X, 'winner': winner if winner else ''}
    return jsonify(result)


@app.route('/reset', methods=['POST'])
def reset_handler():
    for row in table:
        for i in range(len(row)):
            row[i] = N
    return 'OK'
