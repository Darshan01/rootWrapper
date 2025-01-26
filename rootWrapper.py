import ROOT

class graph():
    def __init__(self, name, title, nbins, xlow, xup, data=[], 
                xTitle = "", yTitle = "Counts", ylow = 0, yhigh = None,
                lineColor = ROOT.kBlack, markerStyle = ROOT.kFullDotLarge, 
                markerColor = ROOT.kBlack, scale = 1, binErrorOption = None,
                includeErrors = False, errorAsym = False, errorValues = None, 
                errorHigh = None, errorLow = None, suppressXError = True,
                errorLineColor = ROOT.kBlack, errorFillColor = ROOT.kBlack,
                errorFillStyle = 3003):
        
        self.name = name
        self.title = title
        self.nbins = nbins
        self.xlow = xlow
        self.xup = xup
        self.data = data
        self.xTitle = xTitle
        self.yTitle = yTitle
        self.ylow = ylow
        self.yhigh = yhigh
        self.lineColor = lineColor
        self.markerStyle = markerStyle
        self.markerColor = markerColor
        self.scale = scale
        self.binErrorOption = binErrorOption
        self.includeErrors = includeErrors
        self.errorAsym = errorAsym
        self.errorValues = errorValues
        self.errorHigh = errorHigh
        self.errorLow = errorLow
        self.suppressXError = suppressXError
        self.errorLineColor = errorLineColor
        self.errorFillColor = errorFillColor
        self.errorFillStyle = errorFillStyle
        
        self.histo = ROOT.TH1D(self.name, self.title, self.nbins, self.xlow, self.xup)
        self.plots = [self.histo]
        self.stack = None
        
        self.fill(data)
        
        self.setXTitle(xTitle)
        self.setYTitle(yTitle)
        
        self.setYHigh(yhigh)
        self.setYLow(ylow)
        
        if binErrorOption != None:
            self.histo.SetBinErrorOption(binErrorOption)
        
        self.histo.SetLineColor(lineColor)
        self.histo.SetMarkerStyle(markerStyle)
        self.histo.SetMarkerColor(markerColor)
        
        if includeErrors:
            if errorAsym:
                
                self.plots.append(ROOT.TGraphAsymmErrors(self.plots[0]))
                
                if (errorHigh is None or errorLow is None) and binErrorOption is None:
                    print("Error: errorHigh and errorLow must be set if errorAsym is True, or binErrorOption must be set")
                    exit(1)
                
                if binErrorOption is not None:
                    if errorHigh is not None or errorLow is not None: print("Warning: binErrorOption is set, errorHigh and errorLow will be ignored")
                else:
                    self.setErrors(errorValues, errorHigh, errorLow)
                
                if self.suppressXError: self.setXErrorAsym()
                
            else:
                self.plots.append(ROOT.TGraphErrors(self.plots[0]))
                
                if errorValues is None and binErrorOption is None:
                    print("Error: errorValues must be set if errorAsym is False, or binErrorOption must be set")
                    exit(1)

                if binErrorOption is not None:
                    print(binErrorOption)
                    if errorValues is not None: print("Warning: binErrorOption is set, errorValues will be ignored")

                else:
                    self.setErrors(errorValues)
            
            self.plots[1].SetLineColor(errorLineColor)
            self.plots[1].SetFillColor(errorFillColor)
            self.plots[1].SetFillStyle(errorFillStyle)
        
        
        
    def fill(self, data):
        if(len(data) == 0):
            return 
        
        for i in range(self.nbins):
            self.histo.SetBinContent(i+1, self.scale * data[i])
        
        self.setYHigh(self.yhigh)
        self.setYLow(self.ylow)
    
    def setXTitle(self, xTitle):
        if(xTitle == ""):
            return
        
        self.histo.GetXaxis().SetTitle(xTitle)
    
    def setYTitle(self, yTitle):
        if(yTitle == ""):
            return
        
        self.histo.GetYaxis().SetTitle(yTitle)
    
    def setYHigh(self, yhigh):
        if yhigh == None and len(self.data) != 0:
            self.yhigh = 1.2*max(self.data)
            self.histo.SetAxisRange(self.ylow, 1.2*max(self.data), "Y")
        elif yhigh != None:
            self.yhigh = yhigh
            self.histo.SetAxisRange(self.ylow, yhigh, "Y")
    
    def setYLow(self, ylow):
        self.ylow = ylow
        self.histo.SetAxisRange(ylow, self.yhigh, "Y")
    
    def setYRange(self, ylow, yhigh):
        self.setYLow(ylow)
        self.setYHigh(yhigh)
    
    def setErrors(self, errorValues = None, errorHigh = None, errorLow = None):
        if self.includeErrors:
            
            graph = self.plots[1]
            if self.errorAsym:
                for i in range(self.nbins):
                    graph.SetPointEYhigh(i, errorHigh[i])
                    graph.SetPointEYlow(i, errorLow[i])
            else:
                for i in range(self.nbins):
                    if self.suppressXError: graph.SetPointError(i, 0, errorValues[i])
                    else: graph.SetPointError(i, 1, errorValues[i])
                    
            
        else:
            print("Error: includeErrors is set to False, errors cannot be set")
            exit(1)
    
    def setXErrorAsym(self, xErrorHigh = None, xErrorLow = None):
        
        if not self.suppressXError:
            if xErrorHigh is not None and xErrorLow is not None:
                for i in range(self.nbins):
                    self.plots[1].SetPointEXhigh(i, xErrorHigh[i])
                    self.plots[1].SetPointEXlow(i, xErrorLow[i])
            else:
                for i in range(self.nbins):
                    self.plots[1].SetPointEXhigh(i, 0.5)
                    self.plots[1].SetPointEXlow(i, 0.5)
        
        else:
            if xErrorHigh is not None and xErrorLow is not None:
                print("Warning: xErrorHigh and xErrorLow were provided, suppressXError will be set to False")
                self.suppressXError = False
                self.setXErrorAsym(xErrorHigh, xErrorLow)
            for i in range(self.nbins):
                self.plots[1].SetPointEXhigh(i, 0)
                self.plots[1].SetPointEXlow(i, 0)
    
    def getHisto(self):
        return self.plots[0]
    
    def getErrorGraph(self):
        if self.includeErrors:
            return self.plots[1]
        else:
            print("Error: includeErrors is set to False, error graph does not exist")
            exit(1)
            
    def draw(self, histOption = "HIST", errorOption = "SAME E0"):
        self.drawHisto(histOption)
        
        if self.includeErrors:
            self.drawError(errorOption)
    
    def drawHisto(self, histOption = "HIST"):
        self.plots[0].Draw(histOption)
    
    def drawError(self, errorOption = "SAME E0"):
        if self.includeErrors:
            self.plots[1].Draw(errorOption)
        else:
            print("Error: includeErrors is set to False, error graph does not exist")
            exit(1)