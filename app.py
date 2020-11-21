from copy import deepcopy

import numpy
from flask import Flask, render_template, request, jsonify, make_response

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

state = {}

users = []

"""
TODO
* [done] determine winner, assign cookies to players
* [server] determine whose turn, return in the response
* [client] display whose turn, based on the response
    add an HTML element that would show the turn or the winner
    update its text based on responses from POST to /turn or GET to /state
* [server] allow to click only on your turn
    = don't do anything if user id from the cookie is the same as last_turn, just return the state
* [client] display when somebody won
    update the HTML element based on responses from POST to /turn or GET to /state
* [server] stop the game when somebody won = don't allow clicking
    = don't do anything if a td is clicked if there is a winner
"""


def flatten_table():
    return tuple(''.join([''.join(e) for e in table]))


@app.route('/')
def index_handler():
    resp = make_response(render_template('index.html', cell=flatten_table()))

    if not users:
        next_user_id = X
    elif len(users) == 1:
        next_user_id = O
    else:
        next_user_id = None

    cookies = request.cookies.get('user_id')
    if not cookies and next_user_id:
        resp.set_cookie('user_id', next_user_id)
        users.append(next_user_id)
    return resp


@app.route('/turn', methods=['POST'])
def turn_handler():
    user = request.cookies.get("user_id")
    # sdelat' if na user id i na est  li pobeditel
    x = int(request.form['x'])
    y = int(request.form['y'])
    table[y][x] = user

    # check if somebody won
    rotated = numpy.rot90(deepcopy(table))
    check_list = [
        table[0], table[1], table[2],  # rows
        rotated[0], rotated[1], rotated[2],  # columns
        numpy.diagonal(table), numpy.diagonal(rotated)  # diagonals
    ]

    winner = None
    for list_item in check_list:
        if ''.join(list_item) == 'XXX':
            winner = X
        elif ''.join(list_item) == 'OOO':
            winner = O

    # FIXME: actual last turn
    state.update({'x': x, 'y': y, 'last_turn': user, 'winner': winner if winner else ''})
    return jsonify(state)


@app.route('/state', methods=['GET'])
def state_handler():
    return jsonify(state)


@app.route('/reset', methods=['POST'])
def reset_handler():
    for row in table:
        for i in range(len(row)):
            row[i] = N
    global state
    state = {}
    return 'OK'
