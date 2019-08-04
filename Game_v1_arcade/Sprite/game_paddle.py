import arcade
from costanti.game_v1_arcade_costanti import *
from Game_v1_arcade.game_risorse import Immagini


class Paddle(arcade.AnimatedTimeSprite):
    """
    Sprite Paddle: AnimatedTimeSprite
    """
    def __init__(self):
        super().__init__(center_x=Costanti.LEVEL_INFO['width'], center_y=Costanti.LEVEL_INFO['bottom'] - Costanti.Paddle_HEIGHT // 2)
        self.width = Costanti.Paddle_WIDTH
        self.height = Costanti.Paddle_HEIGHT
        self.textures = Immagini.img_paddle

        self.change_x = 0
        self.speed = 5

    def on_scale(self, scale):
        """
        Scala le dimensioni il caso di cambio modalità fullscreen
        :param scale:
        :return:
        """
        self.center_x *= scale
        self.center_y *= scale
        self.change_x *= scale
        self.change_y *= scale
        self.speed *= scale
        self.width = Costanti.Paddle_WIDTH
        self.height = Costanti.Paddle_HEIGHT

    def update(self):
        """
        Aggiorna i movimenti del paddle
        :return:
        """
        if self.change_x < 0 and self.left - self.speed <= Costanti.LEVEL_INFO['left']:
            # raggiunto limite sinistro
            self.left = Costanti.LEVEL_INFO['left'] + 1
        elif self.change_x > 0 and Costanti.LEVEL_INFO['right'] <= self.right + self.speed:
            # raggiunto limite destro
            self.right = Costanti.LEVEL_INFO["right"] - 1
        elif self.left > Costanti.LEVEL_INFO["left"] and self.right < Costanti.LEVEL_INFO["right"]:
            # sposta il paddle
            self.center_x += self.change_x * self.speed

        # aggiorno l'immagine per l'animazione
        super().update_animation()

        # ristabilisco le giuste dimensioni del paddle e non quelle dell'immagine originale
        self.width = Costanti.Paddle_WIDTH
        self.height = Costanti.Paddle_HEIGHT
