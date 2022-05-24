import wx
from MainWindowModule import MainWindow

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(parent=None, title="CGC (version 1.0)")
    frame.Show()
    app.MainLoop()