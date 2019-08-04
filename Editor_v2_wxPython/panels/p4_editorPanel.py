import wx
from Editor_v2_wxPython.editor import Editor

class EditorPanel(wx.Panel):
    """
     crea un pannello per l'editor dove inserisce la scrolledWindow.
     è necessario in quanto la scrolledWindow per funzionare deve essere posizionata in un pannello intero e non in parte di esso
     """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.enable_tool = parent.enable_tool
        self.enable_redo = parent.enable_redo
        self.enable_undo = parent.enable_undo
        self.enable_copy_cut_paste = parent.enable_copy_cut_paste
        self.statusbar_set_text = parent.statusbar_set_text
        self.get_brick_select = parent.get_brick_select

        self.editor_win = Editor(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.editor_win, 1, wx.CENTER | wx.EXPAND, 0)
        self.SetSizer(sizer)
