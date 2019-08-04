import pygame
from costanti.game_v1_arcade_costanti import *
from Editor_v1_pygame.editor_button import MyButton
from Editor_v1_pygame.editor_risorse import Risorse, WHITE


class ToolBar(object):
    def __init__(self, y=40):
        width = WINDOW_WIDTH / 4 - Costanti.EDGE_INFO["size"]

        self.title = Risorse.title_font2.render("EDITOR", 1, WHITE)
        self.title_pos = ((width - self.title.get_rect().width) / 2, y)

        # type of brick
        dy = Risorse.button_yellow.get_rect().height + 10
        x = (width - Risorse.button_yellow.get_rect().width) / 2
        y += self.title.get_rect().height + 30
        self.text_type = Risorse.title_font3.render("Tipo di brick", 1, WHITE)
        self.text_type_pos = ((width - self.text_type.get_rect().width) / 2, y)
        y += self.text_type.get_rect().height + 10
        self.buttons_type = {
            "type_simple": MyButton(Risorse.button_yellow, x, y, "SIMPLE"),
            "type_double": MyButton(Risorse.button_yellow, x, y + dy, "DOUBLE"),
            "type_immortal": MyButton(Risorse.button_yellow, x, y + dy * 2, "IMMORTAL")
        }

        # selezione type symple
        self.selected_type = "type_simple"
        self.buttons_type[self.selected_type].selected = True

        # color of brick
        y += dy * 3 + 30
        dx = Risorse.bricks_color_size[0] + 12
        dy = Risorse.bricks_color_size[1] + 12
        x = (width - (dx * 3 - 12)) / 2

        self.selected_color = None

        self.text_color = Risorse.title_font3.render("Colore", 1, WHITE)
        self.text_color_pos = ((width - self.text_color.get_rect().width) / 2, y)

        y += self.text_color.get_rect().height + 20
        self.buttons_color = {
            'blue': MyButton(Risorse.bricks_color[ID_BLUE], x, y, ""),
            'light_green': MyButton(Risorse.bricks_color[ID_GREEN], x + dx, y, ""),
            'pink': MyButton(Risorse.bricks_color[ID_PURPLE], x + dx * 2, y, ""),

            "red": MyButton(Risorse.bricks_color[ID_RED], x, y + dy, ""),
            "orange": MyButton(Risorse.bricks_color[ID_ORANGE], x + dx, y + dy, ""),
            "light_blue": MyButton(Risorse.bricks_color[ID_LIGHT_BLUE], x + dx * 2, y + dy, ""),

            "yellow": MyButton(Risorse.bricks_color[ID_YELLOW], x, y + dy * 2, ""),
            "green": MyButton(Risorse.bricks_color[ID_DARK_GREEN], x + dx, y + dy * 2, ""),
            "brown": MyButton(Risorse.bricks_color[ID_BROWN], x + dx * 2, y + dy * 2, "")
        }

        # seleziona un colore iniziale
        self.selected_color = "blue"
        self.buttons_color[self.selected_color].selected = True

        # tool bt
        #x = (width - Risorse.button_orange.get_rect().width) / 2
        #y += Risorse.bricks_color["blue"].get_rect().height + dy * 2 + 40
        x = WINDOW_WIDTH - width
        y = 50
        dy = Risorse.button_orange.get_rect().height + 10
        self.bt_tool = {
            "load": MyButton(Risorse.button_orange, x, y, "LOAD"),
            "save": MyButton(Risorse.button_orange, x, y + dy, "SAVE"),
            "clear": MyButton(Risorse.button_orange, x, y + dy * 2, "CLEAR"),
            "exit": MyButton(Risorse.button_orange, x, y + dy * 3, "EXIT")
        }

    def handle_input_color(self, mouse_pos):
        for k in self.buttons_color.keys():
            if self.buttons_color[k].is_clicked(mouse_pos):
                if k == self.selected_color:
                    self.selected_color = None
                else:
                    for k1 in self.buttons_color.keys():
                        if not (k1 == k):
                            self.buttons_color[k1].selected = False
                    self.selected_color = k

    def handle_input_type(self, mouse_pos):  # type
        for k in self.buttons_type.keys():
            if self.buttons_type[k].is_clicked(mouse_pos):
                for k1 in self.buttons_type.keys():
                    if not (k1 == k):
                        self.buttons_type[k1].selected = False
                self.selected_type = k

    def handle_input_tool(self,mouse_pos):
        for bt in self.bt_tool.values():
            bt.is_clicked(mouse_pos)

    def draw(self, win):  # type
        win.blit(self.title, self.title_pos)

        win.blit(self.text_type, self.text_type_pos)
        for b in self.buttons_type.values():
            b.draw(win)

        win.blit(self.text_color, self.text_color_pos)
        for b in self.buttons_color.values():
            if b.selected:
                pygame.draw.rect(win, WHITE, (b.x, b.y, b.bt_rect.width, b.bt_rect.height), 2)
            b.draw(win)

        for b in self.bt_tool.values():
            b.draw(win)
