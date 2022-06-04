import wx
from wx.lib.pubsub import pub 
import numpy as np
import matplotlib.figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg

class RadiiGraphsPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        self.checkBoxNumber = 0
        self.graphsR = []
        self.graphsr = []
        self.checkBoxes = []

        pub.subscribe(self.plotResults, "DataToPlot")
        pub.subscribe(self.makeCheckBoxes, "CheckBoxNumber")
        pub.subscribe(self.deleteCheckBoxes, "DeleteCheckBoxes")
        
        self.gr = wx.GridBagSizer(5, 5)
        self.widgetSizer = wx.GridBagSizer(5, 5)

        explanation = "RadiiGraphsPanel"
        text = wx.StaticText(self, label=explanation)

        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvasWxAgg(self, -1, self.figure)

        self.gr.Add(text, pos=(0,0), span=(1,2), flag= wx.EXPAND | wx.LEFT | wx.RIGHT)
        self.gr.Add(self.canvas, pos=(1,0))
        self.gr.Add(self.widgetSizer, pos=(1,1))
        self.SetSizer(self.gr)


    def deleteCheckBoxes(self, message):
        if self.widgetSizer.GetChildren():
            while self.checkBoxNumber > 0:
                self.widgetSizer.Hide(self.checkBoxNumber-1)
                self.widgetSizer.Remove(self.checkBoxNumber-1)
                self.checkBoxNumber -= 1
            self.checkBoxes = []
            self.frame.Fit()


    def makeCheckBoxes(self, message):
        self.checkBoxNumber = message
        for i in range(self.checkBoxNumber):
            label = f"{i+1} shell"
            newCheckBox = wx.CheckBox(self, label=label)
            newCheckBox.SetValue(True)
            self.checkBoxes.append(newCheckBox)
            self.widgetSizer.Add(newCheckBox, pos=(i, 0))
        updateButton = wx.Button(self, wx.ID_ANY, "Update")
        self.Bind(wx.EVT_BUTTON, self.updateResults, updateButton)
        self.widgetSizer.Add(updateButton, pos=(self.checkBoxNumber, 0))
        self.frame.Fit()


    def plotResults(self, message):
        solution = message
        self.axes.clear()

        datar = solution.getMaterialRadius()
        dataR = solution.getSpatialRadius()
        t = np.linspace(0, 2*np.pi, num=100)

        j = 0
        for R, r in zip(dataR['Old radii'], datar['New radii']):
            self.graphsR.append(self.axes.plot(R*np.cos(t), R*np.sin(t), linestyle='--', label=f'R{j+1}'))
            self.graphsr.append(self.axes.plot(r*np.cos(t), r*np.sin(t), linestyle='-', label=f'r{j+1}'))
            j += 1

        self.updateResults(None)
        pub.sendMessage("logOutputPrint", message='radiuses plotted\n')


    def updateResults(self, event):
        i = 1
        for checkBox, axisR, axisr in zip(self.checkBoxes, self.graphsR, self.graphsr):
            if checkBox.GetValue():
                axisR[0].set_visible(True)
                axisR[0].set_label(f'R{i}')

                axisr[0].set_visible(True)
                axisr[0].set_label(f'r{i}')
            else:
                axisR[0].set_visible(False)
                axisR[0].set_label(None)

                axisr[0].set_visible(False)
                axisr[0].set_label(None)

            i += 1

        self.axes.legend()
        self.canvas.draw()
        pub.sendMessage("logOutputPrint", message='results on the radii panel was updated\n')