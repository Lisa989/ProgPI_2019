#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame

from sys import exit
from os import environ

from costanti.color import *
from costanti.game_v2_pygame_costanti import get_row_column_center

MB_LEFT = 1
MB_RIGHT = 3

WINDOW_STYLE = pygame.HWSURFACE | pygame.DOUBLEBUF


class Window(object):
    def __init__(self, width, height, caption="MyWindow"):
        """
        Inizializza pygame, e crea la finestra con le dimensioni date
        :param width: larghezza finestra
        :param height: altezza finestra
        :param caption: titolo della finestra (default: MyWindow)
        """
        self.__done = False

        self.width = width
        self.height = height

        # posiziona la finestra sullo schermo in 5,35
        environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5, 35)

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height), WINDOW_STYLE)

        pygame.display.set_caption(caption)

        self.__clock = pygame.time.Clock()
        self.__fps = 60.0

        self.__backgroundColor = BLACK
        self.backgroundImage = None

    """
    --------------------------------------------------------------------------------------------------------------------
    *******************************************--FUNZIONI--**************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    @staticmethod
    def get_size():
        """
        :return: dimensione della finestra
        """
        return pygame.display.get_surface().get_size()

    @staticmethod
    def set_mouse_visible(status):
        """
        Setta il mouse visibile o no
        :param status: True visibile, False altrimenti
        :return:
        """
        pygame.mouse.set_visible(status)

    def set_background_color(self, colore):
        """
        setta il colore del background
        :param colore:
        :return:
        """
        self.__backgroundColor = colore

    def start_render(self):
        """
        pulisce lo schermo
        :return:
        """
        self.screen.fill(self.__backgroundColor)

    def text_to_screen(self, txt, font, riga, align, colore):
        """
        Disegna il testo sullo schermo
        :param txt: testo da disegnare
        :param font: pygame.font da utilizzare
        :param riga: riga in cui scrivere
        :param align: "center", "left", "life": parte dello schermo per cui calcolare le coordinate
        :param colore: colore del testo
        :return:
        """
        # trova le coordinare e disegna il testo
        center_x, center_y = get_row_column_center(riga, 1, align)
        txt = font.render(txt, True, colore)
        x = center_x - txt.get_width() // 2
        y = center_y - txt.get_height() // 2
        # x, y = get_point_to_draw(center_x, center_y, txt.get_width(), txt.get_height())
        self.screen.blit(txt, (x, y))

    """
    --------------------------------------------------------------------------------------------------------------------
    ***********************************************--RUN--**************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def run(self):
        """
        esegue il ciclo continuo di gioco: rivela gli eventi, aggiorna il gioco, disegna e aggiorna lo schermo
        :return:
        """

        while not self.__done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.on_exit()
                if event.type == pygame.MOUSEMOTION:
                    self.on_mouse_motion(event.pos[0], event.pos[1])
                if event.type == pygame.KEYDOWN:
                    self.on_key_press(event.key)
                if event.type == pygame.KEYUP:
                    self.on_key_release(event.key)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.on_mouse_release(event.pos[0], event.pos[1], event.button)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_press(event.pos[0], event.pos[1], event.button)
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict['size'], WINDOW_STYLE)
                    self.on_resize()

            self.on_update()
            self.on_draw()

            self.__clock.tick(self.__fps)

            pygame.display.flip()

    def on_resize(self):
        """
        funzione chiamata quando si verifica l'evento VIDEORESIZE
        :return:
        """
        pass

    def on_update(self):
        """
        funzione che aggiorna il gioco
        :return:
        """
        pass

    def on_draw(self):
        """
        funzione che disegna sullo schermo
        :return:
        """
        pass

    def on_mouse_motion(self, x, y):
        """
        funzione chiamata quando si verifica l'evento MOUSEMOTION
        :param x: coordinata x del mouse
        :param y: coordinata y del mouse
        :return:
        """
        pass

    def on_mouse_press(self, x, y, button):
        """
        funzione chiamata quando si verifica l'evento MOUSEBUTTONDOWN
        :param x: coordinata x del mouse
        :param y: coordinata y de mouse
        :param button: bottone premuto
        :return:
        """
        pass

    def on_mouse_release(self, x, y, button):
        """
        funzione chiamata quando si verifica l'evento MOUSEBUTTONUP
        :param x: coordinata x del mouse
        :param y: coordinata y de mouse
        :param button: bottone rilasciato
        :return:
        """
        pass

    def on_key_press(self, key):
        """
        funzione chiamata quando si verifica l'evento KEYDOWN
        :param key: tasto premuto
        :return:
        """
        pass

    def on_key_release(self, key):
        """
        funzione chiamata quando si verifica l'evento KEYUP
        :param key: tasto premuto
        :return:
        """
        pass

    def on_exit(self):
        """
        funzione che chiude pygame e termina la finestra
        :return:
        """
        self.__done = True
        pygame.quit()
        exit()
