import wx
from LogPanelModule import LogPanel
from TopPanelModule import TopPanel
from wx.lib.pubsub import pub 

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent=parent, title=title, size=(900, 700))

        self.CreateStatusBar() # a status bar in the bottom of the window

        # settin up the file menu 
        fileMenu = wx.Menu()
        fileMenuItemAbout = fileMenu.Append(wx.ID_ABOUT, "&About", "Information about the programm")
        fileMenuItemExit = fileMenu.Append(wx.ID_EXIT, "&Exit", "Terminate the programm")
        self.Bind(wx.EVT_MENU, self.onAbout, fileMenuItemAbout)
        self.Bind(wx.EVT_MENU, self.onExit, fileMenuItemExit)

        # create the menu bar and add on main window
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        
        # divide the window into two panels
        splitter = wx.SplitterWindow(self)
        topPanel = TopPanel(splitter)
        logPanel = LogPanel(splitter)
        #logPanel.SetMaximumSize(100)
        splitter.SplitHorizontally(topPanel, logPanel)
        splitter.SetMinimumPaneSize(550)
        
        self.Show(True)

    def onAbout(self, event):
        message = '>> Text about this programm\n'
        pub.sendMessage("logOutputPrint", message=message)

    def onExit(self, event):
        self.Close(True)
