import wx
from costanti.editor_v2_wxPython_costanti import ID_BLUE, ID_GREEN, ID_BROWN, ID_DARK_GREEN, ID_YELLOW, ID_LIGHT_BLUE, ID_ORANGE, ID_PURPLE, ID_RED
from costanti.editor_v2_wxPython_costanti import ID_IMMORTAL, ID_DOUBLE, ID_SIMPLE


class MyPopupMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)

        self.parent = parent

        self.menu_colore()
        self.menu_tipo()
        self.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.on_new, self.Append(wx.MenuItem(self, wx.NewId(), 'New')))
        self.Bind(wx.EVT_MENU, self.on_delete, self.Append(wx.MenuItem(self, wx.NewId(), 'Delete')))
        self.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.on_copy, self.Append(wx.MenuItem(self, wx.NewId(), 'Copy')))
        self.Bind(wx.EVT_MENU, self.on_cut, self.Append(wx.MenuItem(self, wx.NewId(), 'Cut')))
        self.Bind(wx.EVT_MENU, self.on_paste, self.Append(wx.MenuItem(self, wx.NewId(), 'Paste')))

    def menu_colore(self):
        cls = wx.Menu()
        self.Bind(wx.EVT_MENU, self.on_click_light_blue, cls.Append(wx.ID_ANY, ID_LIGHT_BLUE))
        self.Bind(wx.EVT_MENU, self.on_click_blue, cls.Append(wx.ID_ANY, ID_BLUE))
        self.Bind(wx.EVT_MENU, self.on_click_green, cls.Append(wx.ID_ANY, ID_GREEN))
        self.Bind(wx.EVT_MENU, self.on_click_dark_green, cls.Append(wx.ID_ANY, ID_DARK_GREEN))
        self.Bind(wx.EVT_MENU, self.on_click_yellow, cls.Append(wx.ID_ANY, ID_YELLOW))
        self.Bind(wx.EVT_MENU, self.on_click_orange, cls.Append(wx.ID_ANY, ID_ORANGE))
        self.Bind(wx.EVT_MENU, self.on_click_purple, cls.Append(wx.ID_ANY, ID_PURPLE))
        self.Bind(wx.EVT_MENU, self.on_click_red, cls.Append(wx.ID_ANY, ID_RED))
        self.Bind(wx.EVT_MENU, self.on_click_brown, cls.Append(wx.ID_ANY, ID_BROWN))

        self.Append(wx.ID_ANY, 'Colore', cls)

    def menu_tipo(self):
        tp = wx.Menu()
        self.Bind(wx.EVT_MENU, self.on_click_simple, tp.Append(wx.ID_ANY, ID_SIMPLE))
        self.Bind(wx.EVT_MENU, self.on_click_double, tp.Append(wx.ID_ANY, ID_DOUBLE))
        self.Bind(wx.EVT_MENU, self.on_click_immortal, tp.Append(wx.ID_ANY, ID_IMMORTAL))

        self.Append(wx.ID_ANY, 'Tipo', tp)

    def on_click_blue(self, event):
        self.parent.change_brick_color(ID_BLUE)

    def on_click_light_blue(self, event):
        self.parent.change_brick_color(ID_LIGHT_BLUE)

    def on_click_green(self, event):
        self.parent.change_brick_color(ID_GREEN)

    def on_click_dark_green(self, event):
        self.parent.change_brick_color(ID_DARK_GREEN)

    def on_click_yellow(self, event):
        self.parent.change_brick_color(ID_YELLOW)

    def on_click_orange(self, event):
        self.parent.change_brick_color(ID_ORANGE)

    def on_click_purple(self, event):
        self.parent.change_brick_color(ID_PURPLE)

    def on_click_red(self, event):
        self.parent.change_brick_color(ID_RED)

    def on_click_brown(self, event):
        self.parent.change_brick_color(ID_BROWN)

    def on_click_simple(self, event):
        self.parent.change_brick_type(ID_SIMPLE)

    def on_click_double(self, event):
        self.parent.change_brick_type(ID_DOUBLE)

    def on_click_immortal(self, event):
        self.parent.change_brick_type(ID_IMMORTAL)

    def on_copy(self, event):
        self.parent.on_click_copy(event)

    def on_cut(self, event):
        self.parent.on_click_cut(event)

    def on_paste(self, event):
        self.parent.on_click_paste(event)

    def on_new(self, event):
        self.parent.new_brick()

    def on_delete(self, event):
        self.parent.delete_brick()
