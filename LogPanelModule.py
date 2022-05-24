import wx
from wx.lib.pubsub import pub 

class LogPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.logText = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_RICH)
        pub.subscribe(self.outputPrint, "logOutputPrint")

        # expanding the log on all panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.logText, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)

    def outputPrint(self, message):
        self.logText.AppendText(message)