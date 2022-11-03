

class Board:
    def __init__(self):
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

    def getByX(self,x):
        self.board