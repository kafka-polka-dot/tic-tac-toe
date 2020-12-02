from app import flatten_table, X, N, O, determine_winner


def test_flatten_table():
    table = [
        [X, N, N],
        [N, N, X],
        [N, N, N]
    ]
    expected = (X, N, N, N, N, X, N, N, N)
    actual = flatten_table(table)
    assert expected == actual


def test_determine_winner():
    """
    tests:
    * winning combinations:
        horizontal rows - 1 case
        vertical rows - 1 case
        diagonals - 2 cases
    * non-winning combinations:
        1 case
        + a row of Ns should not return winner=N
    """
    # horizontal row
    table = [
        [X, X, X],
        [O, O, X],
        [N, X, N]
    ]
    expected = X
    actual = determine_winner(table)
    assert expected == actual
    # vertical row
    table = [
        [O, O, X],
        [O, N, X],
        [N, X, X]
    ]
    expected = X
    actual = determine_winner(table)
    assert expected == actual
    # diagonal_1
    table = [
        [O, O, X],
        [O, X, N],
        [X, N, X]
    ]
    expected = X
    actual = determine_winner(table)
    assert expected == actual
    # diagonal_2
    table = [
        [O, X, N],
        [X, O, O],
        [N, X, O]
    ]
    expected = O
    actual = determine_winner(table)
    assert expected == actual
    # non_winning_combination
    table = [
        [N, N, N],
        [O, X, N],
        [N, X, X]
    ]
    expected = None
    actual = determine_winner(table)
    assert expected == actual
