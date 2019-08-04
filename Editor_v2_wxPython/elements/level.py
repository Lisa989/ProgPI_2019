from Editor_v2_wxPython.elements.griglia import Griglia
from costanti.editor_v2_wxPython_costanti import MAX_CLN, MAX_ROW, DEBUG, ID_IMMORTAL, ID_NONE
from Editor_v2_wxPython.elements.brick import Brick
from wx import LogMessage


class Level:
    def __init__(self, filename=""):
        self.filename = filename
        self.__bricks = self.init_bricks()
        self.__contextSave = True

    @staticmethod
    def init_bricks():
        brks = []
        for p in range(0, MAX_CLN * MAX_ROW):
            brks.append(None)
        return brks

    def put_list_bricks(self, brks):
        self.__bricks = brks

    def is_position_free(self, p):
        """
        Verifica se la posizione p è occupata
        :param p: indice array
        :return: True se è libera, False altrimenti
        """
        if self.__bricks[p] is None:
            return True
        return False

    def draw_briks(self, dc):
        """
        Disegna tutti i brick
        :param dc:
        :return:
        """
        for brk in self.__bricks:
            if brk is not None:
                brk.draw(dc)

    def take_brick(self, p):
        """
        Preleva il brick in posizione p
        :param p: indice array
        :return: brick prelevato
        """
        brk = self.__bricks[p]
        self.__bricks[p] = None
        return brk

    def get_brick(self, p):
        """
        Restituisce il brick in posizione p
        :param p:
        :return:
        """
        return self.__bricks[p]

    def put_brick(self, brk, p):
        """
        Inserisce il brick nella posizione p
        :param brk: brick da inserire
        :param p: indice dell'array
        :return:
        """
        self.__bricks[p] = brk

    def new_brick(self, row, column, tipo, colore):
        """
        Crea un nuovo brick e lo posiziona nell'apposita struttura bricks
        :return:
        """
        if not tipo == ID_IMMORTAL and colore == ID_NONE:
            LogMessage("Nessun colore selezionato")
            return -1, None
        p = Griglia.get_index_from_row_column(row, column)
        if self.__bricks[p] is None:
            self.__bricks[p] = Brick(row, column, tipo, colore)
            return p, self.__bricks[p]
        return -1, None

    def delete_brick(self, p):
        """
        Cancella il brick data la posizione del mouse
        :param p: posizione nell' array
        :return:
        """
        brk = self.__bricks[p]
        self.__bricks[p] = None

        return brk

    def serialize(self):
        """
        :return: lista informazioni brikcs
        """
        if DEBUG:
            print("serialize")

        list_bricks = []

        for column in range(0, MAX_CLN):
            for row in range(0, MAX_ROW):
                p = Griglia.get_index_from_row_column(row, column)
                if self.__bricks[p] is None:
                    list_bricks.append(None)
                else:
                    list_bricks.append(self.__bricks[p].serialize())

        return list_bricks

    def clear_screen(self):
        """
        Cancella tutti i bricks presenti sullo schermo
        :return:
        """
        brks = []
        for p in range(0, MAX_ROW * MAX_CLN):
            brks.append(self.__bricks[p])
            self.__bricks[p] = None
        return brks

    # gestione della modifica del contesto
    def set_context_modified(self):
        """
        Il contesto è stato modificato
        :return:
        """
        self.__contextSave = False

    def set_context_saved(self):
        """
        Il contesto è stato salvato
        :return:
        """
        self.__contextSave = True

    def is_context_saved(self):
        """
        :return: True se il contesto è salvato, false altrimenti
        """
        return self.__contextSave
