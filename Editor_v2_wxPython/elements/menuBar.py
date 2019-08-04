import wx


class MenuBar(wx.MenuBar):
    """
    crea menubar
    """

    def __init__(self, parent, style=0):
        wx.MenuBar.__init__(self)
        self.parent = parent

        self.init_file_menu()
        self.init_editor_menu()
        self.init_view_menu()

    def init_view_menu(self):
        view_menu = wx.Menu()

        self.statusbar_check = view_menu.Append(wx.ID_ANY, 'Mostra statusbar', 'Mostra Statusbar', kind=wx.ITEM_CHECK)
        self.toolbar_check = view_menu.Append(wx.ID_ANY, 'Mostra toolbar', 'Mostra Toolbar', kind=wx.ITEM_CHECK)
        # self.logpanel_check = view_menu.Append(wx.ID_ANY, 'Mostra logFile', 'Mostra logFile', kind=wx.ITEM_CHECK)

        view_menu.Check(self.statusbar_check.GetId(), True)
        view_menu.Check(self.toolbar_check.GetId(), True)
        # view_menu.Check(self.logpanel_check.GetId(), True)

        self.Bind(wx.EVT_MENU, self.toggle_status_bar, self.statusbar_check)
        self.Bind(wx.EVT_MENU, self.toggle_tool_bar, self.toolbar_check)
        # self.Bind(wx.EVT_MENU, self.toggle_tool_bar, self.logpanel_check)

        self.Append(view_menu, '&View')

    def init_file_menu(self):
        file_menu = wx.Menu()  # creo un menu

        item_new = file_menu.Append(wx.ID_NEW, 'New\tCtrl+N')
        item_open = file_menu.Append(wx.ID_OPEN, 'Open\tCtrl+L')
        item_save = file_menu.Append(wx.ID_SAVE, 'Save\tCtrl+S')
        file_menu.AppendSeparator()  # un separator
        item_exit = file_menu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q')

        self.Bind(wx.EVT_MENU, self.handle_buttons, item_exit)
        self.Bind(wx.EVT_MENU, self.handle_buttons, item_new)
        self.Bind(wx.EVT_MENU, self.handle_buttons, item_open)
        self.Bind(wx.EVT_MENU, self.handle_buttons, item_save)

        self.Append(file_menu, '&File')

    def init_editor_menu(self):
        editor_menu = wx.Menu()  # creo il menu
        item_backward = editor_menu.Append(wx.ID_UNDO, 'Backward\tCtrl+Z')
        item_forward = editor_menu.Append(wx.ID_REDO, 'Forward\tCtrl+Y')
        editor_menu.AppendSeparator()
        item_cut = editor_menu.Append(wx.ID_CUT, 'Cut\tCtrl+X')
        item_copy = editor_menu.Append(wx.ID_COPY, 'Copy\tCtrl+C')
        item_paste = editor_menu.Append(wx.ID_PASTE, 'Past\tCtrl+V')
        # editor_menu.AppendSeparator()
        # item_zoom_in = editor_menu.Append(wx.ID_ZOOM_IN, 'Zoom in\tCtrl+I')
        # item_zoom_out = editor_menu.Append(wx.ID_ZOOM_OUT, 'Zoom out\tCtrl+O')

        self.Bind(wx.EVT_MENU, self.handle_buttons, item_backward)
        self.Bind(wx.EVT_MENU, self.handle_buttons, item_forward)
        self.Bind(wx.EVT_MENU, self.handle_buttons, item_cut)
        self.Bind(wx.EVT_MENU, self.handle_buttons, item_copy)
        self.Bind(wx.EVT_MENU, self.handle_buttons, item_paste)
        # self.Bind(wx.EVT_MENU, self.handle_buttons, item_zoom_in)
        # self.Bind(wx.EVT_MENU, self.handle_buttons, item_zoom_out)

        self.Append(editor_menu, '&Edit')

    def enable_menu_save(self, status):
        self.Enable(wx.ID_SAVE, status)

    def enable_menu_undo(self, status):
        self.Enable(wx.ID_UNDO, status)

    def enable_menu_redo(self, status):
        self.Enable(wx.ID_REDO, status)

    def enable_copy_cut_past(self, status):
        self.Enable(wx.ID_CUT, status)
        self.Enable(wx.ID_COPY, status)
        self.Enable(wx.ID_PASTE, status)

    def toggle_status_bar(self, e):
        self.parent.toggle_status_bar(self.statusbar_check.IsChecked())

    def toggle_tool_bar(self, e):
        self.parent.toggle_tool_bar(self.toolbar_check.IsChecked())

    def handle_buttons(self, event):
        self.parent.handle_menu_button(event)
