# encoding: utf-8

import random
import math
from functools import lru_cache

import pyglet

from dungeon.map import Wall, Floor, Map
from dungeon.items import Potion
from dungeon.creatures import Hero, Abomination, Creature
from world import World

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 24
WORLDS_COUNT = 10
COLORS = {
    Wall: (69, 61, 66),
    Floor: (133, 124, 119),
    Hero: (234, 243, 247),
    Abomination: (66, 27, 79),
    'blood': (204, 23, 33),
    'background': (46 / 255, 38 / 255, 45 / 255, 1),
}


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pyglet.gl.glClearColor(*COLORS['background'])
        pyglet.clock.schedule_interval(self.update, 0.1)

        self.tiles_batch = pyglet.graphics.Batch()
        self.objects_batch = pyglet.graphics.Batch()
        self.fx_batch = pyglet.graphics.Batch()
        self.heroes_batch = pyglet.graphics.Batch()

        self.tile_sprites = []
        self.objects_sprites = {}

        self.map = None
        self.make_map('level1.txt')
        self.make_objects_sprites()

        self.worlds = [World(self.map) for _ in range(WORLDS_COUNT)]

        self.make_heroes_sprites()

        def death(creature):
            blood = pyglet.sprite.Sprite(
                self.animation('blood.png', 1, 14, 1/50, False),
                batch=self.fx_batch,
                **self.coords_to_gl(creature.x, creature.y)
            )
            blood.color = COLORS['blood']
            self.objects_sprites[creature.id].opacity -= 255 / WORLDS_COUNT

        Creature.killed.append(death)

    def coords_to_gl(self, x, y):
        return {
            'x': x * SPRITE_WIDTH,
            'y': self.height - (y * SPRITE_HEIGHT) - SPRITE_HEIGHT,
        }

    @lru_cache(maxsize=None)
    def texture_grid(self, filename, height, width):
        return pyglet.image.TextureGrid(pyglet.image.ImageGrid(
            pyglet.image.load('assets/{}'.format(filename)), height, width)
        )

    @lru_cache(maxsize=None)
    def animation(self, filename, height, width, period, loop=True):
        return pyglet.image.Animation.from_image_sequence(
            pyglet.image.TextureGrid(pyglet.image.ImageGrid(
                pyglet.image.load('assets/{}'.format(filename)), height, width)
            ),
            period,
            loop
        )

    def make_map(self, filename):
        self.map = Map('assets/{}'.format(filename))
        for x in range(self.map.width):
            for y in range(self.map.height):
                tile = self.map.tiles[x][y]
                if isinstance(tile, Wall):
                    if y == self.map.height - 1 or self.map.tiles[x][y + 1].passable:
                        img = self.texture_grid('wall.png', 2, 1)[0]
                    else:
                        img = self.texture_grid('wall.png', 2, 1)[1]
                elif isinstance(tile, Floor):
                    if random.random() > 0.8:
                        img = random.choice(self.texture_grid('floor.png', 1, 7))
                    else:
                        img = self.texture_grid('floor.png', 1, 7)[0]

                sprite = pyglet.sprite.Sprite(
                    img=img,
                    batch=self.tiles_batch,
                    **self.coords_to_gl(x, y),
                )
                sprite.color = COLORS[tile.__class__]
                self.tile_sprites.append(sprite)

    def make_objects_sprites(self):
        for obj in self.map.objects:
            if isinstance(obj, Abomination):
                img = self.animation('abomination.png', 2, 1, 0.5)
            sprite = pyglet.sprite.Sprite(img, batch=self.objects_batch, **self.coords_to_gl(obj.x, obj.y))
            sprite.game_object = obj
            sprite.color = COLORS[obj.__class__]
            self.objects_sprites[obj.id] = sprite

    def make_heroes_sprites(self):
        for idx, world in enumerate(self.worlds):
            hero = world.hero
            sprite = pyglet.sprite.Sprite(
                self.animation('hero.png', 2, 1, 0.5),
                batch=self.heroes_batch,
                **self.coords_to_gl(hero.x, hero.y)
            )
            sprite.game_object = hero
            color = hsv_to_rgb((360 / WORLDS_COUNT) * idx, 0.8, 1)
            sprite.color = (channel * 255 for channel in color)
            self.objects_sprites[hero.id] = sprite

    def reset(self):
        for world in self.worlds:
            world.reset()
        for sprite in self.objects_sprites.values():
            sprite.opacity = 255

    def on_draw(self):
        self.clear()
        self.tiles_batch.draw()
        self.objects_batch.draw()
        self.fx_batch.draw()
        self.heroes_batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.reset()
        elif symbol == pyglet.window.key.ESCAPE:
            self.close()

    def update(self, dt):
        for world in self.worlds:
            world.update(dt)
        for sprite in self.objects_sprites.values():
            sprite.set_position(**self.coords_to_gl(sprite.game_object.x, sprite.game_object.y))


def hsv_to_rgb(h, s, v):
    if s == 0:
        return v, v, v

    h /= 60.0
    i = math.floor(h)
    f = h - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    return v, p, q


if __name__ == '__main__':
    window = Window(width=816, height=900)
    pyglet.app.run()
