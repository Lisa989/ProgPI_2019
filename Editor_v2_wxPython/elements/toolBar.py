import wx
from Editor_v2_wxPython.editor_risorse import Icone

TB_FLAG = wx.TB_FLAT | wx.TB_HORIZONTAL | wx.TB_HORZ_TEXT


class ToolBar(wx.ToolBar):
    """
        crea la toolbar
    """
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, style=TB_FLAG)
        self.parent = parent

        self.init_file_tool()
        self.init_edit_tool()
        self.init_mode_tool()

        self.Realize()

    def init_file_tool(self,):
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_EXIT, 'Quit', Icone.quit))
        self.AddSeparator()
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_NEW, 'New', Icone.new))
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_OPEN, 'Open', Icone.open))
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_SAVE, 'Save', Icone.save))
        self.AddSeparator()

    def init_edit_tool(self):
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_CLEAR, 'Clear', Icone.clear))
        self.AddSeparator()
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_COPY, 'Copy', Icone.copy))
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_CUT, 'Cut', Icone.cut))
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_PASTE, 'Paste', Icone.paste))
        self.AddSeparator()
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_UNDO, 'Undo', Icone.undo))
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_REDO, 'Redo', Icone.redo))
        self.AddSeparator()
        # self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_ZOOM_OUT, 'Zoom in', icon_zom_in))
        # self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddTool(wx.ID_ZOOM_IN, 'Zoom out', icon_zoom_out))
        # self.AddSeparator()

    def init_mode_tool(self):
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddRadioTool(wx.ID_ADD, 'Edit', Icone.edit))
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddRadioTool(wx.ID_MOVE_FRAME, 'Move', Icone.move))
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddRadioTool(wx.ID_DELETE, 'Delete', Icone.delete))
        self.Bind(wx.EVT_TOOL, self.handle_buttons, self.AddRadioTool(wx.ID_SELECTALL, 'Select', Icone.select))

    def enable_tool_item(self, status):
        self.EnableTool(wx.ID_SAVE, status)
        self.EnableTool(wx.ID_CLEAR, status)

        self.EnableTool(wx.ID_ADD, status)
        self.EnableTool(wx.ID_MOVE_FRAME, status)
        self.EnableTool(wx.ID_SELECTALL, status)
        self.EnableTool(wx.ID_DELETE, status)

    def enable_undo(self, status):
        self.EnableTool(wx.ID_UNDO, status)

    def enable_redo(self, status):
        self.EnableTool(wx.ID_REDO, status)

    def enable_copy_cut_paste(self, status):
        self.EnableTool(wx.ID_CUT, status)
        self.EnableTool(wx.ID_COPY, status)
        self.EnableTool(wx.ID_PASTE, status)

    def handle_buttons(self, event):
        self.parent.handle_tool_button(event)
