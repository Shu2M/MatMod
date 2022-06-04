from email import message
import wx
from wx.lib.pubsub import pub 

class ModelPanel(wx.Panel):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent)

        gr = wx.GridBagSizer(5, 5)
        textSize = (60, 20)

        self.staticTextR = wx.StaticText(self, label='R')
        

        self.staticTextGammar = wx.StaticText(self, label='gamma_r')
        

        self.staticTextGammat = wx.StaticText(self, label='gamma_t')
        

        self.staticTextGammaz = wx.StaticText(self, label='gamma_z')
        

        self.staticTextMu = wx.StaticText(self, label='mu')
        

        self.staticTextN = wx.StaticText(self, label='N')
        

        self.staticTextP = wx.StaticText(self, label='P')
        

        self.solveButton = wx.Button(self, id=wx.ID_ANY, label="Solve")
        gr.Add(self.solveButton, pos=(7, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.Bind(wx.EVT_BUTTON, self.onSolve)

        self.SetSizer(gr)

    def onSolve(self, event):       
        dataMessage = {'Gamma_r_list': [], 
                       'Gamma_t_list': [],
                       'Gamma_z_list': [],
                       'A_list': [], 
                       'mu': 0,
                       'N': 0,
                       'P': 0}
        #logOutputPrint DataToSolve
        pub.sendMessage("logOutputPrint", message='start solving\n')
        pub.sendMessage("DataToSolve", message=dataMessage)
        

