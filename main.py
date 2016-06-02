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
    Abomination: (66, 27, 79),
    'blood': (204, 23, 33),
    'background': (46 / 255, 38 / 255, 45 / 255, 1),
}


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pyglet.gl.glClearColor(*COLORS['background'])
        pyglet.clock.schedule_interval(self.update, 0.1)

        self.floor_texture = self.make_texture_grid('floor.png', 1, 7)
        self.wall_texture = self.make_texture_grid('wall.png', 2, 1)
        self.hero_animation = self.make_animation('hero.png', 2, 1, 0.5)
        self.abomination_animation = self.make_animation('abomination.png', 2, 1, 0.5)
        self.blood_animation = self.make_animation('blood.png', 1, 14, 1/50, False)

        self.tiles_batch = pyglet.graphics.Batch()
        self.objects_batch = pyglet.graphics.Batch()

        self.tile_sprites = []
        self.objects_sprites = []

        self.map = None
        self.make_map('level1.txt')
        self.make_objects_sprites()

    def coords_to_gl(self, x, y):
        return {
            'x': x * SPRITE_WIDTH,
            'y': self.height - (y * SPRITE_HEIGHT) - SPRITE_HEIGHT,
        }

    def make_texture_grid(self, filename, height, width):
        return pyglet.image.TextureGrid(pyglet.image.ImageGrid(
            pyglet.image.load('assets/{}'.format(filename)), height, width)
        )

    def make_animation(self, filename, height, width, period, loop=True):
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
                        img = self.wall_texture[0]
                    else:
                        img = self.wall_texture[1]
                elif isinstance(tile, Floor):
                    if random.random() > 0.8:
                        img = random.choice(self.floor_texture)
                    else:
                        img = self.floor_texture[0]

                sprite = pyglet.sprite.Sprite(
                    img=img,
                    batch=self.tiles_batch,
                    **self.coords_to_gl(x, y),
                )
                sprite.color = COLORS[tile.__class__]
                self.tile_sprites.append(sprite)

    def make_objects_sprites(self):
        for obj in self.map.objects:
            if isinstance(obj, Hero):
                img = self.hero_animation
            elif isinstance(obj, Abomination):
                img = self.abomination_animation
            sprite = pyglet.sprite.Sprite(img, batch=self.objects_batch, **self.coords_to_gl(obj.x, obj.y))
            sprite.game_object = obj
            sprite.color = COLORS[obj.__class__]
            self.objects_sprites.append(sprite)

    def on_draw(self):
        self.clear()
        self.tiles_batch.draw()
        self.objects_batch.draw()

    def update(self, dt):
        self.map.hero.update(1, self.map)
        removed = set()
        for sprite in self.objects_sprites:
            sprite.set_position(**self.coords_to_gl(sprite.game_object.x, sprite.game_object.y))
            if not sprite.game_object.active:
                if isinstance(sprite.game_object, Abomination):
                    blood = pyglet.sprite.Sprite(self.blood_animation, batch=self.objects_batch,
                                                 **self.coords_to_gl(sprite.game_object.x, sprite.game_object.y))
                    blood.color = COLORS['blood']
                removed.add(sprite)
        for sprite in removed:
            self.objects_sprites.remove(sprite)
            sprite.delete()
        removed.clear()


if __name__ == '__main__':
    window = Window(width=816, height=900)
    pyglet.app.run()
