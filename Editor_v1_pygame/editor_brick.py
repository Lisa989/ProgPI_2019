from Editor_v1_pygame.editor_risorse import Risorse
import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.type = 'type'
        self.color = color
        self.img = Risorse.bricks[color]
        self.img_break = None
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, win):
        if self.type == "type_double":
            win.blit(self.img_break,(self.rect.x, self.rect.y))
        else:
            win.blit(self.img, (self.rect.x, self.rect.y))

    def draw_alpha(self, win, x, y):
        if self.type == "type_double":
            win.blit(self.img_break, (x, y))
        else:
            win.blit(self.img, (x, y))


class BrickSimple(Brick):
    def __init__(self, x, y, color):
        super(BrickSimple, self).__init__(x, y, color)
        self.type = 'type_simple'


class BrickDouble(Brick):
    def __init__(self, x, y, color):
        super(BrickDouble, self).__init__(x, y, color)
        self.type = 'type_double'
        self.img_break = Risorse.bricks_break[color]


class BrickImmortal(Brick):
    def __init__(self, x, y):
        super(BrickImmortal, self).__init__(x, y, 'grey')
        self.type = 'type_immortal'






