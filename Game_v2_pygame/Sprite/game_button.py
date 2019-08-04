#!/usr/bin/python
# -*- coding: utf-8 -*-

from costanti.game_v2_pygame_costanti import *
from costanti.color import BLACK
from Game_v2_pygame.game_risorse import MyFont
from Game_v2_pygame.game_risorse import Immagini
from Game_v2_pygame.Sprite.game_sprite import GameSprite


class TextButton(GameSprite):
    """ Text-based button """

    def __init__(self, x, y, text, action_function, bt_id):
        GameSprite.__init__(self, None, x, y, BUTTON_WIDTH, BUTTON_HEIGHT)

        self.text = text
        self.bt_id = bt_id
        self.action_function = action_function

        self.img_button = Immagini.img_button_yellow
        self.img_button_press = Immagini.img_button_orange

        self.pressed = False

    def draw(self, screen):
        if not self.pressed:
            screen.blit(self.img_button, (self.rect.x, self.rect.y))
            self.text_to_screen(screen, self.text, MyFont.font20, self.center_x, self.center_y, BLACK)
        else:
            screen.blit(self.img_button_press, (self.rect.x, self.rect.y))
            self.text_to_screen(screen, self.text, MyFont.font20, self.center_x + 2, self.center_y + 2, BLACK)

    @staticmethod
    def text_to_screen(screen, txt, font, center_x, center_y, colore):
        text = font.render(txt, True, colore)
        x = center_x - text.get_width() // 2
        y = center_y - text.get_height() // 2
        screen.blit(text, (x, y))

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False
        if self.bt_id == 0:
            self.action_function()
        else:
            self.action_function(self.bt_id)


class Button(TextButton):
    def __init__(self, row, column, text, action_function, bt_id=0):
        center_x, center_y = get_row_column_center(row, column)
        x, y = center_x - BUTTON_WIDTH / 2, center_y - BUTTON_HEIGHT / 2
        TextButton.__init__(self, x, y, text, action_function, bt_id)

    @staticmethod
    def check_mouse_press_for_buttons(x, y, button_list):
        """ Given an x, y, see if we need to register any button clicks. """
        for button in button_list:
            if button.rect.collidepoint(x, y):
                button.on_press()

    @staticmethod
    def check_mouse_release_for_buttons(x, y, button_list):
        """ If a mouse button has been released, see if we need to process
            any release events. """
        for button in button_list:
            if button.pressed and button.rect.collidepoint(x, y):
                button.on_release()
