import wx
from ModelPanelModule import ModelPanel
from ResultsPanelModule import ResultsPanel

class TopPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        
        # creating nnotebook with 2 tabs (sizer is needed)
        notebook = wx.Notebook(self)
        notebook.AddPage(ModelPanel(notebook), "Model")
        notebook.AddPage(ResultsPanel(notebook), "Results")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)