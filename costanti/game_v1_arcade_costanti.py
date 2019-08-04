from costanti.costanti import *

# dimensioni not fullscreen
WINDOW_WIDTH = DISPLAY_WIDTH - 100
WINDOW_HEIGHT = DISPLAY_HEIGHT - 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Costanti:
    __screen_width = 0
    __screen_height = 0
    __edge_size = 0

    to_full_screen = 0
    to_not_full_screen = 0

    LEVEL_INFO = dict(width=0, height=0, left=0, top=0, right=0, bottom=0, paddle_area_height=0)
    EDGE_INFO = dict(size=0, left=(0, 0, 0, 0), right=(0, 0, 0, 0), top=(0, 0, 0, 0))

    Brick_WIDTH = 0
    Brick_HEIGHT = 0

    Paddle_WIDTH = 0
    Paddle_HEIGHT = 0

    Ball_RADIUS = 0

    Button_WIDTH = 0
    Button_HEIGHT = 0

    PT_FONT = dict(title=0, title2=0, text=0, text2=0)

    NEXT_ROW = 0
    NEXT_COLUMN = 0

    LIFE_X_START_DRAW = 0
    BALL_LIFE_SIZE = 0

    MAX_LEVEL = 0

    @staticmethod
    def init():
        Costanti.__screen_width = DISPLAY_WIDTH
        Costanti.__screen_height = DISPLAY_HEIGHT
        Costanti.__edge_size = 22

        Costanti.to_full_screen = Costanti.__screen_height / WINDOW_HEIGHT
        Costanti.to_not_full_screen = WINDOW_HEIGHT / Costanti.__screen_height

        Costanti.LEVEL_INFO = dict(
            width=Costanti.__screen_width // 2,
            height=Costanti.__screen_height - Costanti.__edge_size,
            left=Costanti.__screen_width // 4,
            top=Costanti.__screen_height - Costanti.__edge_size,
            right=3 * Costanti.__screen_width // 4,
            bottom=80,
            paddle_area_height=350
        )

        Costanti.EDGE_INFO = dict(
            size=Costanti.__edge_size,
            left=(
                Costanti.LEVEL_INFO['left'] - Costanti.__edge_size // 2,
                Costanti.__screen_height // 2,
                Costanti.__edge_size,
                Costanti.__screen_height
                ),
            right=(
                3 * Costanti.__screen_width // 4 + Costanti.__edge_size // 2,
                Costanti.__screen_height // 2,
                Costanti.__edge_size,
                Costanti.__screen_height
                ),
            top=(
                Costanti.__screen_width // 2,
                Costanti.__screen_height - Costanti.__edge_size // 2,
                Costanti.__screen_width // 2,
                Costanti.__edge_size

            )
        )

        Costanti.Brick_WIDTH = (Costanti.LEVEL_INFO['width'] - 1) / MAX_CLN
        Costanti.Brick_HEIGHT = (Costanti.LEVEL_INFO['height'] -
                                 Costanti.LEVEL_INFO['paddle_area_height']) / MAX_ROW

        Costanti.Paddle_WIDTH = 97
        Costanti.Paddle_HEIGHT = 25.6

        Costanti.Ball_RADIUS = 8

        Costanti.NEXT_ROW = Costanti.LEVEL_INFO['height'] / 10
        Costanti.NEXT_COLUMN = Costanti.LEVEL_INFO['width'] / 3

        Costanti.Button_WIDTH = Costanti.NEXT_COLUMN - 40
        Costanti.Button_HEIGHT = Costanti.NEXT_ROW - 40

        Costanti.PT_FONT = dict(title=60, title2=50, text=40, text2=20)
        Costanti.LIFE_X_START_DRAW = Costanti.LEVEL_INFO['width'] / 5
        Costanti.BALL_LIFE_SIZE = 30

        Costanti.MAX_LEVEL = N_LEVELS

    @staticmethod
    def get_row_column_center(row, column=1, align="center"):
        if align == 'life':
            center_x = Costanti.LIFE_X_START_DRAW
        elif align == "right":
            center_x = 3 * Costanti.LEVEL_INFO['width'] / 4
        elif align == "left":
            center_x = Costanti.LEVEL_INFO['width'] / 4
        else:  # center
            center_x = (Costanti.LEVEL_INFO['left'] + Costanti.NEXT_COLUMN / 2) + Costanti.NEXT_COLUMN * column

        center_y = (Costanti.LEVEL_INFO['top'] - Costanti.NEXT_ROW / 2) - Costanti.NEXT_ROW * row

        return center_x, center_y

    @staticmethod
    def on_scale(fullscreen):
        if fullscreen:
            scale = Costanti.to_full_screen
        else:
            scale = Costanti.to_not_full_screen

        Costanti.__edge_size *= scale
        Costanti.__screen_width *= scale
        Costanti.__screen_height *= scale

        Costanti.LEVEL_INFO = dict(
            width=Costanti.__screen_width // 2,
            height=Costanti.__screen_height - Costanti.__edge_size,
            left=Costanti.__screen_width // 4,
            top=Costanti.__screen_height - Costanti.__edge_size,
            right=3 * Costanti.__screen_width // 4,
            bottom=Costanti.LEVEL_INFO['bottom']*scale,
            paddle_area_height=Costanti.LEVEL_INFO['paddle_area_height']*scale
        )

        Costanti.EDGE_INFO = dict(
            size=Costanti.__edge_size,
            left=(
                Costanti.LEVEL_INFO['left'] - Costanti.__edge_size // 2,
                Costanti.__screen_height // 2,
                Costanti.__edge_size,
                Costanti.__screen_height
            ),
            right=(
                3 * Costanti.__screen_width // 4 + Costanti.__edge_size // 2,
                Costanti.__screen_height // 2,
                Costanti.__edge_size,
                Costanti.__screen_height
            ),
            top=(
                Costanti.__screen_width // 2,
                Costanti.__screen_height - Costanti.__edge_size // 2,
                Costanti.__screen_width // 2,
                Costanti.__edge_size

            )
        )

        Costanti.Brick_WIDTH = (Costanti.LEVEL_INFO['width'] - 1) / MAX_CLN
        Costanti.Brick_HEIGHT = (Costanti.LEVEL_INFO['height'] -
                                 Costanti.LEVEL_INFO['paddle_area_height']) / MAX_ROW

        Costanti.Paddle_WIDTH *= scale
        Costanti.Paddle_HEIGHT *= scale

        Costanti.Ball_RADIUS *= scale

        Costanti.PT_FONT['title'] *= scale
        Costanti.PT_FONT['title2'] *= scale
        Costanti.PT_FONT['text'] *= scale
        Costanti.PT_FONT['text2'] *= scale

        Costanti.NEXT_ROW = Costanti.LEVEL_INFO['height'] / 10
        Costanti.NEXT_COLUMN = Costanti.LEVEL_INFO['width'] / 3

        Costanti.Button_WIDTH = Costanti.NEXT_COLUMN - 40
        Costanti.Button_HEIGHT = Costanti.NEXT_ROW - 40

        Costanti.LIFE_X_START_DRAW *= scale
        Costanti.BALL_LIFE_SIZE *= scale

    @staticmethod
    def get_point_to_draw(cx, cy, w, h):
        """
        Funzione per calcolare i punti da disegnare in pygame,
        essendo le costanti calcolate per la libreria arcade
        :param cx:
        :param cy:
        :param w:
        :param h:
        :return: x, y
        """
        x = cx - (w / 2)
        y = Costanti.__screen_height - cy - (h / 2)
        return x, y
