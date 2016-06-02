import math
import random
from _heapq import heappop, heappush
from collections import defaultdict

SQRT2 = math.sqrt(2)


class TileGrid:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x2 = x + width - 1
        self.y2 = y + height - 1

    def neighbors(self, x, y):
        if x < self.x or y < self.y or x > self.x2 or y > self.y2:
            raise StopIteration

        if x > self.x:
            yield (x - 1, y), 1
        if y > self.y:
            yield (x, y - 1), 1
        if x < self.x2:
            yield (x + 1, y), 1
        if y < self.y2:
            yield (x, y + 1), 1


class OctileGrid(TileGrid):
    def neighbors(self, x, y):
        if x < self.x or y < self.y or x > self.x2 or y > self.y2:
            raise StopIteration

        left = x > self.x
        top = y > self.y
        right = x < self.x2
        bottom = y < self.y2

        if left:
            yield (x - 1, y), 1
        if left and top:
            yield (x - 1, y - 1), SQRT2
        if top:
            yield (x, y - 1), 1
        if top and right:
            yield (x + 1, y - 1), SQRT2
        if right:
            yield (x + 1, y), 1
        if right and bottom:
            yield (x + 1, y + 1), SQRT2
        if bottom:
            yield (x, y + 1), 1
        if bottom and left:
            yield (x - 1, y + 1), SQRT2


class AStar:
    def __init__(self, grid, cost=None, heuristic=None):
        self.grid = grid
        self.cost = cost if cost else self.default_cost
        if heuristic is None:
            if isinstance(grid, TileGrid):
                self.heuristic = self.default_heuristic_orthogonal
            else:
                self.heuristic = self.default_heuristic_diagonal
        else:
            self.heuristic = heuristic

    @staticmethod
    def default_cost(origin, destination):
        return 1

    @staticmethod
    def default_heuristic_orthogonal(origin, destination):
        dx = abs(origin[0] - destination[0])
        dy = abs(origin[1] - destination[1])
        return dx + dy + random.random() * 0.001 + random.random() * 0.001

    @staticmethod
    def default_heuristic_diagonal(origin, destination):
        dx = abs(origin[0] - destination[0])
        dy = abs(origin[1] - destination[1])
        return (dx + dy) + (SQRT2 - 2) * min(dx, dy) + random.random() * 0.001

    def find(self, origin, destination):
        frontier = []
        heappush(frontier, (0, origin))
        came_from = {origin: None}
        accumulated_cost = defaultdict(lambda: float('inf'))
        accumulated_cost[origin] = 0

        while frontier:
            current = heappop(frontier)[1]

            if current == destination:
                break

            for next, base_cost in self.grid.neighbors(*current):
                calculated = self.cost(current, next) * base_cost
                if not calculated:
                    continue
                new_cost = accumulated_cost[current] + calculated
                if new_cost < accumulated_cost[next]:
                    accumulated_cost[next] = new_cost
                    priority = new_cost + self.heuristic(next, destination)
                    heappush(frontier, (priority, next))
                    came_from[next] = current

        current = destination
        yield current
        while current != origin:
            current = came_from[current]
            yield current
