from email import message
from matplotlib.pyplot import flag
import wx
from wx.lib.pubsub import pub 
from SolveModule import GrowTask
import wx.grid as grid

class TableDialog(wx.Dialog):
    def __init__(self, parent, rowNameList, colNameList, *args, **kw):
        super().__init__(parent, *args, **kw)
        self.parent = parent
        self.rowNameList = rowNameList
        self.colNameList = colNameList

        self.grid = grid.Grid(self)
        self.grid.CreateGrid(len(rowNameList), len(colNameList))
        i = 0
        for rowName in rowNameList:
            self.grid.SetRowLabelValue(i, (rowName))
            i += 1
        i = 0
        for colName in colNameList:
            self.grid.SetColLabelValue(i, (colName))
            i += 1

        #for i in range(len(rowNameList)):
            #for j in range(len(colNameList)):
                #self.grid.SetCellValue(i, j, '0')
    
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        if self.rowNameList[0] == 'R':
            #self.parent.radii_list
            editor = self.grid.GetCellEditor(0, 0)
            message = 'kjkj'#editor.GetValue()
            print()
            pub.sendMessage("logOutputPrint", message=f'{message}<- if\n')
        else:
            #self.parent.gamma_r 
            #self.parent.gamma_t
            #self.parent.gamma_z
            pub.sendMessage("logOutputPrint", message='else\n')
            pass
        self.Destroy()

class ModelPanel(wx.Panel):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent)

        #self.gamma_r = []
        #self.gamma_t = []
        #self.gamma_z = []
        #self.radii_list = []

        gr = wx.GridBagSizer(5, 5)
        textSize = (60, 20)

        self.staticTextR = wx.StaticText(self, label='R')
        gr.Add(self.staticTextR, pos=(0, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowR1 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowR1, pos=(0, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowR2 = wx.TextCtrl(self, size=textSize, value='2')
        gr.Add(self.inputWindowR2, pos=(0, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowR3 = wx.TextCtrl(self, size=textSize, value='3')
        gr.Add(self.inputWindowR3, pos=(0, 4), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextGammar = wx.StaticText(self, label='gamma_r')
        gr.Add(self.staticTextGammar, pos=(1, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammar1 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammar1, pos=(1, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammar2 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammar2, pos=(1, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextGammat = wx.StaticText(self, label='gamma_t')
        gr.Add(self.staticTextGammat, pos=(2, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammat1 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammat1, pos=(2, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammat2 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammat2, pos=(2, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

        self.staticTextGammaz = wx.StaticText(self, label='gamma_z')
        gr.Add(self.staticTextGammaz, pos=(3, 0), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammaz1 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammaz1, pos=(3, 2), flag=wx.TOP | wx.LEFT | wx.BOTTOM)
        self.inputWindowGammaz2 = wx.TextCtrl(self, size=textSize, value='1')
        gr.Add(self.inputWindowGammaz2, pos=(3, 3), flag=wx.TOP | wx.LEFT | wx.BOTTOM)

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
        gr.Add(self.solveButton, pos=(7, 0), flag=wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.onSolve, self.solveButton)

        #self.staticText = wx.StaticText(self, label='Number of shells')
        #gr.Add(self.staticText, pos=(8, 0), flag=wx.EXPAND | wx.ALL)
        #self.numberRadius = wx.SpinCtrl(self, value='2', min=2, max=10)
        #gr.Add(self.numberRadius, pos=(8,2))

        #self.setRadiiButton = wx.Button(self, id=wx.ID_ANY, label="Set shell radii")
        #self.Bind(wx.EVT_BUTTON, self.setRadii, self.setRadiiButton)
        #gr.Add(self.setRadiiButton, pos=(9,0), flag=wx.EXPAND)

        #self.setGammaButton = wx.Button(self, id=wx.ID_ANY, label="Set gamma")
        #self.Bind(wx.EVT_BUTTON, self.setGamma, self.setGammaButton)
        #gr.Add(self.setGammaButton, pos=(10,0), flag=wx.EXPAND)

        self.SetSizer(gr)

    def onSolve(self, event): 
        pub.sendMessage("logOutputPrint", message='start solving\n')     
        solution = GrowTask([self.inputWindowGammar1.GetValue(), self.inputWindowGammar1.GetValue()],
                            [self.inputWindowGammat1.GetValue(), self.inputWindowGammat1.GetValue()],
                            [self.inputWindowGammaz1.GetValue(), self.inputWindowGammaz1.GetValue()],
                            [float(self.inputWindowR1.GetValue()), float(self.inputWindowR2.GetValue()), float(self.inputWindowR3.GetValue())],
                            float(self.inputWindowMu.GetValue()),
                            float(self.inputWindowN.GetValue()),
                            float(self.inputWindowP.GetValue()))
        if solution.IsSolved():
            pub.sendMessage("logOutputPrint", message='solving completed succsesful\n')

        pub.sendMessage("DeleteCheckBoxes", message=True)
        pub.sendMessage("CheckBoxNumber", message=3)

        pub.sendMessage("DataToPlot", message=solution)
    '''    
    def setRadii(self, event):
        pub.sendMessage("logOutputPrint", message='good 1\n')
        colNameList = [f'{i+1} shell' for i in range(self.numberRadius.GetValue())]
        dialogTable = TableDialog(self, rowNameList=['R'], colNameList=colNameList, title="Set shell radii")
        dialogTable.ShowModal()

    def setGamma(self, event):
        pub.sendMessage("logOutputPrint", message='good 2\n')
        colNameList = [f'{i+1} layer' for i in range(self.numberRadius.GetValue()-1)]
        dialogTable = TableDialog(self, rowNameList=['gamma r', 'gamma t', 'gamma z'], colNameList=colNameList, title="Set shell radii")
        dialogTable.ShowModal()
    '''
