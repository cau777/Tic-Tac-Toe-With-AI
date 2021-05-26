class BoardPos:
    def __init__(self, row: int = 0, col: int = 0):
        self.row = row
        self.col = col

    def __str__(self):
        return f'({self.row}, {self.col})'


class Board:
    win_conditions = (
        (BoardPos(0, 0), BoardPos(0, 1), BoardPos(0, 2)), (BoardPos(1, 0), BoardPos(1, 1), BoardPos(1, 2)),
        (BoardPos(2, 0), BoardPos(2, 1), BoardPos(2, 2)), (BoardPos(0, 0), BoardPos(1, 0), BoardPos(2, 0)),
        (BoardPos(0, 1), BoardPos(1, 1), BoardPos(2, 1)), (BoardPos(0, 2), BoardPos(1, 2), BoardPos(2, 2)),
        (BoardPos(0, 0), BoardPos(1, 1), BoardPos(2, 2)), (BoardPos(0, 2), BoardPos(1, 1), BoardPos(2, 0)))

    def __init__(self, initial_config='         '):
        self.board = []
        for row in range(3):
            board_row = list(initial_config[row * 3: (row + 1) * 3])
            self.board.append(board_row)

    def __str__(self):
        rep = '---------\n'
        for row in self.board:
            rep += '| ' + ' '.join(row) + ' |\n'
        rep += '---------'
        return rep

    def count(self, value: str):
        count = 0
        for row in self.board:
            count += row.count(value)
        return count

    def verify_win_condition(self, condition: tuple):
        value1, value2, value3 = self.get_cell(condition[0]), self.get_cell(condition[1]), self.get_cell(condition[2])
        if value1 == value2 == value3 != ' ':
            return value1
        else:
            return False

    def game_winner(self):
        for condition in Board.win_conditions:
            winner = self.verify_win_condition(condition)
            if winner:
                return winner

        if self.count(' ') == 0:
            # Draw
            return ' '
        else:
            # Game isn't over
            return None

    def get_cell(self, pos: BoardPos):
        return self.board[pos.row][pos.col]

    def is_empty(self, pos: BoardPos):
        return self.get_cell(pos) == ' '

    def get_all_empty(self):
        empty_positions = []
        for row in range(3):
            for col in range(3):
                pos = BoardPos(row, col)
                if self.is_empty(pos):
                    empty_positions.append(pos)
        return empty_positions

    def set_cell(self, pos: BoardPos, value: str):
        self.board[pos.row][pos.col] = value

    def copy(self):
        board_config = ''
        for row in range(3):
            for col in range(3):
                board_config += self.get_cell(BoardPos(row, col))
        return Board(board_config)
