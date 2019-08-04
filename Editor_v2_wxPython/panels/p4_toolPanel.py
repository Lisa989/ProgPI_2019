import wx
from Editor_v2_wxPython.panels.p5_brickColorPanel import BrickColorPanel
from Editor_v2_wxPython.panels.p5_brickTypePanel import BrickTypePanel
from costanti.editor_v2_wxPython_costanti import BUTTON_HEIGHT

SPLIITER_FLAG = wx.SP_3D | wx.SP_NO_XP_THEME | wx.SP_LIVE_UPDATE


class ToolPanel(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, style=SPLIITER_FLAG)
        self.SetDoubleBuffered(True)
        self.statusbar_set_text = parent.statusbar_set_text

        self.brickTypePanel = BrickTypePanel(self)
        self.brickColorPanel = BrickColorPanel(self)

        sizerV = wx.BoxSizer(wx.VERTICAL)
        self.SetSizerAndFit(sizerV)
        sizerV.Add(self.brickTypePanel, 1, flag=wx.EXPAND | wx.TOP | wx.CENTER)
        sizerV.Add(self.brickColorPanel, 1, flag=wx.EXPAND | wx.BOTTOM | wx.CENTER)

        self.SplitHorizontally(self.brickTypePanel, self.brickColorPanel)
        self.SetMinimumPaneSize(BUTTON_HEIGHT * 3)
