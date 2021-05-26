import random

from utils import BoardPos, Board


def read_commands():
    while True:
        user_input = input('Input command: ')
        if user_input == 'exit':
            exit()

        if user_input == 'help':
            print('''
Supported commands:
help - displays more information.
exit - exits the program.
start - lets you play a game specifying X and O. For example:
start user user (play both X and O)
start user easy (play as X against the easy AI
start hard easy (see the hard AI play against the easy AI)

AI modes:
easy - makes random moves.
medium - makes random moves but react if it can win in the next move or its opponent can.
hard - uses minimax (with alpha-beta pruning) to quickly search all possible moves and find the best one.

Enter the board coordinates in the pattern "row column". "1 1" refers to the top left corner.
            ''')
            continue

        if user_input.startswith('start'):
            input_parts = user_input.split()
            if len(input_parts) == 3:
                return [input_parts[1], input_parts[2]]

        print('Bad parameters!')


def opposite(cell_value: str):
    return 'X' if cell_value == 'O' else 'O'


def read_user_input(board: Board):
    while True:
        user_input_parts = input('Enter the coordinates:').split()

        if len(user_input_parts) != 2:
            print('You should enter 2 numbers')
            continue

        try:
            row = int(user_input_parts[0])
            col = int(user_input_parts[1])
        except ValueError:
            print('You should enter numbers!')
            continue

        if not (1 <= row <= 3 and 1 <= col <= 3):
            print('Coordinates should be from 1 to 3!')
            continue

        pos = BoardPos(row - 1, col - 1)
        if not board.is_empty(pos):
            print('This cell is occupied! Choose another one!')
            continue
        return pos


def user_move(board: Board):
    move = read_user_input(board)
    return move


def ai_move_easy(board: Board):
    # Random moves
    return random.choice(board.get_all_empty())


def ai_move_medium(board: Board, cell_value: str):
    win_conditions = Board.win_conditions
    for condition in win_conditions:
        values = []
        for cell in condition:
            values.append(board.get_cell(cell))

        # If one empty square
        if values.count(' ') == 1:
            # If it already has two in a row and can win with one further move
            if values.count(cell_value) == 2:
                return condition[values.index(' ')]

            # If its opponent can win with one move
            if values.count(opposite(cell_value)) == 2:
                return condition[values.index(' ')]
    # Else, make a random move
    return ai_move_easy(board)


def find_best_movement_recursive(board: Board, cell_value: str, alpha: int, beta: int):
    # Minimax with alpha beta pruning to speed up the search

    # Base case
    winner = board.game_winner()
    if winner is not None:
        if winner == ' ':
            return 0
        elif winner == cell_value:
            return 10
        else:
            return -10

    possible_positions = board.get_all_empty()
    for pos in possible_positions:
        temp_board = board.copy()
        temp_board.set_cell(pos, cell_value)
        evaluation = -find_best_movement_recursive(temp_board, opposite(cell_value), -beta, -alpha)
        if evaluation >= beta:
            # Move was good, so the opponent will avoid this position
            return beta
        alpha = max(alpha, evaluation)
    return alpha


def ai_move_hard(board: Board, cell_value: str):
    possible_positions = board.get_all_empty()
    best_option = None
    best_score = -100
    for pos in possible_positions:
        temp_board = board.copy()
        temp_board.set_cell(pos, cell_value)
        score = -find_best_movement_recursive(temp_board, opposite(cell_value), -100, 100)
        if score > best_score:
            best_option = pos
            best_score = score
    return best_option


def main():
    print('Type "help" for more information')
    while True:
        turn = 0
        players = read_commands()
        board = Board()
        print(board)

        while True:
            player_turn = turn % 2
            cell_value = 'X' if player_turn == 0 else 'O'

            if players[player_turn] == 'user':
                move = user_move(board)
            else:
                ai_level = players[player_turn]
                print(f'Making move level "{ai_level}"')
                if ai_level == 'easy':
                    move = ai_move_easy(board)
                elif ai_level == 'medium':
                    move = ai_move_medium(board, cell_value)
                else:
                    move = ai_move_hard(board, cell_value)

            board.set_cell(move, cell_value)
            print(board)

            winner = board.game_winner()
            # If we have a winner
            if winner is not None:
                if winner == 'X':
                    print('X wins')
                elif winner == 'O':
                    print('O wins')
                else:
                    print('Draw')
                break

            turn += 1


main()
