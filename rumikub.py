from enum import Enum
from itertools import combinations
import random

class Color(Enum):
    RED = "r"
    YELLOW = "y"
    BLUE = "u"
    BLACK = "k"

colors = [Color.RED, Color.YELLOW, Color.BLUE, Color.BLACK]

class Tile():
    def __init__(self, color, number):
        self.index = (colors.index(color) * 13) + number
        self.color = color
        self.number = number
        
    def __str__(self):
        return str(self.color.value) + str(self.number)

    def __repr__(self):
        return str(self.color.value) + str(self.number)

class OrderedTileGroup():
    def __init__(self, startingTiles = []):
        self.tiles = startingTiles

    def addTile(self, tile):
        spotToAdd = next((i for i, _ in enumerate(self.tiles) if tile.index < self.tiles[i].index), len(self.tiles))
        self.tiles.insert(spotToAdd, tile)

    def filterByNumber(self, num):
        return OrderedTileGroup(list(filter(lambda t: t.number == num, self.tiles)))

    def filterByColor(self, color):
        return OrderedTileGroup(list(filter(lambda t: t.color == color, self.tiles)))

    def __str__(self):
        return ".".join(map(str, self.tiles))

    def __repr__(self):
        return ".".join(map(str, self.tiles))

    def __len__(self):
        return len(self.tiles)

    def __iter__(self):
        return iter(self.tiles)
        
class Game():
    def __init__(self):
        self.unselectedTiles = OrderedTileGroup()
        self.createAllTiles()

    def createAllTiles(self):
        for color in colors:
            for i in range(1, 14):
                self.unselectedTiles.addTile(Tile(color, i))

    def pick14(self):
        pickedTiles = OrderedTileGroup([])
        for _ in range(20):
            tile = random.choice(self.unselectedTiles.tiles)
            #print(tile)
            pickedTiles.addTile(tile)
            self.unselectedTiles.tiles.remove(tile)
        print(pickedTiles, organizeTiles(pickedTiles))

def organizeTiles(tiles):
    def generateSetCombinations(tiles):
        result = []
        for r in range(3, len(tiles) + 1):
            result.extend(combinations(tiles, r))
        return result

    def generateRunCombinations(tile_group):
        tiles = sorted(tile_group.tiles, key=lambda t: t.number)  # Sort tiles by number
        result = []
        for start in range(len(tiles)):
            run = [tiles[start]]
            for next_tile in tiles[start + 1:]:
                if next_tile.number == run[-1].number + 1:  # Check for consecutive numbers
                    run.append(next_tile)
                    if len(run) >= 3:  # Add only if the run has at least 3 tiles
                        result.append(tuple(run))
                else:
                    break  # Stop if the sequence is broken
        return result

    groups = []
    
    for i in range(1, 14):
        numberTiles = tiles.filterByNumber(i)
        groups.extend(generateSetCombinations(numberTiles))

    for c in colors:
        colorTiles = tiles.filterByColor(c)
        groups.extend(generateRunCombinations(colorTiles))

    return groups

game = Game()
#organizeTiles(game.unselectedTiles)
game.pick14()
