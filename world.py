# encoding: utf-8

from enum import Enum
from copy import deepcopy

from dungeon.map import Map
from dungeon.creatures import Hero


class State(Enum):
    RUNNING = 1
    FINISHED = 0


class World:
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.hero = Hero(*dungeon.hero_position, 1)
        self.objects = [deepcopy(obj) for obj in dungeon.objects]
        self.state = State.RUNNING

    def update(self, dt):
        if not self.hero.hp or not self.objects:
            self.state = State.FINISHED
            return

        self.hero.update(dt, self)

    def reset(self):
        self.objects = [deepcopy(obj) for obj in self.dungeon.objects]
        self.hero.x = self.dungeon.hero_position[0]
        self.hero.y = self.dungeon.hero_position[1]
        self.hero.set_level(1)
        self.state = State.RUNNING
