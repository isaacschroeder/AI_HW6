

class Board:
    def __init__(self):
        # 9x9 board
        self.size = 9

        # none signifies empty space
        board = []
        for x in range(self.row_count):
            row = []
            for y in range(self.col_count):
                row.append(None)
            board.append(row)
        self.board = board