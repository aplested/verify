import random
import math
import sys
from tkinter import *
from tkinter import filedialog  # Per salvare il file

from PlotParam import PlotParam

__author__ = "Andrew"
__date__ = "$22-Nov-2018 12:52:01$"

class Plot:
    """Displays a plot in a Tkinter frame."""

    def __init__(self, host):
        self.createFrame(host)

        # Create buttons for each plot but disable them initially
        self.b1 = Button(host, text="Replot", command=self.callback1, state=DISABLED)
        self.b2 = Button(host, text="Save Pic", command=self.callback2, state=DISABLED)
        self.b1.grid(row=1, column=0)
        self.b2.grid(row=1, column=1)
        
        # nothing plotted yet so we don't know what kind of plot it is
        self.is2DPlot = False
        self.isTracePlot = False

    def addTitle(self, title):
        """Add a title to the plot."""
        self.c.create_text(220, 15, text=title)

    def real2Pix(self, x, y):
        """Convert real world coordinates into graph pixel coordinates."""
        if not hasattr(self, 'xAxis') or not self.xAxis:
            return 0, 0

        xScaleDbl = (self.xMaxPix - self.xMinPix) / (self.xAxis[-1] - self.xAxis[0] + 1e-6)
        xpix = int(self.xMinPix + xScaleDbl * (x - self.xAxis[0]))

        yScaleDbl = (self.yMaxPix - self.yMinPix) / (self.yAxis[-1] - self.yAxis[0] + 1e-6)
        ypix = int(self.yMaxPix + yScaleDbl * (y - self.yAxis[-1]))

        return xpix, ypix

    def prep2DPlot(self, xData, yData):
        """Prepare for 2D plotting, taking account of data."""
        self.xData = [abs(x) for x in xData]
        self.yData = yData

        self.xAxisTitle = "Current"
        self.yAxisTitle = "Variance"

        self.ymin, self.ymax = min(self.yData), max(self.yData)
        self.xmin, self.xmax = min(self.xData), max(self.xData)

        self.createAxes()
        self.activateButtons()
        self.is2DPlot = True

    def prepTracePlot(self, trace):
        """Prepare to plot a trace, taking account of data."""
        self.trace = trace
        self.xAxisTitle = "Points"
        self.yAxisTitle = "Current"

        self.ymin, self.ymax = min(trace), max(trace)
        self.xmin, self.xmax = 0, len(trace)

        self.createAxes()
        self.activateButtons()
        self.isTracePlot = True

    def createFrame(self, host):
        """Create frame for plot."""
        cwidth, cheight = 400, 300
        self.c = Canvas(host, width=cwidth, height=cheight, bg='white')
        self.c.grid(row=0, column=0, columnspan=2)

        self.xMinPix, self.xMaxPix = int(cwidth * 0.15), int(cwidth * 0.95)
        self.yMinPix, self.yMaxPix = int(cheight * 0.10), int(cheight * 0.85)

    def createAxes(self):
        """Draw the axes."""
        if self.xmax == self.xmin:
            self.xmax += 1

        if self.ymax == self.ymin:
            self.ymax += 1

        step_x = max(1, int((self.xmax - self.xmin) / 5))
        self.xAxis = range(int(self.xmin), int(self.xmax) + 1, step_x)

        yAxisMin = int(1.5 * self.ymin - 0.5 * self.ymax)
        yAxisMax = int(0.5 * self.ymin + 1.5 * self.ymax)

        step_y = max(1, int((yAxisMax - yAxisMin) / 5))
        self.yAxis = range(yAxisMax, yAxisMin - 1, -step_y)

        # Draw X-axis
        self.c.create_line(self.xMinPix, self.yMaxPix, self.xMaxPix, self.yMaxPix, width=2)
        for tick in self.xAxis:
            px, py = self.real2Pix(tick, self.yAxis[-1])
            self.c.create_line(px, py, px, py + 5, width=2)
            self.c.create_text(px, py + 15, text='%i' % tick)

        self.c.create_text(int(self.xMaxPix / 1.9), self.yMaxPix + 30, text=self.xAxisTitle, font=("Helvetica", "12"))

        # Draw Y-axis
        self.c.create_line(self.xMinPix, self.yMinPix, self.xMinPix, self.yMaxPix, width=2)
        for tick in self.yAxis:
            px, py = self.real2Pix(self.xAxis[0], tick)
            self.c.create_line(px, py, px - 5, py, width=2)
            self.c.create_text(px - 25, py, text='%i' % tick)

        self.c.create_text(self.xMinPix - 50, self.yMaxPix - 100, text=self.yAxisTitle, font=("Helvetica", "12"),
                           angle=90)

    def draw2D(self):
        """Draw a 2D plot."""
        r = 2
        for i in range(len(self.xData)):
            px, py = self.real2Pix(abs(self.xData[i]), self.yData[i])
            self.c.create_oval(px - r, py - r, px + r, py + r, width=1, outline='DarkSlateBlue', fill='SteelBlue')

    def drawTrace(self):
        """Draw a trace plot."""
        r, npt = 2, 300
        step = max(1, int(self.xmax / npt))
        for i in range(0, self.xmax, step):
            px, py = self.real2Pix(i, self.trace[i])
            self.c.create_oval(px - r, py - r, px + r, py + r, width=1, outline='Green', fill='Green')

    def activateButtons(self):
        """Activate buttons when data is loaded."""
        self.b1.config(state=NORMAL)
        self.b2.config(state=NORMAL)

    def callback1(self):
        """Called by REPLOT button."""
        self.limits = [self.xmin, self.xmax, self.ymin, self.ymax]
        params = PlotParam(self.b1, limits = self.limits)
        self.xmin, self.xmax = params.xmin, params.xmax
        #self.dx = params.dx
        self.ymin, self.ymax = params.ymin, params.ymax
        
        # delete original
        self.c.delete("all")
        self.createAxes()
        
        if self.is2DPlot:
            self.draw2D()
            
        elif self.isTracePlot:
            self.drawTrace()
     

    def callback2(self):
        """Called by Save Pic button."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
        if file_path:
            self.c.postscript(file=file_path + ".ps", colormode='color')
            print(f"Plot saved as {file_path}")

