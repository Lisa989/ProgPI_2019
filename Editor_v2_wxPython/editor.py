from Editor_v2_wxPython.panels.p5_editorScrolledWindow import EditorScrolledWindow
from Editor_v2_wxPython.editor_risorse import Immagini
from Editor_v2_wxPython.elements.griglia import Griglia
from Editor_v2_wxPython.elements.level import Level
from Editor_v2_wxPython.elements.popupMenu import MyPopupMenu
from costanti.editor_v2_wxPython_costanti import *
from Editor_v2_wxPython.elements.queueUndoRedo import MyQueueUndoRedo

import wx
import json

MODE_NONE = wx.NewId()  # nessun livello creato
MODE_EDIT = wx.NewId()  # modalità inserimento brick
MODE_PAINTING = wx.NewId()  # modalità sto disegnando brick
MODE_DELETE = wx.NewId()  # modalità cancellazione
MODE_ERASING = wx.NewId()  # modalità sto cancellando brick
MODE_MOVE = wx.NewId()  # modalità spostamento
MODE_DRAGGING = wx.NewId()  # modalità sto trascinando un brick
MODE_SELECT = wx.NewId()  # modalità selezione

# id delle operazioni
ID_PASTE = wx.NewId()
ID_COPY = wx.NewId()
ID_CUT = wx.NewId()
ID_MOVE = wx.NewId()
ID_NEW = wx.NewId()
ID_DELETE = wx.NewId()
ID_CLEAR = wx.NewId()
ID_CHANGE_COLOR = wx.NewId()
ID_CHANGE_TYPE = wx.NewId()


class Editor(EditorScrolledWindow):
    def __init__(self, parent):
        EditorScrolledWindow.__init__(self, parent)
        # struttura per gestire drag and drop dict(brk, idx_old, offset_x, offset_y)
        self.__drag_drop = None

        # struttura per gestire la selezione # dict(idx, brk, xy, rc)
        self.__select_brick = dict(idx=-1, brk=None, xy=(0, 0), rc=(0, 0))

        # variabile per memorizzare il brick copiato o tagliato
        self.__copy_cut_brick = None

        # coda per gestire le funzioni undo e redo
        self.__queue_log = MyQueueUndoRedo(self)

        # struttura contenente tutti i dati del livello
        self.__level = None

        # modalità selezionata
        self.__current_mode = MODE_NONE

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    ********************************************--UPDATE/DRAW--*********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def do_drawing(self, dc, printing=False):

        if self.__current_mode == MODE_NONE:
            return  # non è stato aperto un nuovo livello

        #  background
        dc.DrawBitmap(Immagini.background, SCREEN_LEVEL_X, SCREEN_LEVEL_Y, True)
        dc.DrawBitmap(Immagini.edge_top, EDGE_TOP, True)
        dc.DrawBitmap(Immagini.edge_vertical, EDGE_LEFT, True)
        dc.DrawBitmap(Immagini.edge_vertical, EDGE_RIGHT, True)

        # disegna il contorno del brick eccetto che in modalità select
        if Griglia.is_on_grid(self.mouse_pos) and not self.__current_mode == MODE_SELECT:
            dc.SetPen(wx.Pen('WHITE', 2))
            x, y = Griglia.get_xy_from_mouse(self.mouse_pos)
            dc.DrawLine(x, y, x + BRICK_WIDTH, y)
            dc.DrawLine(x, y, x, y + BRICK_HEIGHT)
            dc.DrawLine(x, y + BRICK_HEIGHT, x + BRICK_WIDTH, y + BRICK_HEIGHT)
            dc.DrawLine(x + BRICK_WIDTH, y, x + BRICK_WIDTH, y + BRICK_HEIGHT)

        # in modalità seleziona disegna brk selezionato
        if self.__current_mode == MODE_SELECT and not self.__select_brick['idx'] == -1:
            dc.SetPen(wx.Pen('WHITE', 2))
            x, y = self.__select_brick['xy']
            dc.DrawLine(x, y, x + BRICK_WIDTH, y)
            dc.DrawLine(x, y, x, y + BRICK_HEIGHT)
            dc.DrawLine(x, y + BRICK_HEIGHT, x + BRICK_WIDTH, y + BRICK_HEIGHT)
            dc.DrawLine(x + BRICK_WIDTH, y, x + BRICK_WIDTH, y + BRICK_HEIGHT)

        if self.__level is not None:
            self.__level.draw_briks(dc)

        # drag and drop
        if self.__current_mode == MODE_DRAGGING:
            x, y = (self.mouse_pos[0] - self.__drag_drop['offset_x']), (
                    self.mouse_pos[1] - self.__drag_drop['offset_y'])
            self.__drag_drop['brk'].draw_in_pos(dc, x, y)

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--EDITOR--************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def make_new_level(self, name, data=None):
        """
        Crea un nuovo livello
        :param name: nome del livello/file
        :param data: dati contenuti nel file caricato, None se il livello e nuovo
        :return:
        """
        if DEBUG:
            print("make_new_level")

        # abilita i bottoni, crea il livello, spacchetta i dati e inserisce i brick presenti nel livello
        self.enable_tool(True)
        self.__level = Level(name)
        if data is not None:
            for p in range(0, MAX_ROW * MAX_CLN):
                if data[p] is not None:
                    row, cln = data[p]["row"], data[p]["cln"]
                    tipo, colore = data[p]["type"], data[p]["color"]
                    self.__level.new_brick(row, cln, tipo, colore)

    # operazioni log per bottoni undo e redo
    def clear_redo_undo(self):
        """
        Vuota le liste redo e undo e disattiva i relativi pulsanti
        """
        if DEBUG:
            print("clear_redo_undo")

        self.__queue_log.clear_redo()
        self.__queue_log.clear_redo()

    # operazioni su brk
    def change_brick_color(self, color):
        """
        cambia il colore del brick selezionato
        :param color:
        """
        if DEBUG:
            print("change_brick_color")

        if self.__select_brick['brk'] is not None:
            color_old = self.__select_brick['brk'].get_color()
            self.__select_brick['brk'].change_color(color)
            # aggiorna la coda undo con l'operazione eseguita
            log = (ID_CHANGE_COLOR, self.__select_brick['idx'], self.__select_brick['brk'], color, color_old)
            self.__queue_log.put_undo(log)
            self.__queue_log.clear_redo()

            self.statusbar_set_text("Colore brick cambiato")
            if DEBUG:
                print("log: " + str(log))

    def change_brick_type(self, tipo):
        """
        cambia il tipo del brick selezionato
        :param tipo:
        :return
        """
        if DEBUG:
            print("change_brick_type")

        if self.__select_brick['brk'] is not None:
            tipo_old = self.__select_brick['brk'].get_type()
            self.__select_brick['brk'].change_type(tipo)
            # aggiorna la coda undo con l'operazione eseguita
            log = (ID_CHANGE_TYPE, self.__select_brick['idx'], self.__select_brick['brk'], tipo, tipo_old)
            self.__queue_log.put_undo(log)
            self.__queue_log.clear_redo()

            self.statusbar_set_text("Tipo brick cambiato")

            if DEBUG:
                print("log: " + str(log))

    def delete_brick(self):
        """
        cancella il brick sotto il puntatore del mouse
        :return
        """
        if DEBUG:
            print("delete_brick")

        # se non è stato creato un livello non fa niente
        if self.__current_mode == MODE_NONE:
            return

        p = Griglia.get_index_from_mouse(self.mouse_pos)
        brk = self.__level.delete_brick(p)
        if brk is not None:
            brk = brk.copy_brk()
            self.__level.set_context_modified()
            # aggiorna la coda undo con l'operazione eseguita
            log = (ID_DELETE, p, brk)
            self.__queue_log.put_undo(log)
            self.statusbar_set_text("Brick cancellato")
            if DEBUG:
                print("log: " + str(log))

    def new_brick(self):
        """
        inseriesce un brick con le caratteristiche selezionate sotto il puntatore del mouse
        """
        if DEBUG:
            print("new_brick")

        # se non è stato creato un livello non fa niente
        if self.__current_mode == MODE_NONE:
            return

        row, cln = Griglia.get_row_column_from_mouse(self.mouse_pos)
        tipo, colore = self.parent.get_brick_select()
        p, brk = self.__level.new_brick(row, cln, tipo, colore)
        if not p == -1:
            self.__level.set_context_modified()
            # aggiorna la coda undo con l'operazione eseguita
            log = (ID_NEW, p, brk)
            self.__queue_log.put_undo((ID_NEW, p, brk))
            self.__queue_log.clear_redo()
            self.statusbar_set_text("Nuovo brick inserito")

            if DEBUG:
                print("log: " + str(log))

    # operazioni per seleziona
    @staticmethod
    def is_equal_position(pos1, pos2):
        if DEBUG:
            print("is_equal_position")

        """
        Verifica se due posizioni sono uguali
        :param pos1:
        :param pos2:
        :return: True se pos1 e pos2 sono uguali, False altrimenti
        """
        x1, y1 = pos1
        x2, y2 = pos2
        return x1 == x2 and y1 == y2

    def select_none(self):
        """
        Imposta self.__select_brick con i valori di vuoto.
        """
        if DEBUG:
            print("select_none")

        self.__select_brick = dict(idx=-1, brk=None, xy=(0, 0), rc=(0, 0))
        self.statusbar_set_text("Nessuna posizione selezionata")

    def select_brick(self, p):
        """
        inserisce in self.__select_brick le informazione della posizione p
        :param p: indice arrey brick selezionato
        :return:
        """
        if DEBUG:
            print("select_brick")

        brk = self.__level.get_brick(p)
        pos = Griglia.get_xy_from_mouse(self.mouse_pos)
        r_c = Griglia.get_row_column_from_mouse(self.mouse_pos)
        self.__select_brick = dict(idx=p, brk=brk, xy=pos, rc=r_c)
        self.statusbar_set_text("Posizione " + str(p) + " selezionata")
        if DEBUG:
            print(self.__select_brick)

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--INPUT--*************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_mouse_motion(self, event):
        """
        Evento muovo il mouse
        :param event:
        """
        event.Skip()
        # se non è stato aperto un livello non fa niente
        if self.__current_mode == MODE_NONE:
            event.Skip()
            return

        self.set_xy(event)  # aggiorna la posizione del mouse

        # se sono sulla griglia
        # modalità disegno, inserisce un nuovo brick
        # modalità cancellazione, cancella il brick
        if Griglia.is_on_grid(self.mouse_pos):
            if self.__current_mode == MODE_PAINTING:
                self.new_brick()
            if self.__current_mode == MODE_ERASING:
                self.delete_brick()

    def on_mouse_press_left(self, event):
        """
        Evento tasto sinistro del mouse premuto
        :param event:
        """
        if DEBUG:
            print("on_mouse_press_left")

        # se non è stato aperto un livello non fa niente
        event.Skip()
        if self.__current_mode == MODE_NONE:
            return

        # se sono sulla griglia
        if Griglia.is_on_grid(self.mouse_pos):  # click sulla griglia
            p = Griglia.get_index_from_mouse(self.mouse_pos)
            # se sono in modalità EDIT, inserisce la modalità PAINT
            # veifica che la postazione sia libera e che sia stato selezionato un colore
            # crea un nuovo brick
            if self.__current_mode == MODE_EDIT:
                self.__current_mode = MODE_PAINTING
                self.statusbar_set_text("Modalità PAINTING")
                if DEBUG:
                    print("Modalità PAINTING")
                tipo, colore = self.parent.get_brick_select()
                if self.__level.is_position_free(p) and colore is not None:  # paint
                    self.new_brick()

            # se sono nella modalità MOVE, inserisce la modalità DRAGGING
            # salva le informazioni self.__drag_drop
            elif self.__current_mode == MODE_MOVE and not self.__level.is_position_free(p):  # drag and drop
                self.__current_mode = MODE_DRAGGING
                self.statusbar_set_text("Modalità DRAGGING")
                if DEBUG:
                    print("Modalità DRAGGING")
                brk = self.__level.take_brick(p)
                x, y = brk.get_position_on_screen()
                self.__drag_drop = dict(brk=brk, idx_old=p, offset_x=abs(self.mouse_pos[0] - x),
                                        offset_y=abs(self.mouse_pos[1] - y))
            # se sono in modalità DELETE, inserisce la modalita ERESING
            # cancella il brick
            elif self.__current_mode == MODE_DELETE:  # cancella
                self.__current_mode = MODE_ERASING
                self.statusbar_set_text("Modalità ERESING")
                if DEBUG:
                    print("Modalità ERESING")
                self.delete_brick()
            # se sono in modalità SELECT, seleziona o deseleziona il brick
            elif self.__current_mode == MODE_SELECT:
                pos = Griglia.get_xy_from_mouse(self.mouse_pos)
                if not self.__select_brick['idx'] == -1 and self.is_equal_position(pos, self.__select_brick['xy']):
                    self.select_none()
                else:
                    self.select_brick(p)

    def on_mouse_release_left(self, event):
        """
        Evento tasto sinistro del mouse rilasciato
        :param event:
        """
        if DEBUG:
            print("on_mouse_release_left")
        event.Skip()
        # se non è stato aperto un livello non fa niente
        if self.__current_mode == MODE_NONE:
            return

        # se sono in modalità DRAGGING, torno alla modalità MOVE
        # se sono sulla griglia e la posizione è libera, aggiorno le proprietà del brick,
        # altrimenti setta idx al vecchio indice dell'array
        # posiziona il brick all'indice corretto, cancella la struttura self.__drag_drop
        if self.__current_mode == MODE_DRAGGING:
            self.__current_mode = MODE_MOVE
            self.statusbar_set_text("Modalità MOVE ripristinata ")
            if DEBUG:
                print("Modalità MOVE ripristinata ")
            idx = Griglia.get_index_from_mouse(self.mouse_pos)
            if Griglia.is_on_grid(self.mouse_pos) and self.__level.is_position_free(idx):
                xy = Griglia.get_xy_from_mouse(self.mouse_pos)
                rc = Griglia.get_row_column_from_mouse(self.mouse_pos)
                # aggiorna la coda undo con l'operazione eseguita
                log = (ID_MOVE, idx, self.__drag_drop['idx_old'], self.__drag_drop['brk'], xy,
                       self.__drag_drop['brk'].get_position_on_screen(), rc,
                       self.__drag_drop['brk'].get_position_on_grid())
                self.__queue_log.put_undo(log)
                self.__queue_log.clear_redo()
                if DEBUG:
                    print("log: " + str(log))

                self.__drag_drop['brk'].change_pos(xy, rc)
                self.__level.set_context_modified()
                self.statusbar_set_text("Il brick è stato spostato")
            else:
                idx = self.__drag_drop['idx_old']
            self.__level.put_brick(self.__drag_drop['brk'], idx)
            self.__drag_drop = None
        # se sono in modalità ERASING, torno in modalità DELETE
        elif self.__current_mode == MODE_ERASING:
            self.__current_mode = MODE_DELETE
            if DEBUG:
                print("Modalità DELETE ripristinata ")
            self.statusbar_set_text("Modalità DELETE ripristinata")

        # se sono in modalità PAINT, torno in modalità EDIT
        elif self.__current_mode == MODE_PAINTING:
            self.__current_mode = MODE_EDIT
            if DEBUG:
                print("Modalità EDIT ripristinata ")
            self.statusbar_set_text("Modalità EDIT ripristinata")

    def on_mouse_press_right(self, event):
        """
        Evento tasto destro del mouse premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_mouse_press_right")
        # se non è stato aperto un livello non fa niente
        if self.__current_mode == MODE_NONE:
            return

        # se sono sulla griglia seleziono la casella e apro il menu a tendina
        if Griglia.is_on_grid(self.mouse_pos):
            p = Griglia.get_index_from_mouse(self.mouse_pos)
            self.select_brick(p)
            self.PopupMenu(MyPopupMenu(self), event.GetPosition())

    def on_leave_window(self, event):
        """
        Evento il mouse lascia la finestra dell'editor
        :param event:
        :return:
        """
        if DEBUG:
            print("on_leave_window")
        event.Skip()
        # se non è stato aperto un livello non fa niente
        if self.__current_mode == MODE_NONE:
            return

        # se sono in modalità DRAGGING, torno in modalità MOVE, riposiziono il brick nella vecchia posizione e cancello
        # la struttura self.__drag_drop
        if self.__current_mode == MODE_DRAGGING:
            self.__current_mode = MODE_MOVE
            self.statusbar_set_text("Modalità MOVE ripristinata")
            if DEBUG:
                print("Modalità MOVE ripristinata")
            self.__level.put_brick(self.__drag_drop['brk'], self.__drag_drop['idx_old'])
            self.__drag_drop = None
        # se sono in modalità ERESING, torno in modalità DELETE
        elif self.__current_mode == MODE_ERASING:
            self.__current_mode = MODE_DELETE
            self.statusbar_set_text("Modalità DELETE ripritinata")
            if DEBUG:
                print("Modalità DELETE ripritinata")
        # se sono in modalità PAINT, torno in modalità EDIT
        elif self.__current_mode == MODE_PAINTING:
            self.__current_mode = MODE_EDIT
            self.statusbar_set_text("Modalità EDIT ripristinata")
            if DEBUG:
                print("Modalità EDIT ripristinata")

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--BOTTONI--***********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_click_clear(self, event):
        """
        Evento bottone CLEAR premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_clear")
        brks = self.__level.clear_screen()
        # aggiorna la coda undo con l'operazione eseguita
        log = (ID_CLEAR, brks)
        self.__queue_log.put_undo(log)
        self.__queue_log.clear_redo()
        self.statusbar_set_text("I brick sono stati eliminati dal livello")
        if DEBUG:
            print("log: " + str(log))

    def on_click_open(self, event):
        """
        Evento bottone OPEN premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_open")
        # se l'attuale progresso del livello non è stato savato, chiede se si vuole proseguire comunque
        if self.__level is not None and not self.__level.is_context_saved():
            if wx.MessageBox("Il livello non è stato salvato! Procedere?", "Conferma",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # altrimenti chiede all'utente quale file vuole aprire
        with wx.FileDialog(self, "Open level", defaultDir=LEVEL_DIR, wildcard="JSON (*.json)|*.json|All Files|*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # l'utente ha cambiato idea

            # Procede a caricare il file scelto dall'utente, crea un nuovo livello,
            # se siamo in monalità NONE, setta la modalità EDIT
            # svuota le eventuali code undo e redo presenti
            filename = resource_path(fileDialog.GetPath())
            try:
                with open(filename) as data_file:
                    data = json.load(data_file)
                    data_file.close()
                self.make_new_level(fileDialog.GetFilename(), data)
                if self.__current_mode == MODE_NONE:
                    self.__current_mode = MODE_EDIT
                self.clear_redo_undo()
            except IOError:
                wx.LogError("Cannot open file '%s'." % filename)
                return
        self.statusbar_set_text("Il livello " + self.__level.filename + " è stato caricato")
        if DEBUG:
            print("Il livello " + self.__level.filename + " è stato caricato")

    def on_click_save(self, event):
        """
        Evento bottone SAVE premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_save")
        # apre la finestra di dialogo che permette di scegliere il nome e il luogo dove salvare il file
        with wx.FileDialog(self, "Save level", defaultDir=LEVEL_DIR, defaultFile=self.__level.filename,
                           wildcard="JSON (*.json)|*.json|All Files|*",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # l'utente ha cambiato idea

            # Procede con il salvataggio del file, serializza i dati
            filename = resource_path(fileDialog.GetPath())
            try:
                with open(filename, "w") as lv:
                    json.dump(self.__level.serialize(), lv)
                    self.__level.filename = fileDialog.GetFilename()
                    lv.close()
                    self.__level.set_context_saved()
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % filename)

        self.statusbar_set_text("Il livello " + self.__level.filename + " è stato salvato")
        if DEBUG:
            print("Il livello " + self.__level.filename + " è stato salvato")

    def on_click_new(self, event):
        """
        Evento bottone NEW premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_new")
        # se esiste un livello aperto e se l'attuale progresso del livello non è stato savato,
        # chiede se si vuole proseguire comunque
        if self.__level is not None and not self.__level.is_context_saved():
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # Prosegue con la creazione di un nuovo livello, cancella eventuali code undo e redo,
        # se siamo in modalità NONE setta la modalità EDIT
        name = get_level_name(N_LEVELS + 1)
        self.make_new_level(name)
        self.clear_redo_undo()
        if self.__current_mode == MODE_NONE:
            self.__current_mode = MODE_EDIT
        self.statusbar_set_text("E' stato creato il livello " + name)
        if DEBUG:
            print("E' stato creato il livello " + name)

    def on_click_edit_mode(self, event):
        """
        Evento bottone MODE_EDIT premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_edit_mode")
        # disabilita i bottoni copy_brk cut paste e seleziona la modalità
        self.parent.enable_copy_cut_paste(False)
        self.__current_mode = MODE_EDIT
        self.statusbar_set_text("Modalità EDIT selezionata")
        if DEBUG:
            print("Modalità EDIT selezionata")

    def on_click_delete_mode(self, event):
        """
        Evento bottone MODE_DELETE premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_delete_mode")
        # disabilita i bottoni copy_brk cut paste e seleziona la modalità
        self.parent.enable_copy_cut_paste(False)
        self.__current_mode = MODE_DELETE
        self.statusbar_set_text("Modalità DELETE selezionata")
        if DEBUG:
            print("Modalità DELETE selezionata")

    def on_click_move_mode(self, event):
        """
        Evento bottone MODE_MOVE premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_move_mode")

        # disabilita i bottoni copy_brk cut paste e seleziona la modalità
        self.parent.enable_copy_cut_paste(False)
        self.__current_mode = MODE_MOVE
        self.statusbar_set_text("Modalità MOVE selezionata")

        if DEBUG:
            print("Modalità MOVE selezionata")

    def on_click_select_mode(self, event):
        """
        Evento bottone MODE_SELECT premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_select_mode")

        # abilita i bottoni copy_brk cut paste e seleziona la modalità
        self.parent.enable_copy_cut_paste(True)
        self.__current_mode = MODE_SELECT
        self.statusbar_set_text("Modalita SELECT selezionata")

        if DEBUG:
            print("Modalità SELECT selezionata")

    def on_click_copy(self, event):
        """
        Evento bottone COPY premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_copy")

        # se non esiste una posizione selezionata, segnala un messaggio
        if self.__select_brick['idx'] == -1:
            wx.MessageBox("Nessuna casella selezionata")
            return

        # se la posizione selezionata contiene un brick, lo copia
        # altrimenti inserisce None in self.__copy_cut_brick
        if self.__select_brick['brk'] is not None:
            self.__copy_cut_brick = self.__select_brick['brk'].copy_brk()
        else:
            self.__copy_cut_brick = None
        self.statusbar_set_text("Copia")
        if DEBUG:
            print("select_brick: " + str(self.__select_brick))
            print("cut_copy_brick: " + self.__copy_cut_brick)

    def on_click_cut(self, event):
        """
        Evento bottone CUT premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_cut")

        # se non esiste una posizione selezionata, segnala un messaggio
        if self.__select_brick['idx'] == -1:
            wx.MessageBox("Nessuna casella selezionata")
            return

        # preleva il brick dal livello e lo memorizza in self.__copy_cut_brick
        self.__copy_cut_brick = self.__level.take_brick(self.__select_brick['idx'])
        # aggiorna la coda undo con l'operazione eseguita
        log = (ID_CUT, self.__select_brick['idx'], self.__copy_cut_brick)
        self.__queue_log.put_undo(log)
        self.__queue_log.clear_redo()
        self.statusbar_set_text("Taglia")
        if DEBUG:
            print("log: " + str(log))

        if DEBUG:
            print("select_brick: " + str(self.__select_brick))
            print("copy_cut_brick: " + self.__copy_cut_brick)

    def on_click_paste(self, event):
        """
        Evento bottone PASTE premuto
        :param event:
        :return:
        """
        if DEBUG:
            print("on_click_paste")

        # se non esiste una posizione selezionata, segnala un messaggio
        if self.__select_brick['idx'] == -1:
            wx.MessageBox("Nessuna casella selezionata")
            return

        # prende le info necessarie della posizione selezionata
        p = self.__select_brick['idx']
        xy = self.__select_brick['xy']
        rc = self.__select_brick['rc']

        # se esiste un brick copiato o tagliato
        # copia il brick e gli cambia la posizione, lo inserisce nella posizione p
        # altrimenti inserisce None nella posizione p
        if self.__copy_cut_brick is not None:
            brk = self.__copy_cut_brick.copy_brk()
            brk.change_pos(xy, rc)
            self.__level.put_brick(brk, p)
            # aggiorna la coda undo con l'operazione eseguita
            log = (ID_PASTE, p, brk, self.__copy_cut_brick)
            self.__queue_log.put_undo(log)
            self.__queue_log.clear_redo()

        else:
            self.__level.put_brick(None, p)
            # aggiorna la coda undo con l'operazione eseguita
            log = (ID_PASTE, p, None, self.__copy_cut_brick)
            self.__queue_log.put_undo(log)
            self.__queue_log.clear_redo()
        self.statusbar_set_text("Incolla")

        if DEBUG:
            print("log: " + str(log))
            print("select_brick: " + str(self.__select_brick))
            print("copy_cut_brick: " + self.__copy_cut_brick)

    def on_click_undo(self, event):
        """
        Evento bottone UNDO premuto
        :param event:
        :return:
        """
        elem = self.__queue_log.take_undo()  # elemento salvato nella coda
        if DEBUG:
            print("on_click_undo: " + str(elem))

        id_op = elem[0]  # ID operazione

        # operazione PASTE, riposiziona il vecchio contenuto della posizione
        if id_op == ID_PASTE:
            p, brk_old = elem[1], elem[3]
            self.__level.put_brick(brk_old, p)
            self.statusbar_set_text("PASTE undo")
        # operazione CUT, riposiziona il brick nella posizione da cui è stato tagliato
        elif id_op == ID_CUT:
            p, brk = elem[1], elem[2]
            self.__level.put_brick(brk, p)
            self.statusbar_set_text("CUT undo")
        # operazione MOVE, cancella il brick dalla nuova posizione, gli cambia le coordinate e lo riposiziona nella
        # vecchia posizione
        elif id_op == ID_MOVE:
            p_new = elem[1]
            p_old, xy_old, rc_old = elem[2], elem[5], elem[7]
            brk = elem[3]
            self.__level.delete_brick(p_new)
            brk.change_pos(xy_old, rc_old)
            self.__level.put_brick(brk, p_old)
            self.statusbar_set_text("MOVE undo")
        # operazione NEW, elimina il brick in posizione p
        elif id_op == ID_NEW:
            p = elem[1]
            self.__level.delete_brick(p)
            self.statusbar_set_text("NEW undo")
        # operazione DELETE, riposiziona il brk eliminato in posizione p
        elif id_op == ID_DELETE:
            p, brk = elem[1], elem[2]
            self.__level.put_brick(brk, p)
            self.statusbar_set_text("DELETE undo")
        # operazione CLEAR, riposiziona i brick cancellati
        elif id_op == ID_CLEAR:
            brks = elem[1]
            self.__level.put_list_bricks(brks)
            self.statusbar_set_text("CLEAR undo")
        # operazione CHANGE_TYPE, cambia il tipo del brick al vecchio valore
        elif id_op == ID_CHANGE_TYPE:
            brk, tipo_old = elem[2], elem[4]
            brk.change_type(tipo_old)
            self.statusbar_set_text("CHANGE TYPE undo")
        # operazione CHANGE_COLOR, cambia il colore del brick al vecchio valore
        elif id_op == ID_CHANGE_COLOR:
            brk, colore_old = elem[2], elem[4]
            brk.change_color(colore_old)
            self.statusbar_set_text("CHANGE COLOR undo")

    def on_click_redo(self, event):
        """
        Evento bottone REDO premuto
        :param event:
        :return:
        """
        elem = self.__queue_log.take_redo()
        if DEBUG:
            print("on_click_redo: " + str(elem))

        id_op = elem[0]

        # operazione PASTE,
        if id_op == ID_PASTE:
            p, brk = elem[1], elem[2]
            self.__level.put_brick(brk, p)
            self.statusbar_set_text("PASTE redo")
        # operazione CUT,
        elif id_op == ID_CUT:
            p = elem[1]
            self.__level.delete_brick(p)
            self.statusbar_set_text("CUT redo")
        # operazione MOVE,
        elif id_op == ID_MOVE:
            brk = elem[3]
            p_new, xy_new, rc_new = elem[1], elem[4], elem[6]
            p_old = elem[2]
            self.__level.delete_brick(p_old)
            brk.change_pos(xy_new, rc_new)
            self.__level.put_brick(brk, p_new)
            self.statusbar_set_text("MOVE redo")
        # operazione NEW, posiziono il brick nella posizione p
        elif id_op == ID_NEW:
            p, brk = elem[1], elem[2]
            self.__level.put_brick(brk, p)
            self.statusbar_set_text("NEW redo")
        # operazione DELETE, cancello il brick in posizione p
        elif id_op == ID_DELETE:
            p = elem[1]
            self.__level.delete_brick(p)
            self.statusbar_set_text("DELETE redo")
        # operazione CLEAR, svuoto l'array dei brick
        elif id_op == ID_CLEAR:
            self.__level.clear_screen()
            self.statusbar_set_text("CLEAR redo")
        # operazione CHANGE_TYPE, cambia il tipo del brick al nuovo scelto
        elif id_op == ID_CHANGE_TYPE:
            brk, tipo = elem[2], elem[3]
            brk.change_type(tipo)
            self.statusbar_set_text("CHANGE TYPE redo")
        # operazione CHANGE_COLOR, cambia il colore del brick al nuovo scelto
        elif id_op == ID_CHANGE_COLOR:
            brk, colore = elem[2], elem[3]
            brk.change_color(colore)
            self.statusbar_set_text("CHANDE COLOR redo")
