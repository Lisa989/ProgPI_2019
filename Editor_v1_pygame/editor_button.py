from Editor_v1_pygame.editor_risorse import Risorse
from costanti.color import BLACK
import pygame


class MyButton(object):
    def __init__(self, img, x, y, text):
        self.img = img
        self.bt_rect = self.img.get_rect()
        self.x = x
        self.y = y

        self.selected = False

        if not text == "":
            self.text = Risorse.button_font.render(text, 1, BLACK)
            text_rect = self.text.get_rect()
            self.text_pos = (self.x + (self.bt_rect.width - text_rect.width) / 2, self.y + (self.bt_rect.height - text_rect.height) / 2)
        else:
            self.text = None

        self.overlay = pygame.Surface((self.bt_rect.width, self.bt_rect.height))
        self.overlay.set_alpha(128)
        self.overlay.fill(BLACK)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
        if self.text is not None:
            win.blit(self.text, self.text_pos)
        if self.selected:
            win.blit(self.overlay, (self.x, self.y))

    def is_clicked(self, mouse_position):
        click = self.x < mouse_position[0] < self.x + self.bt_rect.width and \
                self.y < mouse_position[1] < self.y + self.bt_rect.height
        if click:
                self.selected = not self.selected

        return click
