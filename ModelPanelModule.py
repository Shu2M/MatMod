from email import message
import wx
from wx.lib.pubsub import pub 

class ModelPanel(wx.Panel):
    def __init__(self, parent):
        global inputWindowR1, inputWindowR2
        global inputWindowGammar1, inputWindowGammar2
        global inputWindowGammat1, inputWindowGammat2
        global inputWindowGammaz1, inputWindowGammaz2
        global inputWindowZeta


        wx.Frame.__init__(self, parent=parent)

        verticalBox = wx.BoxSizer(wx.VERTICAL)

        staticTextR = wx.StaticText(self, label='R')
        inputWindowR1 = wx.TextCtrl(self)
        inputWindowR2 = wx.TextCtrl(self)
        horizontalBoxR = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxR.Add(staticTextR, flag=wx.RIGHT, border=8)
        horizontalBoxR.Add(inputWindowR1)
        horizontalBoxR.Add(inputWindowR2)

        staticTextGammar = wx.StaticText(self, label='gamma_r')
        inputWindowGammar1 = wx.TextCtrl(self)
        inputWindowGammar2 = wx.TextCtrl(self)
        horizontalBoxGammar = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxGammar.Add(staticTextGammar, flag=wx.RIGHT, border=8)
        horizontalBoxGammar.Add(inputWindowGammar1)
        horizontalBoxGammar.Add(inputWindowGammar2)

        staticTextGammat = wx.StaticText(self, label='gamma_t')
        inputWindowGammat1 = wx.TextCtrl(self)
        inputWindowGammat2 = wx.TextCtrl(self)
        horizontalBoxGammat = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxGammat.Add(staticTextGammat, flag=wx.RIGHT, border=8)
        horizontalBoxGammat.Add(inputWindowGammat1)
        horizontalBoxGammat.Add(inputWindowGammat2)

        staticTextGammaz = wx.StaticText(self, label='gamma_z')
        inputWindowGammaz1 = wx.TextCtrl(self)
        inputWindowGammaz2 = wx.TextCtrl(self)
        horizontalBoxGammaz = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxGammaz.Add(staticTextGammaz, flag=wx.RIGHT, border=8)
        horizontalBoxGammaz.Add(inputWindowGammaz1)
        horizontalBoxGammaz.Add(inputWindowGammaz2)

        staticTextZeta = wx.StaticText(self, label='zeta')
        inputWindowZeta = wx.TextCtrl(self)
        horizontalBoxZeta = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxZeta.Add(staticTextZeta, flag=wx.RIGHT, border=8)
        horizontalBoxZeta.Add(inputWindowZeta)

        solveButton = wx.Button(self, id=wx.ID_ANY, label="Solve", size=(70,30))
        horizontalBoxSolveButton = wx.BoxSizer(wx.HORIZONTAL)
        horizontalBoxSolveButton.Add(solveButton, flag=wx.RIGHT, border=8)
        self.Bind(wx.EVT_BUTTON, self.onSolve)

        verticalBox.Add(horizontalBoxR, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        verticalBox.Add(horizontalBoxGammar, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        verticalBox.Add(horizontalBoxGammat, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        verticalBox.Add(horizontalBoxGammaz, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        verticalBox.Add(horizontalBoxZeta, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        verticalBox.Add(horizontalBoxSolveButton, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        self.SetSizer(verticalBox)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(12)
        self.SetFont(font)

    def onSolve(self, event):       
        r1 = inputWindowR1.GetValue()
        r2 = inputWindowR2.GetValue()

        gammar1 = inputWindowGammar1.GetValue()
        gammar2 = inputWindowGammar2.GetValue()

        gammat1 = inputWindowGammat1.GetValue()
        gammat2 = inputWindowGammat2.GetValue()

        gammaz1 = inputWindowGammaz1.GetValue()
        gammaz2 = inputWindowGammaz2.GetValue()

        zeta = inputWindowZeta.GetValue()
        
        message = f"r1 = {r1}\nr2 = {r2}\ngamma_r1 = {gammar1}\n"
        pub.sendMessage("logOutputPrint", message=message)
