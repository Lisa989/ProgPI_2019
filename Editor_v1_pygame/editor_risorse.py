from costanti.game_v1_arcade_costanti import *
from costanti.images_names import *
from pygame import font, image, transform


class Risorse(object):
    background = None
    borderH = None
    borderV = None

    menu_font = None
    title_font3 = None
    title_font1 = None
    title_font2 = None
    button_font = None

    button_orange = None
    button_yellow = None

    bricks = dict()
    bricks_break = dict()
    bricks_color = dict()

    menu_button_size = (200, 30)
    bricks_color_size = (50, 50)

    @classmethod
    def load(cls):
        # font
        cls.menu_font = font.SysFont('goudy stout', 50)
        cls.title_font3 = font.SysFont('arial rounded', 20)
        cls.title_font2 = font.SysFont('algerian', 40)
        cls.title_font1 = font.SysFont('goudy stout', 60)
        cls.button_font = font.SysFont('verdana', 12, True)

        # button
        cls.button_orange = image.load(img_button_orange)
        cls.button_yellow = image.load(img_button_yellow)
        cls.button_orange = transform.scale(cls.button_orange, cls.menu_button_size)
        cls.button_yellow = transform.scale(cls.button_yellow, cls.menu_button_size)
        cls.button_yellow.set_colorkey(WHITE)
        cls.button_orange.set_colorkey(WHITE)

        # background
        size = (int(Costanti.LEVEL_INFO["width"]), int(Costanti.LEVEL_INFO["height"]))
        cls.background = image.load(img_background_0)
        cls.background = transform.scale(cls.background, size)

        border = image.load(img_edge)
        size = int(Costanti.EDGE_INFO["size"])
        height = int(Costanti.LEVEL_INFO["height"] + Costanti.EDGE_INFO["size"])
        width = int(Costanti.LEVEL_INFO["width"])
        cls.borderV = transform.scale(border, (size, height))
        border = transform.rotate(border, 90)
        cls.borderH = transform.scale(border, (width, size))

        # Bricks
        brick_size = int(Costanti.Brick_WIDTH), int(Costanti.Brick_HEIGHT)
        color_size = (Risorse.bricks_color_size[0],Risorse.bricks_color_size[1])
        for color in colors:
            cls.bricks[color] = image.load(img_bricks[color])
            cls.bricks[color] = transform.scale(cls.bricks[color], brick_size)

            cls.bricks_break[color] = image.load(img_bricks_break[color])
            cls.bricks_break[color] = transform.scale(cls.bricks_break[color], brick_size)

            cls.bricks_color[color] = image.load(img_brick_colors[color])
            cls.bricks_color[color] = transform.scale(cls.bricks_color[color], color_size)

        cls.bricks['grey'] = image.load(img_bricks['grey'])
        cls.bricks['grey'] = transform.scale(cls.bricks['grey'], brick_size)

