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

    def sum(self):
        return sum(map(lambda t: t.number, self.tiles))

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
        
        for _ in range(26):
            tile = random.choice(self.unselectedTiles.tiles)
            pickedTiles.addTile(tile)
            self.unselectedTiles.tiles.remove(tile)
            
        findBestMove(pickedTiles)

def findPlayableGroups(tiles):
    def generateSetCombinations(tiles):
        result = []
        for r in range(3, len(tiles) + 1):
            result.extend(combinations(tiles, r))
        return result

    def generateRunCombinations(tile_group):
        tiles = sorted(tile_group.tiles, key=lambda t: t.number)
        result = []
        for start in range(len(tiles)):
            run = [tiles[start]]
            for next_tile in tiles[start + 1:]:
                if next_tile.number == run[-1].number + 1:
                    run.append(next_tile)
                    if len(run) >= 3:
                        result.append(tuple(run))
                else:
                    break
        return result

    groups = []
    
    for i in range(1, 14):
        numberTiles = tiles.filterByNumber(i)
        groups.extend(generateSetCombinations(numberTiles))

    for c in colors:
        colorTiles = tiles.filterByColor(c)
        groups.extend(generateRunCombinations(colorTiles))

    return groups

def findBestMove(tiles):
    bestTilesByNum = tiles
    numOfTiles = len(tiles)
    groupsPlayedNum = []
    
    bestTilesBySum = tiles
    sumOfTiles = tiles.sum()
    groupsPlayedSum = []
    
    def iterative(tiles, groups, groupsPlayed):
        nonlocal numOfTiles, bestTilesByNum, groupsPlayedNum, sumOfTiles, bestTilesBySum, groupsPlayedSum
        for i, group in enumerate(groups):
            if all(tile in tiles for tile in group):
                remainingTiles = tiles.tiles[:]
                for tile in group:
                    remainingTiles.remove(tile)
                remainingGroups = groups[:]
                remainingGroups.pop(i)
                nextGroupsPlayed = groupsPlayed[:]
                nextGroupsPlayed.append(group)
                iterative(OrderedTileGroup(remainingTiles), remainingGroups, nextGroupsPlayed)
            else:
                if (len(tiles) < numOfTiles) or (len(tiles) == numOfTiles and tiles.sum() < bestTilesByNum.sum()):
                    bestTilesByNum = tiles
                    numOfTiles = len(tiles)
                    groupsPlayedNum = groupsPlayed
                if tiles.sum() < sumOfTiles or (tiles.sum() == sumOfTiles and len(tiles) < len(bestTilesBySum)):
                    bestTilesBySum = tiles
                    sumOfTiles = tiles.sum()
                    groupsPlayedSum = groupsPlayed
            
    iterative(tiles, findPlayableGroups(tiles), [])
    print(bestTilesByNum, numOfTiles, bestTilesByNum.sum(), groupsPlayedNum)
    print(bestTilesBySum, len(bestTilesBySum), sumOfTiles, groupsPlayedSum)
    

#game = Game()
#organizeTiles(game.unselectedTiles)
#game.pick14()

def stringToOrderedTileGroup(tile_string):
    tile_list = OrderedTileGroup()
    for tile_info in tile_string.split('.'):
        color_char = tile_info[0]
        number = int(tile_info[1:])
        color = next(color for color in Color if color.value == color_char)
        tile_list.addTile(Tile(color, number))
    return tile_list

x = stringToOrderedTileGroup("u2.u3.u4.y8.y9.y10.k8.u8.r8.y5.r5.u5.k5.k6.k7.y2.k2.r2.r1.r3.y11")
findBestMove(x)
