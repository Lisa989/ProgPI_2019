import wx
from Editor_v2_wxPython.panels.p4_editorPanel import EditorPanel
from Editor_v2_wxPython.panels.p4_toolPanel import ToolPanel
from costanti.editor_v2_wxPython_costanti import WINDOW_WIDTH, SCREEN_WIDTH

SPLIITER_FLAG = wx.SP_3D | wx.SP_NO_XP_THEME | wx.SP_LIVE_UPDATE


class ScreenPanel(wx.SplitterWindow):
    def __init__(self, parent, **k):
        wx.SplitterWindow.__init__(self, parent, style=SPLIITER_FLAG, **k)
        self.enable_tool = parent.enable_tool
        self.enable_redo = parent.enable_redo
        self.enable_undo = parent.enable_undo
        self.enable_copy_cut_paste = parent.enable_copy_cut_paste
        self.statusbar_set_text = parent.statusbar_set_text
        self.parent = parent

        self.toolPanel = ToolPanel(self)
        self.editorPanel = EditorPanel(self)

        # self.Bind(wx.EVT_SIZE, self.on_size)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.toolPanel, 1, flag=wx.EXPAND | wx.CENTRE)
        hbox.Add(self.editorPanel, 1, flag=wx.EXPAND | wx.CENTRE)
        self.SetSizerAndFit(hbox)

        self.SplitVertically(self.toolPanel, self.editorPanel)
        self.SetMinimumPaneSize(WINDOW_WIDTH - SCREEN_WIDTH)

    def get_brick_select(self):
        """
        Trova il tipo e il colore selezionato
        :return: (type, color) selezionati
        """
        type = self.toolPanel.brickTypePanel.get_select_type()
        color = self.toolPanel.brickColorPanel.get_select_color()
        return type, color

    def on_size(self, event):
        event.Skip()
        self.Refresh()
