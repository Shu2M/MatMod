import wx
from wx.lib.pubsub import pub 
from SolveModule import GrowTask
import numpy as np
import matplotlib.figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

class ResultsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent)
        pub.subscribe(self.plotResults, "DataToSolve")
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.figure = matplotlib.figure.Figure()

        self.axes = self.figure.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
        self.canvas.SetMaxSize((600, 600))
        vbox.Add(self.canvas, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetSizer(vbox)
        self.Layout()

    def plotResults(self, message):
        solution = GrowTask(message['Gamma_r_list'], 
                            message['Gamma_t_list'], 
                            message['Gamma_z_list'], 
                            message['A_list'], 
                            message['mu'],
                            message['N'],
                            message['P'])
        pub.sendMessage("logOutputPrint", message='solving completed succsesful\n')

        self.axes.clear()

        dataDictr = solution.getMaterialRadius()
        t = np.linspace(0, 2*np.pi, num=100)
        j = 0
        for R, r in zip(message['A_list'], dataDictr['r']):
            self.axes.plot(R*np.cos(t), R*np.sin(t), linestyle='--', label=f'R{j+1}')
            self.axes.plot(r*np.cos(t), r*np.sin(t), linestyle='-', label=f'r{j+1}')
            j += 1

        self.axes.legend()
        self.canvas.draw()
        pub.sendMessage("logOutputPrint", message='results ploted\n')

        



        