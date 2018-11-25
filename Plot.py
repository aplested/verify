import random
import math
import sys
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *
    
from PlotParam import PlotParam

__author__="Andrew"
__date__ ="$22-Nov-2018 12:52:01$"

class Plot:
    'Displays a plot in a Window.'
    def __init__(self):
        self.createFrame()
    
    def addTitle(self, text):
        self.root.title(text)
    
    def real2Pix(self, x, y):
        'Converts real world coordinates into graph pixel coordinates'
        self.xScaleDbl = float(self.xMaxPix - self.xMinPix) / (self.xAxis[-1] - self.xAxis[0])
        xpix = int(self.xMinPix + self.xScaleDbl * x)
        
        #yScaleDbl should be a negative number because pixels increase as real signal goes negative
        #yAxis counts from large to small
        #datum of y is in the middle of axis
        self.yScaleDbl = float(self.yMaxPix - self.yMinPix) / (self.yAxis[-1] - self.yAxis[0])
        ypix = int(float(self.yMaxPix - self.yMinPix) / 2 + self.yMinPix + self.yScaleDbl * y)
        #print (self.yMaxPix, self.yMinPix, self.yScaleDbl, xpix, ypix)
        return xpix, ypix
    
    def prep2DPlot(self, xData, yData):
        self.root.title("2D Plot")
        self.xData = xData
        self.yData = yData
        
        self.xAxisTitle = "Current"

        #this should be plot specific
        self.yAxisTitle = "Variance"
        
        #data limits
        self.ymin = min(yData)
        self.ymax = max(yData)
        self.xmax = max(xData)
        self.xmin = min(xData)
        
        self.createAxes()
    
    def prepTracePlot(self, trace):
        self.root.title("Trace")
        self.trace = trace
        plotType = 0
        
        xAxisTitle = []
        xAxisTitle.append('Points')
        
        self.xAxisTitle = xAxisTitle[plotType]
        #this should be plot specific
        self.yAxisTitle = "Current"
        
        #data limits
        self.ymin = min(trace)
        self.ymax = max(trace)
        self.xmax = len (trace)
        self.xmin = 0
    
        self.createAxes()
    
    def createFrame(self):
        'Creates frame for plot'

        self.root = Tk()
        self.root.resizable(width='FALSE', height='FALSE')    # should make window not resizable
        cwidth = 600
        cheight = 350
        self.c = Canvas(self.root, width=cwidth, height=cheight, bg= 'white')
        self.c.grid(row=0, column=0, columnspan=2)

        #these are the corner pixels of the graph (L to R, Top to Bottom)
        self.xMinPix = int(cwidth * 15 / 100)
        self.xMaxPix = int(cwidth * 95 / 100)
        self.yMinPix = int(cheight * 5 / 100)
        self.yMaxPix = int(cheight * 85 / 100)
    
    def createAxes(self):
        #to do this properly, we need to know the data limits
        #to make expressions below shorter
        xMinPix = self.xMinPix
        xMaxPix = self.xMaxPix
        yMaxPix = self.yMaxPix
        yMinPix = self.yMinPix
        
        self.xAxis = range(int(self.xmin), int(self.xmax), int(self.xmax / 5))
        yAxisMin = int((self.ymax - self.ymin) * -1.25)
        yAxisMax = int((self.ymax - self.ymin) * 1.25)
        #yAxis counts from max to min in negative steps
        self.yAxis = range(yAxisMax, yAxisMin, -int(float(yAxisMax - yAxisMin) / 5))
        print (self.yAxis, self.ymin, self.ymax)

        # x Axis
        self.c.create_line(xMinPix, yMaxPix, xMaxPix, yMaxPix, width=2)    # axis at bottom
        
        for tick in self.xAxis:
            px, py = self.real2Pix(tick, self.yAxis[-1])
            self.c.create_line(px, py, px, py + 5, width=2)
            self.c.create_text(px, py + 15, text='%i'% tick)
        
        self.c.create_text(int(xMaxPix / 1.9), yMaxPix + 30, text=self.xAxisTitle, font=("Helvetica", "12"))

        # y Axis
        self.c.create_line(xMinPix, yMinPix, xMinPix, yMaxPix,  width=2)

        for tick in self.yAxis:
            px, py = self.real2Pix(self.xAxis[0], tick)
            self.c.create_line(px, py, px-5, py, width=2)
            self.c.create_text(px - 25, py, text='%i'% tick)
        
        self.c.create_text(xMinPix - 50, yMaxPix - 150, text=self.yAxisTitle, font=("Helvectica", "12"), angle=90)
        
    def draw2D(self):
        r = 2
        for i in range(len(self.xData)):
            px, py = self.real2Pix(self.xData[i], self.yData[i])
            self.c.create_oval(
                               px - r,
                               py - r,
                               px + r,
                               py + r,
                               width=1,
                               outline='DarkSlateBlue',
                               fill='SteelBlue'
                               )

    def drawTrace(self):
        #using Fred Sigworth's speed trick of only drawing one point per horizontal pixel
        npt = 300
        r = 2
        for i in range(0, self.xmax, int(float(self.xmax) / npt)):
            px, py = self.real2Pix(i, self.trace[i])
            self.c.create_oval(
                                  px - r,
                                  py - r,
                                  px + r,
                                  py + r,
                                  width=1,
                                  outline='DarkSlateBlue',
                                  fill='SteelBlue'
                                  )
            # put the y value above each bar
            #c.create_text(x0+2, y1, anchor=tk.SW, text=str(self.freq[i]))
        print (px, py)
        # draw small triangle arrow at particular x
        """xArrDbl = mean
        xArr = xMinPix + int((float(xArrDbl)-xMinDbl) * xScaleDbl)
        c.create_line(xArr, yMinPix, xArr-5, yMinPix+10, width=2, fill="blue")
        c.create_line(xArr, yMinPix, xArr+5, yMinPix+10, width=2, fill="blue")
        c.create_line(xArr+5, yMinPix+10, xArr-5, yMinPix+10, width=2, fill="blue")
        """

        b1 = Button(self.root, text="REPLOT", command=self.callback1, state=DISABLED)
        b1.grid(row=1, column=0)
        b2 = Button(self.root, text="Save ASCII", command=self.callback2, state=DISABLED)
        b2.grid(row=1, column=1)
        
        self.root.mainloop()

    def callback1(self):
        'Called by REPLOT button.'

        params = DistPlotParam(self.root)
        xmin1 = params.xmin
        xmax1 = params.xmax
        dx = params.dx
        ymax2 = params.ymax
        """
        xaxis = self.createBins(xmin1, nbin, dx)
        ymax1, freq = self.sortRand(self.rand, xaxis)
        self.createFrame(xaxis, freq, ymax2, self.mean, self.xAxisTitle1)
        """

    def callback2(self):
        'Called by Save ASCII button.'
        pass


        

if __name__ == "__main__":
    randX = []
    nran = 5000
    for i in range(nran):
        u = random.randint(0,10)
        randX.append(u)
    C = PlotTrace(nran, 1)
    C.drawTrace()
