import wx
from Editor_v2_wxPython.panels.p3_screenPanel import ScreenPanel
from Editor_v2_wxPython.elements.toolBar import ToolBar
from Editor_v2_wxPython.panels.logPanel import LogPanel
from costanti.editor_v2_wxPython_costanti import DEBUG

TB_FLAG = wx.TB_FLAT | wx.TB_HORIZONTAL | wx.TB_HORZ_TEXT


class MainPanel(wx.Panel):
    def __init__(self, parent, ):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.statusbar_set_text = parent.statusbar_set_text

        # crea la toolbar
        self.toolbar = ToolBar(self)
        self.toolbar.enable_tool_item(False)
        self.toolbar.enable_undo(False)
        self.toolbar.enable_redo(False)
        self.toolbar.enable_copy_cut_paste(False)
        self.screenPanel = ScreenPanel(self)

        # posiziona toolbar e screenPanel
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.toolbar, 0, wx.TOP | wx.EXPAND)
        vbox.Add(self.screenPanel, 1, wx.BOTTOM | wx.EXPAND)

        if DEBUG:
            self.logPanel = LogPanel(self)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(vbox, 5, wx.EXPAND | wx.LEFT)
            hbox.Add(self.logPanel, 1, wx.EXPAND | wx.RIGHT)
            self.SetSizerAndFit(hbox)
        else:
            self.SetSizerAndFit(vbox)

    def on_quit(self, event):
        event.Skip()

    def enable_copy_cut_paste(self, status):
        self.toolbar.enable_copy_cut_paste(status)
        self.parent.enable_menu_copy_cut_past(status)

    def enable_tool(self, status):
        self.toolbar.enable_tool_item(status)
        self.parent.enable_menu_save(status)

    def enable_redo(self, status):
        self.toolbar.enable_redo(status)
        self.parent.enable_menu_redo(status)

    def enable_undo(self, status):
        self.toolbar.enable_undo(status)
        self.parent.enable_menu_undo(status)

    def handle_tool_button(self, event):
        id_bt = event.GetId()
        editor_win = self.screenPanel.editorPanel.editor_win
        if id_bt == wx.ID_EXIT:
            self.parent.on_quit(event)
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
