from costanti.game_v2_pygame_costanti import *
from Game_v2_pygame.game_risorse import Immagini
from Game_v2_pygame.Sprite.game_sprite import GameSprite


class Ball(GameSprite):
    """
    Ball Sprite
    """

    def __init__(self, *k):

        self.start_x = WINDOW_WIDTH / 2 - BALL_RADIUS
        self.start_y = AREA_PADDLE_BOTTOM - BALL_RADIUS * 2 - 1
        GameSprite.__init__(self, Immagini.img_ball, self.start_x, self.start_y, BALL_RADIUS * 2, BALL_RADIUS * 2, *k)

        self.ancorata = True

        self.speed_x = self.speed_y = 6

        self.change_x = 0
        self.change_y = 0

    def update(self):
        x, y = self.rect.x, self.rect.y

        if self.left <= SCREEN_LEVEL_LEFT:
            if DEBUG:
                print(
                    "ball edge prima", "(dx,dy): (", self.change_x, ",", self.change_y, "), (x,Y): (", self.rect.x, ",",
                    self.rect.y, ")")
            self.change_x = limit_delta(- self.change_x)
            x = SCREEN_LEVEL_LEFT + 1

        if self.right >= SCREEN_LEVEL_RIGHT:
            self.change_x = limit_delta(- self.change_x)
            x = SCREEN_LEVEL_RIGHT - BALL_RADIUS * 2 - 1

        if self.top <= SCREEN_LEVEL_TOP:
            self.change_y = limit_delta(- self.change_y)
            y = SCREEN_LEVEL_TOP + 1

        x, y = int(x + self.change_x * self.speed_x), int(y + self.change_y * self.speed_y)
        self.update_xy(x, y)

        if DEBUG:
            print("ball edge dopo", "(dx,dy): (", self.change_x, ",", self.change_y,
                  "), (x,Y): (", self.rect.x, ",", self.rect.y, ")")

    def start(self):
        self.change_x = 0
        self.change_y = -1
        self.ancorata = False

    def stop(self):
        self.ancorata = True
        self.update_xy(self.start_x, self.start_y)
        self.change_x = 0
        self.change_y = 0
