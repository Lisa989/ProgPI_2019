from costanti.game_v1_arcade_costanti import Costanti
from Game_v1_arcade.game_risorse import Immagini
import arcade


class Ball(arcade.Sprite):
    """
    Sprite Ball
    """

    def __init__(self, x, y):
        super().__init__(center_x=x, center_y=(y + Costanti.Ball_RADIUS + 1))
        self.ancorata = True
        self.texture = Immagini.img_ball
        self.width = Costanti.Ball_RADIUS * 2
        self.height = Costanti.Ball_RADIUS * 2
        self.speed = 6

    def update(self):
        """
        Aggiorna i movimenti della pallina
        :return:
        """
        self.center_x += self.change_x * self.speed
        self.center_y += self.change_y * self.speed

        # sorpassato limite sinistro
        if self.left <= Costanti.LEVEL_INFO['left']:
            self.change_x *= -1
            self.left = Costanti.LEVEL_INFO['left'] + 1

        # sorpassato limite destro
        if self.right >= Costanti.LEVEL_INFO['right']:
            self.change_x *= -1
            self.right = Costanti.LEVEL_INFO['right'] - 1

        # sorpassato limite superiore
        if self.top >= Costanti.LEVEL_INFO['top']:
            self.change_y *= -1
            self.top = Costanti.LEVEL_INFO['top'] - 1

    def on_scale(self, scale):
        """
        Scala le dimensioni in caso di cambio modalità fullscreen
        :param scale:
        :return:
        """
        self.speed *= scale
        self.width *= scale
        self.height *= scale
        self.center_x *= scale
        if self.ancorata:
            self.center_y = Costanti.LEVEL_INFO['bottom'] + Costanti.Ball_RADIUS + 1
        else:
            self.center_y *= scale
        self.change_x *= scale
        self.change_y *= scale

    def start(self):
        """
        Fai partire l apallina
        :return:
        """
        self.change_x = 0
        self.change_y = 1
        self.ancorata = False

    def stop(self):
        """
        Ferma la pallina
        :return:
        """
        self.ancorata = True
        self.center_y = Costanti.LEVEL_INFO['bottom'] + Costanti.Ball_RADIUS + 1
        self.change_x = 0
        self.change_y = 0
