from Game_v1_arcade.game_risorse import Immagini
from costanti.game_v1_arcade_costanti import *
import arcade


class Brick(arcade.Sprite):
    """
    Sprite Brick
    """
    def __init__(self, x, y, color):
        super().__init__(center_x=x, center_y=y)
        self.type = ID_NONE
        self.color = color
        self.dead = False
        self.hit = 1

        self.texture = Immagini.img_brick[self.color]
        self.width = Costanti.Brick_WIDTH
        self.height = Costanti.Brick_HEIGHT

    def on_scale(self, scale):
        """
        Scala le dimensioni in caso di cambio modalità fullscreen
        :param scale:
        :return:
        """
        self.center_y *= scale
        self.center_x *= scale
        self.width = Costanti.Brick_WIDTH
        self.height = Costanti.Brick_HEIGHT

    def on_collide(self):
        """
        Comportamento durante la collisione
        :return:
        """
        pass


class BrickSimple(Brick):
    """
    Sprite Brick simple (1 colpo)
    """
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = ID_SIMPLE

    def on_collide(self):
        self.hit -= 1
        if self.hit <= 0:
            self.dead = True
            # self.kill()
        return 100  # punti


class BrickDouble(Brick):
    """
    Sprite Brick double (2 colpi)
    """
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.type = ID_DOUBLE
        self.hit = 2

    def on_collide(self):
        self.hit -= 1
        if self.hit <= 0:
            self.dead = True
            # self.kill()
        if self.hit == 1:
            self.texture = Immagini.img_brick_break[self.color]
            self.width = Costanti.Brick_WIDTH
            self.height = Costanti.Brick_HEIGHT
        return 150  # punti


class BrickImmortal(Brick):
    """
    Sprite Brick immortal (infiniti colpi)
    """
    def __init__(self, x, y):
        super().__init__(x, y, 'grey')
        self.type = ID_IMMORTAL

    def on_collide(self):
        return 0
