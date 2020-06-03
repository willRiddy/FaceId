import wx

class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 1000))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        #Setting up the menu
        filemenu = wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")

        # Set events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        #Creating the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the menu bar
        self.SetMenuBar(menuBar) # Adding the menu bar ot the frame content
        self.Show(True)

    def OnAbout(self,e):
        # A message dialog box with an Ok button. wx.OK is a standard ID in wxWidgets
        dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self,e):
        self.Close(True)

app = wx.App(False)
frame = MyFrame(None, 'Small editor')
app.MainLoop()