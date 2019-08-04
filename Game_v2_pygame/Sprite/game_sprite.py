#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, w, h, *k):
        pygame.sprite.Sprite.__init__(self, *k)

        self.image = image

        self.center_x = 0
        self.center_y = 0
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

        self.rect = pygame.Rect(x, y, w, h)
        self.update_xy(x, y)

    # def draw(self, screen):
    #    screen.blit(self.image, (self.rect.x, self.rect.y))

    def update_xy(self, x, y):
        """
        Update the sprite.
        """
        self.rect.x = x
        self.rect.y = y
        self.center_x = self.rect.x + (self.rect.width / 2)
        self.center_y = self.rect.y + (self.rect.height / 2)
        self.left = self.rect.x
        self.right = self.rect.x + self.rect.width
        self.top = self.rect.y
        self.bottom = self.rect.y + self.rect.height


class AnimateGameSprite(GameSprite):
    def __init__(self, images, x, y, w, h, *k):
        GameSprite.__init__(self, None, x, y, w, h, *k)

        self.textures = images
        self.cur_texture_index = 0
        self.texture_change_frames = 5
        self.frame = 0
        self.can_cache = False

    def update_animation(self):
        """
               Logic for selecting the proper texture to use.
        """
        if self.frame % self.texture_change_frames == 0:
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
            self.image = self.textures[self.cur_texture_index]
            self.cur_texture_index = self.cur_texture_index
        self.frame += 1
