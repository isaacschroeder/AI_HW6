

#Sudoku CSP:
#   Variables: Each board tile
#   Domain: 1-9
#   Constraints: row, column, and block constraints
#   Goal: Assign a value to each variable without violating constraints
class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

class Board:
    def __init__(self):
        # 9x9 board flattened
        self.size = 81
        self.unassigned = self.size

        # none signifies empty space
        board = []

        self.board = board
    class Tile:
        def __init__(self,x,y,block,entry):
            self.x = x
            self.y = y
            self.block = block
            self.entry = entry
            self.domain = {1,2,3,4,5,6,7,8,9}
            if entry == None:
                self.domain.remove(entry)

    def getByX(self,x):
        self.board

def recursive_backtracking(board):
    if board.unassigned == 0:
        return True
    position = select_unassigned_tile(board)
    for value in order_domain_values(board, position):


# Return the position of the tile to be selected for assignment next
def select_unassigned_tile(board):
    return Position(1, 1)

# Return a list of the domain values to be used for
def order_domain_values(board, position):
    return [1,2,3,4,5,6,7,8,9]



