from Editor_v2_wxPython.editor_risorse import Immagini
from Editor_v2_wxPython.elements.griglia import Griglia
from costanti.costanti import ID_DOUBLE, ID_IMMORTAL, ID_SIMPLE, ID_GREY


class Brick:
    def __init__(self, row, column, tipo, colore):
        """
        Nuovo brick
        :param row: riga
        :param column: colonna
        :param tipo: tipo di brick
        :param colore: colore del brick
        """
        self.__type = tipo
        self.__color = colore
        self.__row = row
        self.__column = column

        # init position on screen
        self.__x, self.__y = Griglia.get_xy_from_row_column(row, column)
        self.__img = self.__init_img()

    def __init_img(self):
        if self.__type == ID_DOUBLE:
            return Immagini.bricks_break[self.__color]
        elif self.__type == ID_IMMORTAL:
            return Immagini.bricks[ID_GREY]
        if self.__type == ID_SIMPLE:
            return Immagini.bricks[self.__color]

    def change_color(self, color):
        self.__color = color
        self.__img = self.__init_img()

    def change_type(self, tipo):
        self.__type = tipo
        self.__img = self.__init_img()

    def change_pos(self, x_y, row_cln):
        self.__x, self.__y = x_y
        self.__row, self.__column = row_cln

    def draw(self, dc):
        dc.DrawBitmap(self.__img, self.__x, self.__y, True)

    def draw_in_pos(self, dc, x, y):
        dc.DrawBitmap(self.__img, x, y, True)

    def serialize(self):
        return dict(cln=self.__column, row=self.__row, color=self.__color, type=self.__type)

    def copy_brk(self):
        return Brick(self.__row, self.__column, self.__type, self.__color)

    def get_type(self):
        return self.__type

    def get_color(self):
        return self.__color

    def get_position_on_screen(self):
        return self.__x, self.__y

    def get_position_on_grid(self):
        return self.__row, self.__column
