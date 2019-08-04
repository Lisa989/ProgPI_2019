import wx
from Editor_v2_wxPython.panels.p2_mainPanel import MainPanel
from Editor_v2_wxPython.elements.menuBar import MenuBar


class MainFrame(wx.Frame):
    def __init__(self, parent, title, size=(700, 600)):
        wx.Frame.__init__(self, parent, -1)
        # self.Maximize(True)
        self.parent = parent
        # status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        #init menubar
        self.__menubar = MenuBar(self)
        self.SetMenuBar(self.__menubar)
        self.__menubar.enable_menu_save(False)
        self.__menubar.enable_copy_cut_past(False)
        self.__menubar.enable_menu_redo(False)
        self.__menubar.enable_menu_undo(False)

        self.enable_menu_copy_cut_past = self.__menubar.enable_copy_cut_past
        self.enable_menu_redo = self.__menubar.enable_menu_redo
        self.enable_menu_undo = self.__menubar.enable_menu_undo
        self.enable_menu_save = self.__menubar.enable_menu_save

        # posiziona mainPanel
        self.mainPanel = MainPanel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        sizer.Add(self.mainPanel, 1, wx.ALL | wx.EXPAND)

        # bind event
        self.Bind(wx.EVT_CLOSE, self.on_quit)
        self.Bind(wx.EVT_SIZE, self.on_size)

        # init window
        self.SetTitle(title)
        self.SetMinSize((700, 600))
        self.SetSize(size)
        self.Centre()

    def toggle_status_bar(self, status):
        if status:
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def toggle_tool_bar(self, status):
        if status:
            self.mainPanel.toolbar.Show()
        else:
            self.mainPanel.toolbar.Hide()

    def statusbar_set_text(self, txt):
        self.statusbar.SetStatusText(txt)

    """
    --------------------------------------------------------------------------------------------------------------------
    *********************************************--GESTIONE--***********************************************************
    **********************************************--EVENTI--***********************************************************
    --------------------------------------------------------------------------------------------------------------------
    """

    def on_quit(self, event):
        answer = wx.MessageBox("Chiudere il programma?", "Conferma", wx.YES_NO | wx.CANCEL, self)
        if answer == wx.YES:
            self.statusbar_set_text("MI STO CHIUDENDO")
            self.Destroy()
        else:
            event.Veto()

    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def handle_menu_button(self, event):
        id_bt = event.GetId()
        editor_win = self.mainPanel.screenPanel.editorPanel.editor_win
        if id_bt == wx.ID_EXIT:
            self.on_quit(event)
        elif id_bt == wx.ID_NEW:
            editor_win.on_click_new(event)
        elif id_bt == wx.ID_OPEN:
            editor_win.on_click_open(event)
        elif id_bt == wx.ID_SAVE:
            editor_win.on_click_save(event)
        elif id_bt == wx.ID_CLEAR:
            editor_win.on_click_clear(event)
        elif id_bt == wx.ID_UNDO:
            editor_win.on_click_undo(event)
        elif id_bt == wx.ID_REDO:
            editor_win.on_click_redo(event)
        elif id_bt == wx.ID_CUT:
            editor_win.on_click_cut(event)
        elif id_bt == wx.ID_COPY:
            editor_win.on_click_copy(event)
        elif id_bt == wx.ID_PASTE:
            editor_win.on_click_paste(event)
        # elif id_bt == wx.ID_ZOOM_IN:
        # editor_win.on_click_zoom_in(event)
        # elif id_bt == wx.ID_ZOOM_OUT:
        # editor_win.on_click_zoom_out(event)
        elif id_bt == wx.ID_ADD:
            editor_win.on_click_edit_mode(event)
        elif id_bt == wx.ID_DELETE:
            editor_win.on_click_delete_mode(event)
        elif id_bt == wx.ID_MOVE_FRAME:
            editor_win.on_click_move_mode(event)
        elif id_bt == wx.ID_SELECTALL:
            editor_win.on_click_select_mode(event)

