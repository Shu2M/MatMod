import wx
from wx.lib.pubsub import pub 
from SolveModule import GrowTask
import numpy as np
import matplotlib.figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

class LongitudStressGraphsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        pub.subscribe(self.plotResults, "DataToSolve")

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
        solution = GrowTask(message['Gamma_r_list'], 
                            message['Gamma_t_list'], 
                            message['Gamma_z_list'], 
                            message['A_list'], 
                            message['mu'],
                            message['N'],
                            message['P'])