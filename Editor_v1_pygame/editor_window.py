import pygame
from pygame.locals import *
from sys import exit
from os import environ

MB_LEFT = 1
MB_RIGHT = 3

WINDOW_STYLE = HWSURFACE | DOUBLEBUF | FULLSCREEN


class Window(object):
    def __init__(self, width, height, caption="MyWindow"):
        """
        Inizializza pygame, e crea la finestra con le dimensioni date
        :param width: larghezza finestra
        :param height: altezza finestra
        :param caption: titolo della finestra (default: MyWindow)
        """
        self.width = width
        self.height = height

        # posiziona la finestra sullo schermo in 5,35
        environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (5, 35)

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height), WINDOW_STYLE)

        pygame.display.set_caption(caption)

    def run(self):
        """
        esegue il ciclo continuo di gioco: rivela gli eventi, aggiorna il gioco, disegna e aggiorna lo schermo
        :return:
        """
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.on_exit()
                if event.type == pygame.MOUSEMOTION:
                    self.on_mouse_motion(event.pos[0], event.pos[1])
                if event.type == pygame.KEYDOWN:
                    self.on_key_press(pygame.key.get_pressed())
                if event.type == pygame.KEYUP:
                    self.on_key_release(pygame.key.get_pressed())
                if event.type == pygame.MOUSEBUTTONUP:
                    self.on_mouse_release(event.pos[0], event.pos[1], event.button)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_press(event.pos[0], event.pos[1], event.button)
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.dict['size'], WINDOW_STYLE)
                    self.on_resize()

            self.on_update()
            self.on_draw()

            pygame.display.flip()

            clock.tick(35000)

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

    def on_mouse_motion(self, x: float, y: float):
        """
        funzione chiamata quando si verifica l'evento MOUSEMOTION
        :param x: coordinata x del mouse
        :param y: coordinata y del mouse
        :return:
        """
        pass

    def on_mouse_press(self, x: float, y: float, button: int):
        """
        funzione chiamata quando si verifica l'evento MOUSEBUTTONDOWN
        :param x: coordinata x del mouse
        :param y: coordinata y de mouse
        :param button: bottone premuto
        :return:
        """
        pass

    def on_mouse_release(self, x: float, y: float, button: int):
        """
        funzione chiamata quando si verifica l'evento MOUSEBUTTONUP
        :param x: coordinata x del mouse
        :param y: coordinata y de mouse
        :param button: bottone rilasciato
        :return:
        """
        pass

    def on_key_press(self, keys: []):
        """
        funzione chiamata quando si verifica l'evento KEYDOWN
        :param keys: array dei tasti premuti
        :return:
        """
        pass

    def on_key_release(self, keys: []):
        """ funzione chiamata quando si verifica l'evento KEYUP """
        pass

    def on_exit(self):
        """ funzione che chiude pygame e termina la finestra """
        pygame.quit()
        exit(0)
