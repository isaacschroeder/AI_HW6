
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

class Board:
    def __init__(self):
        # 9x9 board flattened
        self.size = 81

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
