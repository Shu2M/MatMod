import wx
from wx.lib.pubsub import pub 

class LogPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.logText = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_RICH)
        pub.subscribe(self.outputPrint, "logOutputPrint")

        # expanding the log on all panel
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.logText, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        self.SetSizer(sizer)

    def outputPrint(self, message):
        self.logText.AppendText(str(message))