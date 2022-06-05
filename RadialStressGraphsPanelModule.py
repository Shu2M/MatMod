import wx
from wx.lib.pubsub import pub 
import numpy as np
import matplotlib.figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import math

class RadialStressGraphsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        pub.subscribe(self.plotResults, "DataToPlot")

        gr = wx.GridBagSizer(5, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.figure1 = matplotlib.figure.Figure(figsize=(4, 4))
        self.axes1 = self.figure1.add_subplot(1, 1, 1)
        self.canvas1 = FigureCanvasWxAgg(self, -1, self.figure1)

        self.figure2 = matplotlib.figure.Figure(figsize=(4, 4))
        self.axes2 = self.figure2.add_subplot(1, 1, 1)
        self.canvas2 = FigureCanvasWxAgg(self, -1, self.figure2)

        hbox.Add(self.canvas1, flag=wx.EXPAND|wx.ALL, border=5)
        hbox.Add(self.canvas2, flag=wx.EXPAND|wx.ALL, border=5)
        gr.Add(hbox, pos=(1,0), flag=wx.EXPAND | wx.LEFT | wx.RIGHT)

        self.SetSizer(gr)
        self.Layout()

    def plotResults(self, message):
        solution = message
        self.axes1.clear()
        self.axes2.clear()

        spacialRadialStresses = solution.getSpacialStresses()['Radial stress']
        materialRadialStresses = solution.getMaterialStresses()['Radial stress']

        dr_s = solution.getMaterialStresses()['step'] 
        dr_m = solution.getSpacialStresses()['step'] 

        oldRadii = solution.getSpatialRadius()['Old radii'] 
        newRadii = solution.getMaterialRadius()['New radii'] 

        R = np.linspace(oldRadii[0], oldRadii[-1], num=len(materialRadialStresses), endpoint=True)  #np.arange(oldRadii[0], oldRadii[-1]+dr_s/10, dr_s) 
        r = np.linspace(newRadii[0], newRadii[-1], num=len(spacialRadialStresses), endpoint=True) #np.arange(newRadii[0], newRadii[-1]+dr_m/10, dr_m) 

        self.axes1.plot(R, materialRadialStresses, label='RadialSigma(R)')
        self.axes1.set_xlabel('R')

        self.axes2.plot(r, spacialRadialStresses, label='RadialSigma(r)')
        self.axes2.set_xlabel('r')

        pub.sendMessage("logOutputPrint", message='>> Radial stresses were plotted\n')

        self.axes1.legend()
        self.axes2.legend()

        self.canvas1.draw()
        self.canvas2.draw()
