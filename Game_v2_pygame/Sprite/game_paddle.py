#!/usr/bin/python
# -*- coding: utf-8 -*-

from costanti.game_v2_pygame_costanti import *
from Game_v2_pygame.game_risorse import Immagini
from Game_v2_pygame.Sprite.game_sprite import AnimateGameSprite


class Paddle(AnimateGameSprite):
    def __init__(self, *k):
        self.start_x = SCREEN_LEVEL_WIDTH - PADDLE_WIDTH // 2
        self.start_y = AREA_PADDLE_BOTTOM
        AnimateGameSprite.__init__(self, Immagini.img_paddle, self.start_x, self.start_y, PADDLE_WIDTH, PADDLE_HEIGHT, *k)

        self.change_x = 0
        self.speed_x = 5

    def restart_paddle(self):
        self.change_x = 0
        self.rect.x = self.start_x

    def update(self):
        if self.change_x < 0 and self.left - self.speed_x <= SCREEN_LEVEL_LEFT:
            # oltre sinistra
            self.update_xy(SCREEN_LEVEL_LEFT + 1, self.rect.y)
        elif self.change_x > 0 and SCREEN_LEVEL_RIGHT <= self.right + self.speed_x:
            # oltre destra
            self.update_xy(SCREEN_LEVEL_RIGHT - 1 - PADDLE_WIDTH, self.rect.y)
        elif self.left > SCREEN_LEVEL_LEFT and self.right < SCREEN_LEVEL_RIGHT:
            # sposta
            self.update_xy(self.rect.x + self.change_x * self.speed_x, self.rect.y)

        # aggiorna immagine
        self.update_animation()
