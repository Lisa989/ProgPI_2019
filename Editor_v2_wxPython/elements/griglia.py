from costanti.editor_v2_wxPython_costanti import *


class Griglia:
    X = SCREEN_LEVEL_X
    Y = SCREEN_LEVEL_Y
    WIDTH = SCREEN_LEVEL_WIDTH
    HEIGTH = SCREEN_LEVEL_HEIGHT - AREA_PADDLE
    RIGHT = EDGE_RIGHT[0]
    BOTTOM = EDGE_SIZE + (SCREEN_LEVEL_HEIGHT - AREA_PADDLE)

    @staticmethod
    def is_on_grid(mouse_pos):
        return BRICK_GRID['x'] < mouse_pos[0] < BRICK_GRID['right'] \
               and BRICK_GRID['y'] < mouse_pos[1] < BRICK_GRID['bottom']

    @staticmethod
    def get_xy_from_row_column(row, column):
        """
        :param row:
        :param column:
        :return: x, y della casella
        """
        x_screen = BRICK_GRID['x'] + BRICK_WIDTH * column
        y_screen = BRICK_GRID['y'] + BRICK_HEIGHT * row
        return x_screen, y_screen

    @staticmethod
    def get_row_column_from_mouse(mouse_pos):
        """
        :return: row, column della casella su cui si trova il mouse
        """
        x, y = mouse_pos[0] - BRICK_GRID['x'], mouse_pos[1] - BRICK_GRID['y']

        column = int(x // BRICK_WIDTH)
        row = int(y // BRICK_HEIGHT)

        return row, column

    @staticmethod
    def get_index_from_row_column(row, column):
        """
        :param row:
        :param column:
        :return: indice dell'array
        """
        return (column - 1) + MAX_CLN * (row - 1)

    @classmethod
    def get_xy_from_mouse(cls, mouse_pos):
        """
        :return: x, y della casella dove si trova il mouse
        """
        row, column = cls.get_row_column_from_mouse(mouse_pos)
        return cls.get_xy_from_row_column(row, column)


    @classmethod
    def get_index_from_mouse(cls, mouse_pos):
        """
        :return: indice dell'array dalla posizione del mouse
        """
        row, column = cls.get_row_column_from_mouse(mouse_pos)
        return cls.get_index_from_row_column(row, column)
