import random

board = ["0", "1", "2",
         "3", "4", "5",
         "6", "7", "8"]


# player will maximise,
# ai will minimise
player, ai = "O", "X"


def print_board(board):
    for i in range(9):
        print(board[i], end="   ")
        if (i+1) % 3 == 0:
            print("\n")


def static_evaluation(board, depth, boards_considered, list_of_boards_considered):
    o_won, x_won, draw = check_if_won(board)
    if draw:
        return 0, boards_considered, list_of_boards_considered
    if o_won:
        return (20 - depth), boards_considered, list_of_boards_considered
    if x_won:
        return (-20 + depth), boards_considered, list_of_boards_considered
    else:
        return None


def minimax(board, depth, isMax, max_id, min_id, boards_considered, list_of_boards_considered):
    if static_evaluation(board, depth, boards_considered, list_of_boards_considered) != None:
        return static_evaluation(board, depth, boards_considered, list_of_boards_considered)

    if isMax:
        # set a worst case
        currentMaxEval = -9999
        for i in range(len(board)):
            if not(board[i] == "X" or board[i] == "O"):
                analysis_board = board.copy()
                analysis_board[i] = max_id
                boards_considered += 1
                list_of_boards_considered.append(analysis_board)
                
                evaluation, boards_considered, list_of_boards_considered = minimax(analysis_board, depth+1, False, max_id, min_id, boards_considered, list_of_boards_considered)

                if evaluation > currentMaxEval:
                    currentMaxEval = evaluation
            
        return currentMaxEval, boards_considered, list_of_boards_considered

    if not isMax:
        # set a worst case
        currentMinEval = 9999
        for i in range(len(board)):
            if not(board[i] == "X" or board[i] == "O"):
                analysis_board = board.copy()
                analysis_board[i] = min_id
                boards_considered += 1
                list_of_boards_considered.append(analysis_board)
                
                evaluation, boards_considered, list_of_boards_considered = minimax(analysis_board, depth+1, True, max_id, min_id, boards_considered, list_of_boards_considered)

                if evaluation < currentMinEval:
                    currentMinEval = evaluation

        return currentMinEval, boards_considered, list_of_boards_considered


def find_computer_move(board, ai, player, boards_considered, list_of_boards_considered):
    currentEval = 9999

    for i in range(len(board)):
        if not(board[i] == "X" or board[i] == "O"):
            
            # make a test move
            analysis_board = board.copy()
            analysis_board[i] = ai
            boards_considered +=1
            list_of_boards_considered.append(analysis_board)
            # see if its good
            evaluation, boards_considered, list_of_boards_considered = minimax(analysis_board, 0, True, player, ai, boards_considered, list_of_boards_considered)

            if evaluation < currentEval:
                bestMove = i
                currentEval = evaluation
                # print(bestMove)
    return bestMove, boards_considered, list_of_boards_considered

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
        draw = True
        for tile in board:
            if not(tile == "X" or tile == "O"):
                draw = False
    else:
        draw = False

    return o_won, x_won, draw

pause_to_display_analysis = False

def game():
    done = False
    while not done:
        if not pause_to_display_analysis:
            # player moves
            player_move = input("Enter move: ")
            if player_move == "pass":
                pass
            else:
                board[int(player_move)] = player
            print_board(board)

            # check if done
            player_won, ai_won, draw = check_if_won(board)

            if player_won:
                print("Player won!!")
                break
            if ai_won:
                print("ai won!!")
                break
            if draw:
                print("Draw!!")
                break

            print("----------")

        # computer moves
        boards_considered = 0
        
        # find how many board
        list_of_boards_considered = []
        computer_move, boards_considered, list_of_boards_considered = find_computer_move(board, ai, player, boards_considered, list_of_boards_considered)
        print(boards_considered, list_of_boards_considered)
        
        board[computer_move] = ai
        
        print_board(board)


game()
