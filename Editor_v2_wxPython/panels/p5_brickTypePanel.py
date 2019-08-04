import wx
from costanti.editor_v2_wxPython_costanti import DEBUG, ID_SIMPLE, ID_DOUBLE, ID_IMMORTAL, ID_NONE
from Editor_v2_wxPython.editor_risorse import Immagini
from costanti.images_names import type_bt


class BrickTypePanel(wx.Panel):
    def __init__(self, parent, **k):
        wx.Panel.__init__(self, parent, **k)
        self.parent = parent
        self.statusbar_set_text = parent.statusbar_set_text
        self.SetBackgroundColour("LIGHT_GREY")

        self.select = ID_SIMPLE
        self.bt_type = dict()

        self.__init_buttons()

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_press)
        self.Bind(wx.EVT_MOTION, self.on_mouse_motion)
        self.Bind(wx.EVT_LEFT_UP, self.on_mouse_release_left)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_press_left)
        self.Bind(wx.EVT_RIGHT_UP, self.on_mouse_release_right)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_mouse_press_right)

    def __init_buttons(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticBitmap(self, bitmap=Immagini.type_label), 1, wx.CENTER | wx.ALIGN_CENTER)

        self.bt_type[ID_SIMPLE] = wx.ToggleButton(self, name="Simple")
        self.bt_type[ID_DOUBLE] = wx.ToggleButton(self, name="Double")
        self.bt_type[ID_IMMORTAL] = wx.ToggleButton(self, name="Immortal")

        for tp in type_bt:
            self.bt_type[tp].SetBitmap(Immagini.buttons_yellow[tp])
            self.bt_type[tp].SetBitmapPressed(Immagini.buttons_orange[tp])
            vbox.Add(self.bt_type[tp], 0, wx.CENTER)

        self.bt_type[ID_SIMPLE].SetValue(True)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_button_simple, self.bt_type[ID_SIMPLE])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_button_double, self.bt_type[ID_DOUBLE])
        self.Bind(wx.EVT_TOGGLEBUTTON, self.on_click_button_immortal, self.bt_type[ID_IMMORTAL])

        self.SetSizerAndFit(vbox)

    def get_select_type(self):
        return self.select

    def __select_type(self, select):
        if not self.bt_type[select].GetValue():
            self.select = ID_NONE
            return
        self.select = select
        for tp in type_bt:
            if not tp == select:
                self.bt_type[tp].SetValue(False)

        if DEBUG:
            print('is select: ' + select)

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    *********************************************--BOTTONI--************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_click_button_simple(self, event):
        if DEBUG:
            print("on_click_button_simple")
        self.__select_type(ID_SIMPLE)
        self.statusbar_set_text("Tipo SIMPLE selezionato")
        event.Skip()

    def on_click_button_double(self, event):
        if DEBUG:
            print("on_click_button_double")
        self.__select_type(ID_DOUBLE)
        self.statusbar_set_text("Tipo DOUBLE selezionato")
        event.Skip()

    def on_click_button_immortal(self, event):
        if DEBUG:
            print("on_click_button_immortal")
        self.__select_type(ID_IMMORTAL)
        self.statusbar_set_text("Tipo IMMORTAL selezionato")
        event.Skip()

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--EVENTI--************************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_key_press(self, event):
        if DEBUG:
            print("BrickTypePanel_on_key_press")
        event.Skip()

    def on_mouse_motion(self, event):
        event.Skip()

    def on_mouse_press_left(self, event):
        if DEBUG:
            print("BrickTypePanel_on_mouse_press_left")
        event.Skip()

    def on_mouse_press_right(self, event):
        if DEBUG:
            print("BrickTypePanel_on_mouse_press_right")
        event.Skip()

    def on_mouse_release_left(self, event):
        if DEBUG:
            print("BrickTypePanel_on_mouse_release_left")
        event.Skip()

    def on_mouse_release_right(self, event):
        if DEBUG:
            print("BrickTypePanel_on_mouse_release_right")
        event.Skip()
