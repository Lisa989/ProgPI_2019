from Editor_v2_wxPython.editor_risorse import *
from Editor_v2_wxPython.elements.keyEventTool import get_keyName

class EditorScrolledWindow(wx.ScrolledCanvas):
    def __init__(self, parent):
        wx.ScrolledCanvas.__init__(self, parent, style=wx.BORDER_THEME | wx.ALWAYS_SHOW_SB)
        self.parent = parent
        self.enable_tool = parent.enable_tool
        self.enable_redo = parent.enable_redo
        self.enable_undo = parent.enable_undo
        self.statusbar_set_text = parent.statusbar_set_text

        self.mouse_pos = (0, 0)

        self.SetBackgroundColour("BLACK")
        self.SetDoubleBuffered(True)

        # imposta timer
        self.update_timer = wx.Timer(self)
        self.__fps = 60.0
        self.__timespacing = 1000.0 / self.__fps
        self.update_timer.Start(self.__timespacing, False)

        # bind event
        self.Bind(wx.EVT_TIMER, self.on_update, self.update_timer)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        # self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_press)
        #self.Bind(wx.EVT_CHAR, self.on_key_press)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_release_left)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_press_left)
        self.Bind(wx.EVT_RIGHT_UP, self.on_mouse_release_right)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_mouse_press_right)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave_window)

        # imposta scrolling
        self.maxSize = (SCREEN_WIDTH, SCREEN_HEIGHT)
        # self.SetMaxSize(self.maxSize)
        self.SetVirtualSize(self.maxSize)
        self.SetSize(self.maxSize)
        self.SetScrollRate(20, 20)

        self.__init_buffer()

    def __convert_event_coords(self, event):
        """
        :param event:
        :return: coordinare calcolate secondo la posizione not scrolled
        """
        newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        return newpos

    def set_xy(self, event):
        """
        Calcola le coordinate del evento e le salva in self.__mouse_pos
        :param event:
        :return:
        """
        self.mouse_pos = self.__convert_event_coords(event)

    def __init_buffer(self):
        # Inizializza la bitmap del buffer.
        size_w, size_h = (self.maxSize)  # self.GetVirtualSize()
        self.__buffer = wx.Bitmap(size_w, size_h, 32)
        dc = wx.BufferedDC(None, self.__buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    ********************************************--UPDATE/DRAW--*********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_update(self, event):
        """
        Ad ogni tick crea un wx.BufferedDC, ci disegna e aggiorna la vista
        :param event:
        :return:
        """
        dc = wx.BufferedDC(None, self.__buffer)
        self.do_drawing(dc)

    def do_drawing(self, dc):
        """
        Disegna su dc
        :param dc: wx.BufferedDC su cui disegnare
        :return:
        """
        pass

    def on_paint(self, event):
        """
        Crea il buffer paint DC.
        Creerà il vero wx.PaintDC e quindi bliterà la bitmap su di esso quando viene cancellato dc.
        :param event:
        :return:
        """
        wx.BufferedPaintDC(self, self.__buffer, wx.BUFFER_VIRTUAL_AREA)
        self.Refresh()

    def on_size(self, event):
        self.__init_buffer()
        event.Skip()

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--EVENTI--*************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_key_press(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_key_press " + get_keyName(event.GetKeyCode()))

    def on_mouse_motion(self, event):
        event.Skip()

    def on_mouse_press_left(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_mouse_press_left")

    def on_mouse_press_right(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_mouse_press_right")

    def on_mouse_release_left(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_mouse_release_left")

    def on_mouse_release_right(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_mouse_release_right")

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--BOTTONI--*************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_click_new(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_new")

    def on_click_clear(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_clear")

    def on_click_open(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_open")

    def on_click_save(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_save")

    def on_click_undo(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_backward")

    def on_click_redo(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_redo")

    def on_click_cut(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_cut")

    def on_click_copy(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_copy")

    def on_click_paste(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_paste")

    def on_click_zoom_in(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_zoom_in")

    def on_click_zoom_out(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_zoom_out")

    def on_leave_window(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_leave_window")

    def on_click_edit_mode(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_edit_mode")

    def on_click_delete_mode(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_delete_mode")

    def on_click_move_mode(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_move_mode")

    def on_click_select_mode(self, event):
        event.Skip()
        if DEBUG:
            print("editor_on_click_select_mode")
