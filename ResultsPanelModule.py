import wx
from RadiiGraphsPanelModule import RadiiGraphsPanel
from RadialStressGraphsPanelModule import RadialStressGraphsPanel
from TangentialStressGrahpsPanelModule import TangentialStressGrahpsPanel
from LongitudStressGraphsPanelModule import LongitudStressGraphsPanel


class ResultsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        
        # creating nnotebook with 4 tabs (sizer is needed)
        notebook = wx.Notebook(self)
        notebook.AddPage(RadiiGraphsPanel(notebook), "Radii")
        notebook.AddPage(RadialStressGraphsPanel(notebook), "Radial stresses")
        notebook.AddPage(TangentialStressGrahpsPanel(notebook), "Tangential stresses")
        notebook.AddPage(LongitudStressGraphsPanel(notebook), "Longitudinal stresses")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)