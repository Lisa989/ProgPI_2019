import wx
from costanti.images_names import colors
from Editor_v2_wxPython.editor_risorse import Immagini
from costanti.editor_v2_wxPython_costanti import DEBUG, ID_BROWN, ID_DARK_GREEN, ID_YELLOW, ID_BLUE, ID_ORANGE, ID_RED, ID_PURPLE, ID_GREEN, ID_LIGHT_BLUE, ID_NONE


class BrickColorPanel(wx.Panel):
    def __init__(self, parent, **k):
        wx.Panel.__init__(self, parent, **k)
        self.parent = parent
        self.statusbar_set_text = parent.statusbar_set_text
        self.SetBackgroundColour("LIGHT_GREY")

        self.__select = ID_BLUE
        self.__bt_color = dict()
        self.__init_buttons()

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_press)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_release_left)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_press_left)
        self.Bind(wx.EVT_RIGHT_UP, self.on_mouse_release_right)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_mouse_press_right)

    def __init_buttons(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        grid_box = wx.GridSizer(rows=3, cols=3, hgap=5, vgap=5)

        for color in colors:
            self.__bt_color[color] = wx.ToggleButton(self, name=color)

        self.__bt_color["blue"].SetValue(True)

        for color in colors:
            self.__bt_color[color].SetBitmap(Immagini.color_bricks[color])
            grid_box.Add(self.__bt_color[color], 0, wx.EXPAND | wx.CENTER)

        vbox.Add(wx.StaticBitmap(self, bitmap=Immagini.color_label), 0, wx.EXPAND | wx.CENTER)
        vbox.Add(grid_box, 0, wx.EXPAND | wx.CENTER)

        self.SetSizerAndFit(vbox)

        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_blue, self.__bt_color[ID_BLUE])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_green, self.__bt_color[ID_GREEN])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_purple, self.__bt_color[ID_PURPLE])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_red, self.__bt_color[ID_RED])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_orange, self.__bt_color[ID_ORANGE])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_light_blue, self.__bt_color[ID_LIGHT_BLUE])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_yellow, self.__bt_color[ID_YELLOW])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_dark_green, self.__bt_color[ID_DARK_GREEN])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_brown, self.__bt_color[ID_BROWN])

    def get_select_color(self):
        return self.__select

    def __select_buttons(self, select):
        """
        Seleziona il colore cliccato e deleziona gli altri
        :param select: colore selezionato
        :return:
        """
        if not self.__bt_color[select].GetValue():
            self.__select = ID_NONE
            return
        self.__select = select
        for color in colors:
            if not color == select:
                self.__bt_color[color].SetValue(False)

        if DEBUG:
            print("is select " + select)

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    *********************************************--BOTTONI--************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_click_blue(self, event):
        if DEBUG:
            print("on_click_blue")
        self.__select_buttons(ID_BLUE)
        self.statusbar_set_text("Colore BLUE selezionato")
        event.Skip()

    def on_click_green(self, event):
        if DEBUG:
            print("on_click_green")
        self.__select_buttons(ID_GREEN)
        self.statusbar_set_text("Colore GREEN selezionato")
        event.Skip()

    def on_click_purple(self, event):
        if DEBUG:
            print("on_click_purple")
        self.__select_buttons(ID_PURPLE)
        self.statusbar_set_text("Colore PURPLE selezionato")
        event.Skip()

    def on_click_red(self, event):
        if DEBUG:
            print("on_click_red")
        self.__select_buttons(ID_RED)
        self.statusbar_set_text("Colore RED selezionato")
        event.Skip()

    def on_click_orange(self, event):
        if DEBUG:
            print("on_click_orange")
        self.__select_buttons(ID_ORANGE)
        self.statusbar_set_text("Colore ORANGE selezionato")
        event.Skip()

    def on_click_light_blue(self, event):
        if DEBUG:
            print("on_click_light_blue")
        self.__select_buttons(ID_LIGHT_BLUE)
        self.statusbar_set_text("Colore LIGHT BLUE selezionato")
        event.Skip()

    def on_click_yellow(self, event):
        if DEBUG:
            print("on_click_yellow")
        self.__select_buttons(ID_YELLOW)
        self.statusbar_set_text("Colore YELLOW selezionato")
        event.Skip()

    def on_click_dark_green(self, event):
        if DEBUG:
            print("on_click_dark_green")
        self.__select_buttons(ID_DARK_GREEN)
        self.statusbar_set_text("Colore DARK_GREEN selezionato")
        event.Skip()

    def on_click_brown(self, event):
        if DEBUG:
            print("on_click_brown")
        self.__select_buttons(ID_BROWN)
        self.statusbar_set_text("Colore BROWN selezionato")
        event.Skip()

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--EVENTI--************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_key_press(self, event):
        if DEBUG:
            print("BrickColorPanel_on_key_press", event.GetKeyCode())
        event.Skip()

    def on_mouse_motion(self, event):
        event.Skip()

    def on_mouse_press_left(self, event):
        if DEBUG:
            print("BrickColorPanel_on_mouse_press_left")
        event.Skip()

    def on_mouse_press_right(self, event):
        if DEBUG:
            print("BrickColorPanel_on_mouse_press_right")
        event.Skip()

    def on_mouse_release_left(self, event):
        if DEBUG:
            print("BrickColorPanel_on_mouse_release_left")
        event.Skip()

    def on_mouse_release_right(self, event):
        if DEBUG:
            print("BrickColorPanel_on_mouse_release_right")
        event.Skip()
