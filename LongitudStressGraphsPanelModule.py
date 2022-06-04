import wx
from wx.lib.pubsub import pub 
from SolveModule import GrowTask
import numpy as np
import matplotlib.figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

class LongitudStressGraphsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        pub.subscribe(self.plotResults, "DataToPlot")

        gr = wx.GridBagSizer(5, 5)

        explanation = "LongitudStressGraphsPanel"
        text = wx.StaticText(self, label=explanation)

        self.figure1 = matplotlib.figure.Figure()
        self.axes1 = self.figure1.add_subplot(1, 1, 1)
        self.canvas1 = FigureCanvasWxAgg(self, -1, self.figure1)

        self.figure2 = matplotlib.figure.Figure()
        self.axes2 = self.figure2.add_subplot(1, 1, 1)
        self.canvas2 = FigureCanvasWxAgg(self, -1, self.figure2)

        gr.Add(text, pos=(0,0), span=(1,2), flag= wx.EXPAND | wx.LEFT | wx.RIGHT)
        gr.Add(self.canvas1, pos=(1,0))
        gr.Add(self.canvas2, pos=(1,1))

        self.SetSizer(gr)
        self.Layout()

    def plotResults(self, message):
        solution = message
        self.axes1.clear()
        self.axes2.clear()

        spacialLongitudStresses = solution.getSpacialStresses()['Longitudinal stress']
        materialLongitudStresses = solution.getMaterialStresses()['Longitudinal stress']

        dr_s = solution.getMaterialStresses()['step'] 
        dr_m = solution.getSpacialStresses()['step'] 

        oldRadii = solution.getSpatialRadius()['Old radii'] 
        newRadii = solution.getMaterialRadius()['New radii'] 

        R = np.linspace(oldRadii[0], oldRadii[-1], num=len(materialLongitudStresses), endpoint=True)  #np.arange(oldRadii[0], oldRadii[-1]+dr_s/10, dr_s) 
        r = np.linspace(newRadii[0], newRadii[-1], num=len(spacialLongitudStresses), endpoint=True) #np.arange(newRadii[0], newRadii[-1]+dr_m/10, dr_m) 

        self.axes1.plot(R, materialLongitudStresses, label='material longitud stresses')
        self.axes1.set_xlabel('R')
        self.axes1.set_ylabel('LongitudSigma(R)')

        self.axes2.plot(r, spacialLongitudStresses, label='spacial longitud stresses')
        self.axes2.set_xlabel('r')
        self.axes2.set_ylabel('LongitudSigma(r)')

        pub.sendMessage("logOutputPrint", message='material and spatial longitud stresses were plotted\n')

        self.axes1.legend()
        self.axes2.legend()

        self.canvas1.draw()
        self.canvas2.draw()