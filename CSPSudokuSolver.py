import typing

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

    def getPosition(self) -> tuple[int,int]:
        return (self.x, self.y)

    def placeEntry(self) -> int:
        nextValue = min(self.domain)
        self.domain = {}
        self.entry = nextValue
        return nextValue

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
        self.placeTiles(startingState)

    def __str__(self):
        print("_____________________________________")
        for i in range(9):
            row_string = "| "
            for entry in self.getEntriesByX(i+1):
                value = " "
                if entry != None:
                    value = entry
                row_string += str(value)
                row_string += " | "
            print(row_string)
            print("_____________________________________")
        return ""
    
    def placeTiles(self, startingState):
        for i in range(9):
            j = 0
            for tile in self.getByX(i+1):
                block = getBlockNum(i+1,j+1)
                if startingState[i][j] != 'e':
                    tile.entry = int(startingState[i][j])
                    tile.domain = {}
                    self.forwardCheck(i+1, j+1, block, int(startingState[i][j]))
                else:
                    tile.entry = None
                j += 1

    def getByX(self, x) -> typing.List[Tile]:
        return [tile for tile in self.board if tile.x == x]

    def getEntriesByX(self,x) -> typing.List[int]:
        return [tile.entry for tile in self.board if tile.x == x]

    def getByY(self, y) -> typing.List[Tile]:
        return [tile for tile in self.board if tile.y == y]

    def getEntriesByY(self,y) -> typing.List[int]:
        return [tile.entry for tile in self.board if tile.y == y]

    def getByBlock(self, block) -> typing.List[Tile]:
        return [tile for tile in self.board if tile.block == block]

    def getEntriesByBlock(self, block) -> typing.List[int]:
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
        for (x,y,b) in zip(self.getByX(x),self.getByY(y),self.getByBlock(block)):
            x.updateDomain(entry)
            y.updateDomain(entry)
            b.updateDomain(entry)
            if x.domainEmpty() or y.domainEmpty() or b.domainEmpty():
                return False
        return True

    # Returns number of constraints that a given tile has on other unassigned variables.
    # Essentially, this is the number of unassigned variables other than itself in its row, column and block.
    def tileConstraintInvolvmentCount(self, tile_of_concern):
        count = 0
        # Check horizontal
        row = self.getByX(tile_of_concern.x)
        for tile in row:
            # Ensure not counting the tile of concern itself
            if tile is not tile_of_concern and tile.entry is None:
                count += 1
        # Check vertical
        column = self.getByY(tile_of_concern.y)
        for tile in column:
            # Ensure not counting the tile of concern itself
            if tile is not tile_of_concern and tile.entry is None:
                count += 1
        # Check block
        block = self.getByBlock(tile_of_concern.block)
        for tile in block:
            # Ensure not counting the tile of concern itself
            if tile is not tile_of_concern and tile.entry is None:
                count += 1
        return count

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


# Return the position of the tile to be selected for assignment next.
# Efficiently selects the next variable to be assigned based on minimum remaining values,
# and breaks ties with the degree heuristic.
def select_unassigned_tile(board):
    # Get a list of all the unassigned tiles in the board.
    unassigned = [tile for tile in board if tile.entry is None]
    # Determine best tile choice(s) based on fewest remaining values
    best_tile_choice_mrv = None
    for tile in unassigned:
        if best_tile_choice_mrv is None or len(tile.domain) < len(best_tile_choice_mrv.domain):
            best_tile_choice_mrv = [tile]
        elif len(tile.domain) == len(best_tile_choice_mrv.domain):
            best_tile_choice_mrv.append(tile)
    # Break tile ties with the degree heuristic
    best_tile_choice_deg = None
    best_degree_count = None
    for tile in best_tile_choice_mrv:
        tile_degree_count = board.tileConstraintInvolvmentCount(tile)
        if best_tile_choice_deg is None or tile_degree_count < best_degree_count:
            best_tile_choice_deg = [tile]
            best_degree_count = board.tileConstraintInvolvmentCount(best_tile_choice_deg)
        elif tile_degree_count == best_degree_count:
            best_tile_choice_deg.append(tile)
    # Break additional ties based on tile position (top left highest priority)
    best_tile_choice = None
    for tile in best_tile_choice_deg:
        if best_tile_choice is None or tile < best_tile_choice:
            best_tile_choice = tile
    return best_tile_choice


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
    print(puzzle)
    print(puzzle.getByX(9)[8].domain)
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


# Call to main
main()
