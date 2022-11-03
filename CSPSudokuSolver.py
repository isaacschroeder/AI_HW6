
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

class Board:
    def __init__(self, startingState):
        # 9x9 board flattened
        self.size = 81

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
    
    def createTiles(self, startingState):
        tiles = []
        for i in range(9):
            for j in range(9):
                if startingState[i][j] != 'e':
                    tiles.append(self.Tile(i, j, self.getBlockNum(i, j), startingState[i][j]))

    def getByX(self,x):
        self.board

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