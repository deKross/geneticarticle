# encoding: utf-8

from .creatures import Hero, Abomination


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
        self.hero = None
        self.tiles = [[floor for y in range(self.height)] for x in range(self.width)]
        self.objects = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line.split()):
                if char == '#':
                    self.tiles[x][y] = wall
                elif char == '@':
                    self.hero = Hero(x, y, 1)
                    self.objects.append(self.hero)
                elif char.isdigit():
                    self.objects.append(Abomination(x, y, int(char)))
