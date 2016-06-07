# coding: utf-8

import random

from core.event import Event


class Creature:
    killed = Event()
    levelled = Event()
    maxID = 0

    def __init__(self, x, y, level):
        self.active = True
        self.x = x
        self.y = y
        self.level = level
        self.damage = level
        self.hp = level
        self.id = Creature.maxID
        Creature.maxID += 1

    @property
    def alive(self):
        return self.hp > 0

    def die(self):
        self.killed(self)

    def set_level(self, level):
        self.level = level
        self.damage = level
        self.hp = level
        self.levelled(self)


class Hero(Creature):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = None
        self.used_targets = [self]

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
        self.used_targets.remove(target)
        return False

    def select_target(self, objects):
        pool = [
            obj for obj in objects
            if obj not in self.used_targets
        ]
        if not pool:
            return None
        target = random.choice(pool)
        self.used_targets.append(target)
        return target

    def update(self, dt, world):
        if not self.path:
            destination = self.select_target(world.objects)
            if not destination:
                return

            self.path = list(world.dungeon.astar.find((destination.x, destination.y), (self.x, self.y)))

        node = self.path.pop(0)
        if not self.move(node[0] - self.x, node[1] - self.y, world.dungeon):
            return
        for object in world.objects:
            if object.x != self.x or object.y != self.y:
                continue
            self.used_targets.append(object)
            if isinstance(object, Abomination) and object.alive:
                if self.attack(object):
                    object.die()


class Abomination(Creature):
    pass
