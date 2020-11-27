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
* [done] determine whose turn, return in the response
* [done] display whose turn, based on the response
    add an HTML element that would show the turn or the winner
    update its text based on responses from POST to /turn or GET to /state
* [done] do nothing if the clicked cell is not empty
* [done] allow to click only on your turn
    = don't do anything if user id from the cookie is the same as last_turn, just return the state
* [done] display when somebody won
    update the HTML element based on responses from POST to /turn or GET to /state
* [done] stop the game when somebody won = don't allow clicking
    = don't do anything if a td is clicked if there is a winner
* [testing] unit tests and CI
* [bug] race condition during state change:
    * X clicks a cell -> x, y, last_turn are updated with X's turn
    * X does a /state call
    * O clicks a cell during their turn -> x, y, last_turn are updated with O's turn
    * before the next /state call, X clicks a cell, even though it's not their turn according to what client shows,
      but the server processes it, because O has made their turn
             -> x, y, last_turn are updated with X's turn
    * X's /turn POST returns x, y and last_turn of their turn,
      but X's browser has never received the data about O's turn
* [bug] both browsers have a cookie with the same user_id
* [client] draw empty fields instead of N
* [client] show which player I am
* [server] determine (randomly?) who starts the game
* [client] make it look nicer
"""


def flatten_table():
    return tuple(''.join([''.join(e) for e in table]))


@app.route('/')
# defines a route to call a Python function from web-browser to render a table
def index_handler():
    resp = make_response(render_template('index.html', cell=flatten_table()))
    # game starts with X, than 0 for the next user
    next_user_id = None
    if not users:
        next_user_id = X
    elif len(users) == 1:
        next_user_id = O

    if len(users) > 1:
        can_accept_new_users = False
    else:
        can_accept_new_users = True

    # check if the requesting browser knows which player it is
    cookie = request.cookies.get('user_id')
    # 'not cookie' means that it's a first request from that browser => should send it the user id
    is_request_coming_from_new_browser = cookie is None

    if is_request_coming_from_new_browser and can_accept_new_users:  # request where browser didn't send cookies
        resp.set_cookie('user_id', next_user_id)
        users.append(next_user_id)
    return resp


@app.route('/turn', methods=['POST'])
def turn_handler():
    """
    this function processes the turn

    """
    #request contains coordinates of the clicked cell
    user = request.cookies.get("user_id")
    x = int(request.form['x'])
    y = int(request.form['y'])
    if table[y][x] == 'N' and state.get('last_turn') != user and not state.get('winner'):
        table[y][x] = user
        # check if somebody won
        # FIXME: rotated = zip(*original[::-1])
        # diagonals:
        # [m[i][i] for i in xrange(0, len(m))]
        # [m[i][~i] for i in xrange(0, len(m))]
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

        state.update(
            {'x': x, 'y': y, 'last_turn': user, 'next_turn': O if user == X else X, 'winner': winner if winner else ''})
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
