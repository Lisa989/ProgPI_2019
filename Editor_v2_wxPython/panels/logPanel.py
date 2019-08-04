import wx, sys


class LogPanel (wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.SetBackgroundColour("BLUE")
        # Add a panel so it looks the correct on all platforms

        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        self.__log = wx.TextCtrl(self, wx.ID_ANY, size=(300, 100), style=style)

        # Add widgets to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__log, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer)

        # redirect text here
        sys.stdout = self.__log
        #sys.stderr = self.__log
