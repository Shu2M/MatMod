from email import message
import wx
from wx.lib.pubsub import pub 
from SolveModule import GrowTask

class ModelPanel(wx.Panel):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent)

        gr = wx.GridBagSizer(5, 5)
        textSize = (60, 20)

        self.staticTextR = wx.StaticText(self, label='R')
        gr.Add(self.staticTextR, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowR1 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowR1, pos=(0, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowR2 = wx.TextCtrl(self, size=textSize, value='2')
        gr.Add(self.inputWindowR2, pos=(0, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextGammar = wx.StaticText(self, label='gamma_r')
        gr.Add(self.staticTextGammar, pos=(1, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammar1 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammar1, pos=(1, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextGammat = wx.StaticText(self, label='gamma_t')
        gr.Add(self.staticTextGammat, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammat1 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammat1, pos=(2, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextGammaz = wx.StaticText(self, label='gamma_z')
        gr.Add(self.staticTextGammaz, pos=(3, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammaz1 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammaz1, pos=(3, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextMu = wx.StaticText(self, label='mu')
        gr.Add(self.staticTextMu, pos=(4, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowMu = wx.TextCtrl(self, size=textSize, value='70')
        gr.Add(self.inputWindowMu, pos=(4, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextN = wx.StaticText(self, label='N')
        gr.Add(self.staticTextN, pos=(5, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowN = wx.TextCtrl(self, size=textSize, value='10')
        gr.Add(self.inputWindowN, pos=(5, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextP = wx.StaticText(self, label='P')
        gr.Add(self.staticTextP, pos=(6, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowP = wx.TextCtrl(self, size=textSize, value='20')
        gr.Add(self.inputWindowP, pos=(6, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.solveButton = wx.Button(self, id=wx.ID_ANY, label="Solve")
        gr.Add(self.solveButton, pos=(7, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.Bind(wx.EVT_BUTTON, self.onSolve)

        self.staticText = wx.StaticText(self, label='R num')
        gr.Add(self.staticText, pos=(8, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.numberRadius = wx.SpinCtrl(self, value='2', min=2, max=10)
        gr.Add(self.numberRadius, pos=(8,2))

        self.SetSizer(gr)

    def onSolve(self, event): 
        pub.sendMessage("logOutputPrint", message='start solving\n')     
        solution = GrowTask([self.inputWindowGammar1.GetValue()],
                            [self.inputWindowGammat1.GetValue()],
                            [self.inputWindowGammaz1.GetValue()],
                            [float(self.inputWindowR1.GetValue()), float(self.inputWindowR2.GetValue())],
                            float(self.inputWindowMu.GetValue()),
                            float(self.inputWindowN.GetValue()),
                            float(self.inputWindowP.GetValue()))
        pub.sendMessage("logOutputPrint", message='solving completed succsesful\n')

        pub.sendMessage("DeleteCheckBoxes", message=True)
        pub.sendMessage("CheckBoxNumber", message=self.numberRadius.GetValue())

        pub.sendMessage("DataToPlot", message=solution)
        

