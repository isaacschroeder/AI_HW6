
class Tile:
    def __init__(self,x,y,block,entry):
        self.x = x
        self.y = y
        self.block = block
        self.entry = entry
        self.domain = {1,2,3,4,5,6,7,8,9}
        if entry != None:
            self.domain = {}
            
    def updateDomain(self, entry):
        if self.entry == None:
            self.domain.remove(entry)
            
    def domainEmpty(self) -> bool:
        if len(self.domain) or self.entry != None:
            return False
        return True

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

    def getByX(self, x) -> Tile.Array:
        return [tile for tile in self.board if tile.x == x]

    def getEntriesByX(self,x) -> int.Array:
        return [tile.entry for tile in self.board if tile.x == x]

    def getByY(self, y) -> Tile.Array:
        return [tile for tile in self.board if tile.y == y]

    def getEntriesByY(self,y) -> int.Array:
        return [tile.entry for tile in self.board if tile.y == y]

    def getByBlock(self, block) -> Tile.Array:
        return [tile for tile in self.board if tile.block == block]

    def getEntriesByBlock(self, block) -> int.Array:
        return [tile.entry for tile in self.board if tile.block == block]

    def isConflict(self,x,y,block,entry) -> bool:
        if entry in self.getEntriesByX(x):
            return True
        elif entry in self.getEntriesByY(y):
            return True
        elif entry in self.getEntriesByBlock(block):
            return True
        else:
            return False

    def forwardCheck(self,x,y,block,entry) -> bool:
        for x,y,b in self.getByX(x),self.getByY(y),self.getByBlock(block):
            x.updateDomain(entry)
            y.updateDomain(entry)
            b.updateDomain(entry)
            if x.domainEmpty() or y.domainEmpty() or b.domainEmpty():
                return False
        return True



# Recursively solves the Sudoku problem.
# Returns a sovled board on success, None on failure.
def recursive_backtracking(board):
    if board.unassigned == 0:
        return board
    position = select_unassigned_tile(board)
    for value in order_domain_values(board, position):
        new_board = assign_tile(board, position, value)
        if new_board is not None:
            return recursive_backtracking(new_board)
        else:
            return None

# Return the position of the tile to be selected for assignment next
def select_unassigned_tile(board):
    return Position(1, 1)

# Return a list of the domain values to be used for
def order_domain_values(board, position):
    return [1,2,3,4,5,6,7,8,9]

# Returns a new board with the tile at the given position set to the given value.
# The domains of various other variables are updated via forward checking.
# If forward checking finds a dead end, None is returned
def assign_tile(board, position, value):
    return None



