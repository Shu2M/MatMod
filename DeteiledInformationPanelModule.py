import wx
from wx.lib.pubsub import pub 
from SolveModule import GrowTask
import numpy as np
import matplotlib.figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

class DeteiledInformationPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        pub.subscribe(self.setSolution, "DeteiledInformation")
        self.frame = parent

        hbox = wx.GridBagSizer(5, 5)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        hbox.Add(self.vbox, pos=(0,0))
        self.SetSizer(hbox)

    def setSolution(self, message):
        solution = message
        self.removeText()

        new_inner_r = f"New inner radius: {solution.getMaterialRadius()['r'][0]}"
        new_outer_r = f"New outer radius: {solution.getMaterialRadius()['r'][-1]}"
        ax_strech = f"Axial stretch: {solution.getAxialStretch()}"
        min_mr_stress = f"Minimal material stress: {solution.getMaterialStresses()['Minimal radial stress']}"
        max_mr_stress = f"Maximal material stress: {solution.getMaterialStresses()['Maximal radial stress']}"
        min_sr_stress = f"Minimal spatial stress: {solution.getSpacialStresses()['Minimal radial stress']}"
        max_sr_stress = f"Maximal spatial stress: {solution.getSpacialStresses()['Maximal radial stress']}"
        min_mt_stress = f"Minimal material stress: {solution.getMaterialStresses()['Minimal tangential stress']}"
        max_mt_stress = f"Maximal material stress: {solution.getMaterialStresses()['Maximal tangential stress']}"
        min_st_stress = f"Minimal spatial stress: {solution.getSpacialStresses()['Minimal tangential stress']}"
        max_st_stress = f"Maximal spatial stress: {solution.getSpacialStresses()['Maximal tangential stress']}"
        min_ml_stress = f"Minimal material stress: {solution.getMaterialStresses()['Minimal longitudinal stress']}"
        max_ml_stress = f"Maximal material stress: {solution.getMaterialStresses()['Maximal longitudinal stress']}"
        min_sl_stress = f"Minimal spatial stress: {solution.getSpacialStresses()['Minimal longitudinal stress']}"
        max_sl_stress = f"Maximal spatial stress: {solution.getSpacialStresses()['Maximal longitudinal stress']}"
        overall_min = f"Overall minimum: {solution.getSpacialStresses()['Overall minimum']}"
        overall_max = f"Overall miximum: {solution.getSpacialStresses()['Overall maximum']}"

        self.vbox.Add(wx.StaticText(self, label=new_inner_r))
        self.vbox.Add(wx.StaticText(self, label=new_outer_r))
        self.vbox.Add(wx.StaticText(self, label=ax_strech))
        self.vbox.Add(wx.StaticText(self, label=min_mr_stress))
        self.vbox.Add(wx.StaticText(self, label=max_mr_stress))
        self.vbox.Add(wx.StaticText(self, label=min_sr_stress))
        self.vbox.Add(wx.StaticText(self, label=max_sr_stress))
        self.vbox.Add(wx.StaticText(self, label=min_mt_stress))
        self.vbox.Add(wx.StaticText(self, label=max_mt_stress))
        self.vbox.Add(wx.StaticText(self, label=min_st_stress))
        self.vbox.Add(wx.StaticText(self, label=max_st_stress))
        self.vbox.Add(wx.StaticText(self, label=min_ml_stress))
        self.vbox.Add(wx.StaticText(self, label=max_ml_stress))
        self.vbox.Add(wx.StaticText(self, label=min_sl_stress))
        self.vbox.Add(wx.StaticText(self, label=max_sl_stress))
        self.vbox.Add(wx.StaticText(self, label=overall_min))
        self.vbox.Add(wx.StaticText(self, label=overall_max))
        self.frame.Fit()
        

    def removeText(self):
        if self.vbox.GetChildren():
            for i in range(9):
                self.vbox.Hide(0)
                self.vbox.Remove(0)
            self.frame.Fit()