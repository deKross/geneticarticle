# coding: utf-8

import random


class Creature:
    def __init__(self, x, y, level):
        self.active = True
        self.x = x
        self.y = y
        self.level = level
        self.damage = level
        self.hp = level

    def die(self):
        self.active = False


class Hero(Creature):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = None
        self.used_targets = {self}

    def move(self, dx, dy, dungeon):
        x = self.x + dx
        y = self.y + dy
        if not dungeon.tiles[x][y].passable:
            return []
        self.x = x
        self.y = y
        return True

    def attack(self, target):
        if self.damage >= target.hp:
            return True
        self.hp -= target.damage

    def select_target(self, dungeon):
        pool = [
            obj for obj in dungeon.objects
            if obj not in self.used_targets
        ]
        if not pool:
            return None
        target = random.choice(pool)
        self.used_targets.add(target)
        return target

    def update(self, dt, dungeon):
        if not self.path:
            destination = self.select_target(dungeon)
            if not destination:
                return

            self.path = list(dungeon.astar.find((destination.x, destination.y), (self.x, self.y)))

        node = self.path.pop(0)
        if not self.move(node[0] - self.x, node[1] - self.y, dungeon):
            return
        for object in dungeon.objects:
            if object is self:
                continue
            if object.x != self.x or object.y != self.y:
                continue
            self.used_targets.add(object)
            if isinstance(object, Abomination):
                if self.attack(object):
                    object.die()


class Abomination(Creature):
    pass
