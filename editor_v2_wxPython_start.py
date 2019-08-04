import wx
from Editor_v2_wxPython.panels.p1_mainFrame import MainFrame
from costanti.editor_v2_wxPython_costanti import WINDOW_HEIGHT, WINDOW_WIDTH
from Editor_v2_wxPython.editor_risorse import Immagini, Icone


class App(wx.App):
    def OnInit(self):
        Immagini.load()
        Icone.load()
        self.frame = MainFrame(None, "MyArkanoidEditor", (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.frame.Show()
        self.SetTopWindow(self.frame)

        return True


if __name__ == "__main__":
    app = App()
    app.MainLoop()
