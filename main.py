# encoding: utf-8

import random

import pyglet

from dungeon.map import Wall, Floor, Map
from dungeon.items import Potion
from dungeon.creatures import Hero, Abomination

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 24
COLORS = {
    Wall: (69, 61, 66),
    Floor: (133, 124, 119),
    Hero: (234, 243, 247),
    Abomination: (27, 4, 31),
}


window = pyglet.window.Window(width=816, height=900)

def coords_to_gl(x, y):
    return {
        'x': x * SPRITE_WIDTH,
        'y': window.height - (y * SPRITE_HEIGHT) - SPRITE_HEIGHT,
    }

floor_tex = pyglet.image.TextureGrid(pyglet.image.ImageGrid(pyglet.image.load('assets/floor.png'), 1, 7))
wall_tex = pyglet.image.TextureGrid(pyglet.image.ImageGrid(pyglet.image.load('assets/wall.png'), 2, 1))
hero_ani = pyglet.image.Animation.from_image_sequence(
    pyglet.image.TextureGrid(pyglet.image.ImageGrid(pyglet.image.load('assets/hero.png'), 2, 1)),
    0.5
)
abomination_ani = pyglet.image.Animation.from_image_sequence(
    pyglet.image.TextureGrid(pyglet.image.ImageGrid(pyglet.image.load('assets/abomination.png'), 2, 1)),
    0.5
)

map = Map('assets/level1.txt')
tiles_batch = pyglet.graphics.Batch()
objects_batch = pyglet.graphics.Batch()

tile_sprites = []
objects_sprites = []
for x in range(map.width):
    for y in range(map.height):
        tile = map.tiles[x][y]
        if isinstance(tile, Wall):
            if y == map.height - 1 or map.tiles[x][y + 1].passable:
                img = wall_tex[0]
            else:
                img = wall_tex[1]
        elif isinstance(tile, Floor):
            img = random.choice(floor_tex)

        sprite = pyglet.sprite.Sprite(
            img=img,
            batch=tiles_batch,
            **coords_to_gl(x, y),
        )
        sprite.color = COLORS[tile.__class__]
        tile_sprites.append(sprite)

for obj in map.objects:
    if isinstance(obj, Hero):
        img = hero_ani
    elif isinstance(obj, Abomination):
        img = abomination_ani
    sprite = pyglet.sprite.Sprite(img, batch=objects_batch, **coords_to_gl(obj.x, obj.y))
    sprite.color = COLORS[obj.__class__]
    objects_sprites.append(sprite)

@window.event
def on_draw():
    window.clear()
    tiles_batch.draw()
    objects_batch.draw()


pyglet.gl.glClearColor(46/255, 38/255, 45/255, 1)
pyglet.app.run()
