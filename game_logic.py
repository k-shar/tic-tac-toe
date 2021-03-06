import pygame
from tiles import *
import time

player, ai = "O", "X"


board = [".", ".", ".",
         ".", ".", ".",
         ".", ".", "."]


def generate_board(window, side):
    # -- generate tiles --
    tile_group = pygame.sprite.Group()
    key = 0
    for i in range(0, 3):
        for j in range(0, 3):
            tile_group.add(Tile([j, i], window, key, side, 0.3))
            key += 1
    return tile_group


def fill_board(tile_group):
    # fill tiles
    for i in range(len(tile_group.sprites())):
        tile_group.sprites()[i].state = board[i]


def check_if_won(board):
    winning = [[0, 3, 6],
               [1, 4, 7],
               [2, 5, 8],
               [0, 4, 8],
               [2, 4, 6],
               [0, 1, 2],
               [3, 4, 5],
               [6, 7, 8]]

    o_won = False
    x_won = False

    for line in winning:
        if board[line[0]] == board[line[1]] and \
           board[line[1]] == board[line[2]] and \
           board[line[2]] == "O":
            o_won = True

        if board[line[0]] == board[line[1]] and \
           board[line[1]] == board[line[2]] and \
           board[line[2]] == "X":
            x_won = True

    # if there is no winnner
    if not(o_won or x_won):
        # if a blank space is found draw = False
        draw = True
        for tile in board:
            if tile == ".":
                draw = False
    else:
        draw = False

    return o_won, x_won, draw


def static_evaluation(board, depth, number_of_boards_considered, list_of_boards_considered):
    o_won, x_won, draw = check_if_won(board)

    if draw:
        return 0, number_of_boards_considered, list_of_boards_considered
    if o_won:
        return (20 - depth), number_of_boards_considered, list_of_boards_considered
    if x_won:
        return (-20 + depth), number_of_boards_considered, list_of_boards_considered
    else:
        # still moves left to play
        return None


def minimax(board, depth, isMax, max_id, min_id, number_of_boards_considered, list_of_boards_considered, alpha, beta):

    # if no moves are left to check
    if static_evaluation(board, depth, number_of_boards_considered, list_of_boards_considered) != None:
        return static_evaluation(board, depth, number_of_boards_considered, list_of_boards_considered)

    list_of_boards_considered.append(board)

    # if we are simulating what a player maximising the evaluation would do
    if isMax:
        # set a worst case for this player
        currentMaxEval = -9999
        # check all legal moves
        for i in range(len(board)):
            if board[i] == ".":
                # analyse moves on a test board
                analysis_board = board.copy()
                analysis_board[i] = max_id
                number_of_boards_considered += 1
                list_of_boards_considered.append(analysis_board)

                evaluation, number_of_boards_considered, list_of_boards_considered = minimax(analysis_board, depth+1, False, max_id, min_id, number_of_boards_considered, list_of_boards_considered, alpha, beta)

                currentMaxEval = max(evaluation, currentMaxEval)

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

        return currentMaxEval, number_of_boards_considered, list_of_boards_considered

    # if we are simulating what a player minimising the evaluation would do
    if not isMax:
        # set a worst case for this player
        currentMinEval = 9999
        # check all legal moves
        for i in range(len(board)):
            if board[i] == ".":
                # analyse moves on a test board
                analysis_board = board.copy()
                analysis_board[i] = min_id
                number_of_boards_considered += 1
                list_of_boards_considered.append(analysis_board)

                evaluation, number_of_boards_considered, list_of_boards_considered = minimax(analysis_board, depth+1, True, max_id, min_id, number_of_boards_considered, list_of_boards_considered, alpha, beta)

                currentMinEval = min(evaluation, currentMinEval)

                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

        return currentMinEval, number_of_boards_considered, list_of_boards_considered


def find_computer_move(board, ai, player, number_of_boards_considered, list_of_boards_considered):
    # ai tries to minimise the evaluation
    currentEval = 9999
    tile_eval_for_display = []

    # for every empty move
    for i in range(len(board)):
        if board[i] == ".":

            # make a test move on an analysis board
            analysis_board = board.copy()
            analysis_board[i] = ai
            number_of_boards_considered += 1
            list_of_boards_considered.append(analysis_board)

            alpha = -999999
            beta = 9999999

            # see if its good, check how the human (maximising player) may respond
            evaluation, number_of_boards_considered, list_of_boards_considered = minimax(analysis_board, 0, True, player, ai, number_of_boards_considered, list_of_boards_considered, alpha, beta)
            tile_eval_for_display.append(evaluation)

            if evaluation < currentEval:
                bestMove = i
                currentEval = evaluation
        else:
            tile_eval_for_display.append("_")

    return bestMove, number_of_boards_considered, list_of_boards_considered, tile_eval_for_display


def flash_tiles(board_list, group):
    # set the state of the board
    for i in range(len(board_list)):
        group.sprites()[i].state = board_list[i]
