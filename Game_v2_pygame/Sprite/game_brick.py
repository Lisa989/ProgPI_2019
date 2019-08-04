#!/usr/bin/python
# -*- coding: utf-8 -*-

from Game_v2_pygame.game_risorse import Immagini
from costanti.game_v2_pygame_costanti import *
from Game_v2_pygame.Sprite.game_sprite import GameSprite


class Brick(GameSprite):
    def __init__(self, x, y, color, *k):
        GameSprite.__init__(self, Immagini.img_brick[color], x, y, BRICK_WIDTH, BRICK_HEIGHT, *k)

        self.type = ID_NONE
        self.color = color
        self.dead = False
        self.hit = 1

    def on_collide(self):
        pass


class BrickSimple(Brick):
    def __init__(self, x, y, color, *k):
        Brick.__init__(self, x, y, color, *k)
        self.type = ID_SIMPLE

    def on_collide(self):
        self.hit -= 1
        if self.hit <= 0:
            self.dead = True
            # self.kill()
        return 100  # punti


class BrickDouble(Brick):
    def __init__(self, x, y, color, *k):
        Brick.__init__(self, x, y, color, *k)
        self.type = ID_DOUBLE
        self.hit = 2

    def on_collide(self):
        self.hit -= 1
        if self.hit <= 0:
            self.dead = True
            # self.kill()
        if self.hit == 1:
            self.image = Immagini.img_brick_break[self.color]
            self.rect.width = BRICK_WIDTH
            self.rect.height = BRICK_HEIGHT
        return 150  # punti


class BrickImmortal(Brick):
    def __init__(self, x, y, *k):
        Brick.__init__(self, x, y, ID_GREY, *k)
        self.type = ID_IMMORTAL
        self.hit = 10000

    def on_collide(self):
        return 0
