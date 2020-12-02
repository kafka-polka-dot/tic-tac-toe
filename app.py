import uuid
from copy import deepcopy

import numpy
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__)

X = 'X'
O = 'O'
N = ' '

# stores the current state of the game
table = [
    [N, N, N],
    [N, N, N],
    [N, N, N]
]

# init state with last turn to prevent O from making 1st turn
state = {'last_turn': O}

users = []

session_id = str(uuid.uuid4())

"""
TODO
* [client] show which player I am
* [bug] race condition during state change:
    * X clicks a cell -> x, y, last_turn are updated with X's turn
    * X does a /state call
    * O clicks a cell during their turn -> x, y, last_turn are updated with O's turn
    * before the next /state call, X clicks a cell, even though it's not their turn according to what client shows,
      but the server processes it, because O has made their turn
             -> x, y, last_turn are updated with X's turn
    * X's /turn POST returns x, y and last_turn of their turn,
      but X's browser has never received the data about O's turn
DONE
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
* [done] unit tests and CI
* [done] draw empty fields instead of N
* [done] determine (randomly?) who starts the game --- x starts the game
* [done] render template in index_handler with next_turn
* [done] make it look nicer
* [done] on the O's browser, click 'reset', then click a cell
* [done] both browsers have a cookie with the same user_id
"""


def flatten_table(table_: list) -> tuple:
    return tuple(''.join([''.join(e) for e in table_]))


@app.route('/')
# defines a route to call a Python function from web-browser to render a table
def index_handler():
    resp = make_response(render_template('index.html', cell=flatten_table(table), turn=state.get('next_turn', X)))
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
    user_id_cookie = request.cookies.get('user_id')
    # needed to check if the browser has the cookie of the current session
    session_id_cookie = request.cookies.get('session_id')
    # 'not cookie' means that it's a first request from that browser => should send it the user id
    is_request_coming_from_new_browser = user_id_cookie is None or session_id_cookie != session_id

    if is_request_coming_from_new_browser and can_accept_new_users:
        resp.set_cookie('user_id', next_user_id)
        resp.set_cookie('session_id', session_id)
        users.append(next_user_id)
    return resp


@app.route('/turn', methods=['POST'])
def turn_handler():
    """
    this function processes the turn

    """
    # request contains coordinates of the clicked cell
    user = request.cookies.get("user_id")
    x = int(request.form['x'])
    y = int(request.form['y'])
    if table[y][x] == N and state.get('last_turn') != user and not state.get('winner'):
        table[y][x] = user
        winner = determine_winner(table)
        state.update(
            {'x': x, 'y': y, 'last_turn': user, 'next_turn': O if user == X else X, 'winner': winner if winner else ''})
    return jsonify(state)


def determine_winner(table_: list) -> str:
    """
    check if somebody won
    :return: X or O or None
    """
    # FIXME: rotated = zip(*original[::-1])
    # diagonals:
    # [m[i][i] for i in xrange(0, len(m))]
    # [m[i][~i] for i in xrange(0, len(m))]
    rotated = numpy.rot90(deepcopy(table_))
    check_list = [
        table_[0], table_[1], table_[2],  # rows
        rotated[0], rotated[1], rotated[2],  # columns
        numpy.diagonal(table_), numpy.diagonal(rotated)  # diagonals
    ]
    winner = None
    for list_item in check_list:
        if ''.join(list_item) == 'XXX':
            winner = X
        elif ''.join(list_item) == 'OOO':
            winner = O
    return winner


@app.route('/state', methods=['GET'])
def state_handler():
    return jsonify(state)


@app.route('/reset', methods=['POST'])
def reset_handler():
    for row in table:
        for i in range(len(row)):
            row[i] = N
    global state
    # init state with last turn to prevent O from making 1st turn
    state = {'last_turn': O}
    return 'OK'
