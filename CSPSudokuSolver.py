
def getBlockNum(i, j):
    if i <= 3:
        if j <= 3:
            return 1
        elif j <= 6:
            return 2
        else:
            return 3
    elif i <= 6:
        if j <= 3:
            return 4
        elif j <= 6:
            return 5
        else:
            return 6
    else:
        if j <= 3:
            return 7
        elif j <= 6:
            return 8
        else:
            return 9

class Tile:
    def __init__(self,x,y,block,entry):
        self.x = x
        self.y = y
        self.block = block
        self.entry = entry
        self.domain = {1,2,3,4,5,6,7,8,9}
        if entry != None:
            self.domain = {}

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __gt__(self, other) -> bool:
        if self.x == other.x:
            return self.y < other.y
        else:
            return self.x < other.x

    def updateDomain(self, entry):
        if self.entry == None:
            self.domain.discard(entry)
            
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
    def __init__(self, startingState):
        # 9x9 board flattened
        self.size = 81
        self.unassigned = self.size

        board = []
        for i in range(9):
            for j in range(9):
                board.append(Tile(i+1, j+1, getBlockNum(i+1, j+1), None))
        # none signifies empty space
        self.board = board
        self.board = self.placeTiles(startingState)

    def printBoard(self):
        print("_____________________________________")
        for i in range(9):
            row_string = "| "
            for entry in self.getEntriesByX(i+1):
                value = " "
                if entry != None:
                    value = entry
                row_string += value
                row_string += " | "
            print(row_string)
            print("_____________________________________")
    
    def placeTiles(self, startingState):
        for i in range(9):
            j = 0
            for tile in self.getByX(i+1):
                block = getBlockNum(i+1,j+1)
                if startingState[i][j] != 'e':
                    tile.entry = startingState[i][j]
                    self.forwardCheck(i, j, block, startingState[i][j])
                else:
                    tile.entry = None
                    self.forwardCheck(i, j, block, None)
                j += 1

    def getByX(self, x):
        return [tile for tile in self.board if tile.x == x]

    def getEntriesByX(self,x):
        return [tile.entry for tile in self.board if tile.x == x]

    def getByY(self, y):
        return [tile for tile in self.board if tile.y == y]

    def getEntriesByY(self,y):
        return [tile.entry for tile in self.board if tile.y == y]

    def getByBlock(self, block):
        return [tile for tile in self.board if tile.block == block]

    def getEntriesByBlock(self, block):
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

def main():
    startingState1 = [
        "ee1ee2eee",
        "ee5ee6e3e",
        "46eee5eee",
        "eee1e4eee",
        "6ee8ee143",
        "eeee9e5e8",
        "8eee49e5e",
        "1ee32eeee",
        "ee9eee3ee"
    ]

    puzzle = Board(startingState1)
    puzzle.printBoard()

    startingState2 = [
        "ee5e1eeee",
        "ee2ee4e3e",
        "1e9eee2e6",
        "2eee33333",
        "e4eeee7ee",
        "5eeee7ee1",
        "eee6e3eee",
        "e6e1eeeee",
        "eeee7ee5e"
    ]

    startingState3 = [
        "67eeeeeee",
        "e25eeeeee",
        "3eee8e9ee",
        "eeeeee8e1",
        "eee47eeee",
        "ee86eee9e",
        "eeeeeee1e",
        "1e6e5ee7e"
    ]

main()
