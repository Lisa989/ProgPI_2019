from costanti.costanti import *
# dimensioni della finestra calcolate a seconda dello schermo
WINDOW_WIDTH = DISPLAY_WIDTH - 80
WINDOW_HEIGHT = DISPLAY_HEIGHT - 80

EDGE_SIZE = 25

AREA_PADDLE_BOTTOM = WINDOW_HEIGHT - 80


BRICK_WIDTH = 55  # int(SCREEN_LEVEL_WIDTH / MAX_CLN)
BRICK_HEIGHT = 21  # int((SCREEN_LEVEL_HEIGHT - AREA_PADDLE_HEIGHT) / MAX_ROW)

__AREA_BRICK_HEIGHT = BRICK_HEIGHT * MAX_ROW

AREA_PADDLE_HEIGHT = WINDOW_HEIGHT - __AREA_BRICK_HEIGHT  # 350

SCREEN_LEVEL_WIDTH = BRICK_WIDTH * MAX_CLN  # int(WINDOW_WIDTH / 2)
SCREEN_LEVEL_HEIGHT = __AREA_BRICK_HEIGHT + AREA_PADDLE_HEIGHT  # WINDOW_HEIGHT - EDGE_SIZE

SCREEN_LEVEL_LEFT = int(WINDOW_WIDTH / 4)
SCREEN_LEVEL_RIGHT = SCREEN_LEVEL_LEFT + SCREEN_LEVEL_WIDTH
SCREEN_LEVEL_TOP = EDGE_SIZE
SCREEN_LEVEL_BOTTOM = WINDOW_HEIGHT


# EDGE_POINT_TO_DRAW = x, y
EDGE_H_WIDTH = SCREEN_LEVEL_WIDTH
EDGE_V_HEIGHT = WINDOW_HEIGHT
EDGE_LEFT = (SCREEN_LEVEL_LEFT - EDGE_SIZE, 0)
EDGE_RIGHT = (SCREEN_LEVEL_RIGHT, 0)
EDGE_TOP = (SCREEN_LEVEL_LEFT, 0)

# BRICK_WIDTH = int(SCREEN_LEVEL_WIDTH / MAX_CLN)
# BRICK_HEIGHT = int((SCREEN_LEVEL_HEIGHT - AREA_PADDLE_HEIGHT) / MAX_ROW)

PADDLE_WIDTH = 98
PADDLE_HEIGHT = 25

BALL_RADIUS = 8

NEXT_ROW = int(SCREEN_LEVEL_HEIGHT / 10)
NEXT_COLUMN = int(SCREEN_LEVEL_WIDTH / 3)

BUTTON_WIDTH = NEXT_COLUMN - 40
BUTTON_HEIGHT = NEXT_ROW - 40

LIFE_SIZE = 50
LIFE_X_START_DRAW = int(SCREEN_LEVEL_LEFT / 2 - LIFE_SIZE)

MAX_LEVEL = N_LEVELS


def get_row_column_center(row, column=1, align="center"):
        """
        Calcola il punto centrale di riga e colonna a partire dall'alto
        :param row: riga
        :param column: colonna
        :param align: allineamento 'life', "right", "left", "center"
        :return: coordinate centrali di dove disegnare
        """
        if align == 'life':
            center_x = LIFE_X_START_DRAW
        elif align == "right":
            center_x = 3 * SCREEN_LEVEL_WIDTH // 4
        elif align == "left":
            center_x = SCREEN_LEVEL_WIDTH // 4
        else:  # center
            center_x = (SCREEN_LEVEL_LEFT + NEXT_COLUMN // 2) + NEXT_COLUMN * column

        center_y = (SCREEN_LEVEL_TOP + NEXT_ROW // 2) + NEXT_ROW * row

        return center_x, center_y


def limit_delta(d):
    if d > 0.8:
        d = 0.8
    elif d < -0.8:
        d = -0.8
    elif 0 < d < 0.2:
        d = 0.2
    elif -0.2 < d < 0:
        d = -0.2
    return d
