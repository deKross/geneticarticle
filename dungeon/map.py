# encoding: utf-8

from .creatures import Hero, Abomination
from .pathfinding import TileGrid, AStar


class Wall:
    passable = False


class Floor:
    passable = True


class Map:
    def __init__(self, filename):
        with open(filename, 'rt') as file:
            lines = file.readlines()
        floor = Floor()
        wall = Wall()
        self.width = len(lines[0]) // 2
        self.height = len(lines)
        self.hero_position = None
        self.tiles = [[floor for y in range(self.height)] for x in range(self.width)]
        self.objects = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line.split()):
                if char == '#':
                    self.tiles[x][y] = wall
                elif char == '@':
                    self.hero_position = (x, y)
                elif char.isdigit():
                    self.objects.append(Abomination(x, y, int(char)))
        grid = TileGrid(0, 0, self.width, self.height)
        self.astar = AStar(grid, cost=lambda o, d: int(self.tiles[d[0]][d[1]].passable))
