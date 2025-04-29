import sys
import os.path
import platform
import copy
from datetime import datetime
#import itertools

#PySide2 imports
from PySide2 import QtCore, QtGui
from PySide2.QtCore import Slot
from PySide2 import __version__ as pyside_version
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QMessageBox, QFileDialog, QAction, QGroupBox, QHBoxLayout, QRadioButton, QDialog, QVBoxLayout, QCheckBox, QButtonGroup, QFrame

#package imports
#import numpy as np
#import pandas as pd
#from scipy import __version__ as scipy_version
#import scipy.signal as scsig
#from openpyxl import Workbook
#from openpyxl.utils.dataframe import dataframe_to_rows

#verify imports
import file_tools
from trace_tools import decimate_traces
from Plot import *
from noise import *

#Import pg last to avoid namespace-overwrite problems?
import pyqtgraph as pg

__author__="Andrew"
__date__ ="$29-Apr-2025$"

#not sure if we need this
class QHLine(QFrame):
    ### from https://stackoverflow.com/questions/5671354
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class VerifyMainWindow(QMainWindow):
    
    ### Methods
    ###
    ### createMenu                  : make menubar
    ### about                       : About the app
    ### getStarted                  : a help file for novices
    ### createPlotWidgets           : build the plots

    ### mouseMoved                  : when the mouse moves in zoom

    ### manualPeakToggle            :
    ### fitParabola                 : fitting parabolic function to the data
    ###

    
    def __init__(self, *args, **kwargs):
        super(VerifyMainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Verify 0.5 - Non-Stationary Noise Analysis")
        self.central_widget = QWidget()
        self.central_layout = QGridLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)
        self.resize(1500,800)           # works well on MacBook Retina display
        
        #self.conditions = []                    # conditions will be sheet names from xlsx
        #self.datasetList_CBX = ['-']            # maintain our own list of datasets from the combobox
        #self.extPa = {}                         # external parameters for the peak scraping dialog
        #self.dataLock = True                    # when manual peak editing, lock to trace data
        #self.noPeaks = True                     # were any peaks found yet?
        #self.fitHistogramsOption = False        # histograms are not fitted by default, checkbox -> False later
        #self.saveHistogramsOption = False       # histograms are not saved by default,  checkbox -> False later
        
        # setup main window widgets and menus
        self.createPlotWidgets()
        self.createControlsWidgets()
        self.createMenu()
        #self.toggleDataSource = False
        
        
    def createMenu(self):
        # Skeleton menu commands
        
        self.file_menu = self.menuBar().addMenu("File")
        self.analysis_menu = self.menuBar().addMenu("Analysis")
        self.help_menu = self.menuBar().addMenu("Help")
        
        self.file_menu.addAction("About Verify", self.about) #this actually goes straight into the Verify menu, why?
        self.file_menu.addAction("Open File", self.open_file)
        self.file_menu.addAction("Save Data", self.save_peaks)
        
        self.analysis_menu.addAction("fit parabola", self.fitParabola)
        
        self.help_menu.addAction("Getting Started", self.getStarted)
    
    
    def about(self):
        QMessageBox.about (self, "About Verify",
        """ ----*- VERIFY {0} -*----
        \nVerify and analyse repeated time-series variance
        \nAndrew Plested NIH, FMP- and HU-Berlin 2006-2025
        \nThis application can analyse variance in electrophysiological data
        \nIt makes heavy use of PyQtGraph ({5}, Luke Campagnola).
        \nPython {1}
        \nPySide2 {2} built on Qt {3}
        \nRunning on {4}
        """.format(__version__, platform.python_version(), pyside_version, QtCore.__version__, platform.platform(), pg.__version__))
    
        #pd.__version__, np.__version__, scipy_version,
    
    def modalWarning(self, s):
    
        QMessageBox.warning(self, 'Warning', s)
        #dlg.setWindowTitle("HELLO!")
        #dlg.exec_()
    
    
    def getStarted(self):
        
        introduction ="""
    ---- Verify fluctuations from ion channel noise in difference records ----\n
    according to expectation of not exceeding 7 SD\
    (from Heinemann and Conti 'Methods in Enzymology' 207).
    Takes input from tab-delimited Excel file 'file.txt' with columns being current traces.
    * Mean and variance are computed for the set to use in noise limit test.
    * Baseline noise is determined for each difference trace from the first hundred points (2 ms at 50 kHz)
    * Traces with extremely noisy baselines are removed.
    * Traces that exceed the 7 SD limit are removed and the failing points are explicitly listed to the terminal.
    Output is tab delimited text file with columns consisting of mean, variance and verified difference traces, default to 'verified.txt'
    """
        
        QMessageBox.information(self, "Getting Started", introduction)
        
    def plotVC(self):
        print ("plot Current variance")
    
    def fitParabola(self):
        print ("Fit parabola")
    
    def createPlotWidgets(self):
        """analysis plots"""
        
        # traces plot
        data = []
        self.plots = pg.GraphicsLayoutWidget()
        self.p1rc = (1,0)
        self.p1 = self.plots.addPlot(y=data, row=self.p1rc[0], col=self.p1rc[1], rowspan=3, colspan=1)
        self.p1.setTitle(title="Traces and background subtraction", color="F0F0F0", justify="right")
        self.p1.setLabel('left', "dF / F")
        self.p1.setLabel('bottom', "Time (s)")
        self.p1.vb.setLimits(xMin=0)
        #just a blank for now, populate after loading data to get the right number of split graphs
        self.p1stack = pg.GraphicsLayout()
        
                
        # what does this do??
        #self.p3.scene().sigMouseClicked.connect(self.clickRelay)
        #self.p3.sigMouseClicked.connect(self.clickRelay)
        
        
        self.plots.peakslabel = pg.LabelItem(text='', justify='left')
        
        
        self.central_layout.addWidget(self.plots, row=0, col=0, rowspan=1,colspan=2)
     
     

    
    
    
    
    def mouseMoved(self, evt):
        """Crosshair in p3 shown during manual fitting"""
        if self.autoPeaks == False:
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if self.p3.sceneBoundingRect().contains(pos):
                mousePoint = self.p3vb.mapSceneToView(pos)
                
                # there should be two plot data items, find the curve data
                _c = utils.findCurve(self.p3.items)
                sx, sy = _c.getData()
            
                # quantize x to curve, and get corresponding y that is locked to curve
                idx = np.abs(sx - mousePoint.x()).argmin()
                ch_x = sx[idx]
                ch_y = sy[idx]
                self.hLine.setPos(ch_y)
                self.vLine.setPos(ch_x)
                
                # print ("update label: x={:.2f}, y={:.2f}".format(ch_x, ch_y))
                self.plots.cursorlabel.setText("Cursor: x={: .2f}, y={: .3f}".format(ch_x, ch_y))
    
    

     
    def createControlsWidgets(self):
        """control panel"""
        
        controls = pg.LayoutWidget()
        
        actions = QGroupBox("Actions")
        actionsGrid = QGridLayout()
        
        # load dataset button
        loadDataBtn = QtGui.QPushButton('Load traces')
        loadDataBtn.clicked.connect(self.loadTraces)
        
        verifyTracesBtn = QtGui.QPushButton('Verify traces for variance')
        verifyTracesBtn.clicked.connect(self.verifyTraces)
        
        plotVCBtn = QtGui.QPushButton('Plot Variance vs. current')
        plotVCBtn.clicked.connect(self.plotVC)
               
        fitParabolaBtn = QtGui.QPushButton('Fit Parabola')
        fitParabolaBtn.clicked.connect(self.fitParabola)
        
        actionsGrid.addWidget(loadDataBtn, 1, 0)
        actionsGrid.addWidget(verifyTracesBtn, 2, 0)
        actionsGrid.addWidget(plotVCBtn, 3, 0)
        actionsGrid.addWidget(fitParabolaBtn, 4, 0)
        
        actions.setLayout(actionsGrid)
        
        
        histograms = QGroupBox("Histogram options")
        histGrid = QGridLayout()
        
        NBin_label = QtGui.QLabel("No. of bins")
        NBin_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.histo_NBin_Spin = pg.SpinBox(value=100, step=10, bounds=[0, 250], delay=0)
        self.histo_NBin_Spin.setFixedSize(60, 25)
        
        histGrid.addWidget(NBin_label, 2, 0)
        histGrid.addWidget(self.histo_NBin_Spin, 2, 1, 1, 2)
        
        d_divider = QHLine()
        d_divider.setFixedWidth(375)
        
        histGrid.addWidget(d_divider, 4, 0, 1, -1)
      
        histograms.setLayout(histGrid)
    
        # Baseline controls box
        baseline = QGroupBox("Automatic baseline cleanup")
        base_grid = QGridLayout()
        auto_bs_label = QtGui.QLabel("Baseline removal?")
        auto_bs_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.autobs_Box = pg.ComboBox()
        self.autobs_Box.addItems(['Auto', 'None', 'Lock'])
        self.autobs_Box.setFixedSize(70, 25)
  
        
        # parameters for the auto baseline algorithm
        auto_bs_lam_label = QtGui.QLabel("lambda")
        auto_bs_lam_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.auto_bs_lam_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.auto_bs_lam_slider.setTickPosition(QtGui.QSlider.TicksBothSides)
        self.auto_bs_lam_slider.setMinimum(2)
        self.auto_bs_lam_slider.setMaximum(9)
        self.auto_bs_lam_slider.setValue(6)
        self.auto_bs_lam_slider.setFixedSize(100, 25)
        #self.auto_bs_lam_slider.valueChanged.connect()   connect it to something
        
        
        base_grid.addWidget(auto_bs_label, 0, 0, 1, 2)
        base_grid.addWidget(self.autobs_Box, 0, 2, 1, 1)
        base_grid.addWidget(auto_bs_lam_label, 1, 3)
        base_grid.addWidget(self.auto_bs_lam_slider, 1, 4, 1, 2)
        
     
        baseline.setLayout(base_grid)
        
        
       
    
        #stack widgets into control panel
    
        baseline.setFixedHeight(150)
       
        histograms.setFixedHeight(150)
        
 
        controls.addWidget(baseline, 2, 0 , 1, -1)
        
        controls.addWidget(actions, 3, 0, 1, -1)
  
        controls.addWidget(histograms, 5 , 0, 1, -1)
        
        controls.setFixedWidth(420)
        
        self.central_layout.addWidget(controls, 0, 3, -1, 1)
        return
    
    def loadTraces(self):
        'Called by Load traces button'
        self.input_traces, self.dfile = self.read_Data('excel')
        #dfile contains source data path and filename
        if self.dfile != None:
            self.input_filename_label.set('Data loaded from ' + self.dfile)
            self.b4.config(state=NORMAL)    #turn on VERIFY button
            self.p.prepTracePlot(self.input_traces[0])
            self.p.addTitle("First trace in {}".format(self.dfile))
            self.p.drawTrace()
        else:
            self.input_filename_label.set('No data loaded')
    
    def verifyTraces(self):
        'Called by VERIFY button'
        #send traces to be checked
        print ("Verify")
        
        #results are stored in self.verified_output
        self.getResult()
        
        #default
        out_filename = "verified.txt"
        #determine filename option
        opt = self.v.get()
        
        if opt == 2:
            out_filename = self.getOutputFilename()
        elif opt == 1:
            out_filename = file_tools.addFilenamePrefix(self.dfile, prefix="v_")
        elif opt == 0:
            out_filename = file_tools.addFilenamePrefix(self.dfile, prefix=datetime.now().strftime("%y%m%d-%H%M%S") + "_v_")
        self.b5.config(state=NORMAL)
        #plot preview of current variance automatically
        self.pcv.prep2DPlot(self.meanI, self.ensVariance)
        self.pcv.addTitle("Preview of Current Variance Plot")
        self.pcv.draw2D()
        
        write_output (self.verified_output, self.output_header, out_filename)
    
    
    def resultsPopUp(self):
        """Make a pop up window of the current peak results"""
        _ROI = self.ROI_selectBox.currentText()
        _r = self.workingDataset.resultsDF.df[_ROI]
        #print (_r, type(_r))
        qmb = QDialog()
        qmb.setWindowTitle('Peaks from {}'.format(_ROI))
        qmb.setGeometry(1000,600,600,800)
        self.peaksText = QtGui.QTextEdit()
        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(12)
        self.peaksText.setCurrentFont(font)
        self.peaksText.setText(_r.to_string())
        self.peaksText.setReadOnly(True)
        
        #add buttons, make it the right size
        qmb.layout = QVBoxLayout()
        qmb.layout.addWidget(self.peaksText)
        qmb.setLayout(qmb.layout)
        qmb.exec_()
    

  
    def plotNewData(self):
        """Do some setup immediately after data is loaded"""
        
        _sel_condi = self.p3Selection.currentText()
        print ("Plot New Data with the p3 selector set for: ", _sel_condi)
        y = {}
        
        self.p1.clear()
        self.p3.clear()
        
        for i, _condi in enumerate(self.conditions):
            x = self.workingDataset.traces[_condi].index
            y[i] = self.workingDataset.traces[_condi].mean(axis=1).to_numpy()

            self.p1.plot(x, y[i], pen=(i,3))
        
            if _sel_condi == _condi:
                # curve
                self.p3.plot(x, y[i], pen=(i,3))
                
                if self.autoPeaks:
                    xp, yp = self.peaksWrapper(x, y[i], _condi)
                    
                else:
                    # if new data is loaded without autopeaks, there are no peaks....
                    # this goes wrong later on though
                    xp = np.array([])
                    yp = np.array([])
                
                # need to add something to p3 scatter
                self.p3.plot(xp, yp, name="Peaks "+_condi, pen=None, symbol="s", symbolBrush=(i,3))
                self.plots.peakslabel.setText("{} peaks in {} condition".format(len(yp), _condi))
                
                # create the object for parsing clicks in p3
                self.cA = clickAlgebra(self.p3)
                _p3_scatter = utils.findScatter(self.p3.items)
                if _p3_scatter:
                    _p3_scatter.sigClicked.connect(self.clickRelay)
                    _p3_scatter.sigPlotChanged.connect(self.manualUpdate)
        
        self.createLinearRegion()
        #return


    
    def manualUpdate(self):
        """Some editing was done in p3, so update other windows accordingly"""
        print ('Peak data in p3 changed manually')
       
        _sel_condi = self.p3Selection.currentText()
        _ROI = self.ROI_selectBox.currentText()
        
        # update the peaks in p1 and histograms only
        utils.removeAllScatter(self.p1, verbose=False)
        
        #update p2 histograms
        self.updateHistograms()
        
        for i, _condi in enumerate(self.conditions):
            #colours
            col_series = (i, len(self.conditions))
            
            if _sel_condi == _condi :
                _scatter = utils.findScatter(self.p3.items)
                # sometimes a new scatter is made and this "deletes" the old one
                # retrieve the current manually curated peak data
                if _scatter is None:
                    print ('No Scatter found, empty data.')
                    xp = []
                    yp = []
                else:
                    xp, yp = _scatter.getData()
                
                # write peaks into results
                self.workingDataset.resultsDF.addPeaks(_ROI, _sel_condi, xp, yp)
                # print (self.workingDataset.resultsDF.df[_ROI])
             
            xp, yp = self.workingDataset.resultsDF.getPeaks(_ROI, _condi)
            
            if self.split_traces:
                _target = self.p1stackMembers[i]
                # only one scatter item in each split view
                _t_scat = utils.findScatter(_target.items)
                _t_scat.setData(xp, yp, brush=col_series)
                
            else:
                self.p1.plot(xp, yp, pen=None, symbol="s", symbolBrush=col_series)
            
            self.plots.peakslabel.setText("{} peaks in {} condition.".format(len(yp), _condi))
                
        
    def setRanges(self):
        """ Collect the extremities of data over a set of conditions """
        self.ranges = {}
        # use the first condition (sheet) as a basis
        _df = self.workingDataset.traces[self.conditions[0]]
        self.ranges['xmin'] = _df.index.min()
        self.ranges['xmax'] = _df.index.max()
        self.ranges['ymin'] = _df.min().min()
        self.ranges['ymax'] = _df.max().max()
        
        # lazily compare across all conditions (including the first)
        for sheet in self.workingDataset.traces.values():
            if sheet.min().min() < self.ranges['ymin']:
                self.ranges['ymin'] = sheet.min().min()
            if sheet.max().max() > self.ranges['ymax']:
                self.ranges['ymax'] = sheet.max().max()
                
            if sheet.index.min() < self.ranges['xmin']:
                self.ranges['xmin'] = sheet.index.min()
            if sheet.index.max() > self.ranges['xmax']:
                self.ranges['xmax'] = sheet.index.max()
        return
    
    def save_peaks(self):
        print ("save extracted peak data and optionally histograms")
        
        # needs to be updated for openpyxl
        #format for header cells.
        #self.hform = {
        #'text_wrap': True,
        #'valign': 'top',
        #'fg_color': '#D5D4AC',
        #'border': 1}
        
        if self.noPeaks:        #nothing to save
            print ('Nothing to save, no peaks found yet!')
            return
        
        self.filename = QFileDialog.getSaveFileName(self,
        "Save Peak Data", os.path.expanduser("~"))[0]
        
        if self.filename:
            _wds = self.workingDataset
            wb = Workbook()
            
            # combine allowlist and excludelist dictionaries for output
            #_output = {**self.gpd.pk_extracted_by_condi, **self.gpd.excludelisted_by_condi}
            _allowedPeaks = {}
            _excludedPeaks = {}
            
            if _wds.resultsDF:
                _allowedPeaks = utils.decomposeRDF (_wds.resultsDF.df)
            if _wds.excludelisted:
                _excludedPeaks = utils.decomposeRDF (_wds.excludelisted.df)
            
            _output = {**_allowedPeaks, **_excludedPeaks}
            
            for _condi, _resultdf in _output.items():
                # in case there are duplicate peaks extracted, remove them and package into dummy variable
                # this syntax means : loc["not" the duplicates]
                _pe = _resultdf.loc[~_resultdf.index.duplicated(keep='first')] #StackOverflow 13035764
                
                wb.create_sheet(_condi)
                _wcs = wb[_condi]
                
                # write customised header
                for _num, _pcol in enumerate(_pe.columns.values):
                    _wcs.cell(1, _num + 1).value = _pcol + " " + _condi      #, header_format)
                    
                # write out data
                for _row in dataframe_to_rows(_pe, index=False, header=False):
                    _wcs.append(_row)
            
                #write index
                _wcs.insert_cols(1)
                for _num, _pin in enumerate(_pe.index.values):
                    _wcs.cell(1,1).value = "Time"
                    _wcs.cell(_num + 2, 1).value = _pin
            
            wb.remove(wb['Sheet'])
            
            if self.saveHistogramsOption:
                wb = self.save_histograms(wb)
            
            wb.save(self.filename)
            print ("Saved peaks from to workboook {}".format(self.filename))
          
            

        
    def save_baselined(self):
        # save baselined traces
        # No filtering so far
        print ("save_baselined data?")
        self.btfilename = QFileDialog.getSaveFileName(self,
        "Save Baselined ROI Data", os.path.expanduser("~"))[0]
        
        if self.btfilename:
            _wdsT = self.workingDataset.traces
            wb = Workbook()
            for _condi, _tdf in _wdsT.items():
                wb.create_sheet(_condi)
                _wcs = wb[_condi]
                
                # write customised header
                for _num, _pcol in enumerate(_tdf.columns.values):
                    _wcs.cell(1, _num + 1).value = _pcol + " " + _condi      #, header_format)
                    
                # write out data
                for _row in dataframe_to_rows(_tdf, index=False, header=False):
                    _wcs.append(_row)
            
                #write index
                _wcs.insert_cols(1)
                for _num, _pin in enumerate(_tdf.index.values):
                    _wcs.cell(1,1).value = "Time"
                    _wcs.cell(_num + 2, 1).value = _pin
            
            # was created at start
            
            wb.remove(wb['Sheet'])
            wb.save(self.btfilename)
            print ("Saved traces from to workboook {}".format(self.btfilename))
            
    def open_file(self):
        """Open a dialog to provide sheet names"""
        
        self.filename = QFileDialog.getOpenFileName(self,
            "Open Data", os.path.expanduser("~"))[0]
        
        if self.filename:
            """   #OLD WAY
                #very simple and rigid right now - must be an excel file with conditions
                #should be made generic - load all conditions into dictionary of dataframes no matter what
            with pg.ProgressDialog("Loading conditions...", 0, len(self.conditions)) as dlg:
                _traces = {}
                for _sheet in self.conditions:
                    dlg += 1
                    try:
                        _traces[_sheet] = pd.read_excel(self.filename, sheet_name=_sheet, index_col=0)
                        print ("XLDR: From spreadsheet- {}\n{}".format(_sheet, _traces[_sheet].head()))
                    except:
                        print ("Probably: XLDR error- no sheet named exactly {0}. Please check it.".format(_sheet))
                        self.conditions.remove(_sheet)
                # decide if there is data or not
            """
            
            # Now as a oneliner
            #"None" reads all the sheets into a dictionary of data frames
            _traces = pd.read_excel(self.filename, None, index_col=0)
        
        else:
            print ("file dialog failed")
            return
        
        self.conditions = list(_traces.keys())
        
        print ("Loaded following conditions: ", self.conditions)
        
        if self.workingDataset.isEmpty:
            print ("First data set loaded")
        
        else:
            #store existing working dataset
            self.store.storeSet(copy.copy(self.workingDataset))
            print ("Putting {} in the store.".format(self.workingDataset.DSname))
        
        # overwrite current working set
        self.workingDataset.addTracesToDS(_traces)
        self.workingDataset.isEmpty = False
        _stem = utils.getFileStem(self.filename)
        self.workingDataset.setDSname(_stem)
    
        _DSname = str(self.workingDataset.getDSname())
   
        _duplicate = self.updateDatasetComboBox(_DSname)
        #returns either false or the name to avoid duplicates
        
        #print ("4 {}".format(self.workingDataset.__dict__))
        if _duplicate:
            # update
            self.workingDataset.DSname = _duplicate
        
        self.workingDataset.ROI_list = ["Mean", "Variance"]
        
        _first = self.conditions[0]
        # print (self.workingDataset.__dict__)
        
        # by default use the last sheet, but allow the user to change it
        self.conditionForExtraction = self.conditions[-1]
        print ("scfe: {}".format(self.conditionForExtraction))
        
        self.workingDataset.ROI_list.extend(self.workingDataset.traces[_first].columns.tolist())
        self.updateROI_list_Box()
        
        #find out and store the size of the data
        self.setRanges()
        
        #split trace layout can be made now we know how many sets (conditions) we have
        self.createSplitTraceLayout()
        
        # populate the comboboxes for choosing the data shown in the zoom view,
        # and choosing the reference ROI for peak extraction
        self.p3Selection.clear()
        self.p3Selection.addItems(self.conditions)
        self.refSelection.clear()
        self.refSelection.addItems(self.conditions)
        
        i = self.refSelection.findText(self.conditionForExtraction)
        if i != -1:
            self.refSelection.setCurrentIndex(i)      # the default
            self.p3Selection.setCurrentIndex(i)     #set both for now
        
        #create a dataframe for peak measurements
        self.workingDataset.resultsDF = Results(self.workingDataset.ROI_list, self.conditions)
        print ("peakResults object created", self.workingDataset.resultsDF, self.workingDataset.ROI_list)
        
        self.plotNewData()
        
        #updates based on GUI can now happen painlessly
        self.dataLoaded = True
        self.ROI_Change()
        


if __name__ == "__main__":
    # Change menubar name from 'python' to 'Verify' on macOS
    # Doesn't appear to work
    # from https://stackoverflow.com/questions/5047734/
    if sys.platform.startswith('darwin'):
    # Python 3: pyobjc-framework-Cocoa is needed
        try:
            from Foundation import NSBundle
            bundle = NSBundle.mainBundle()
            if bundle:
                app_name = "Verify"
                app_info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
                
                if app_info is not None:
                    app_info['CFBundleName'] = app_name
                    app_info['CFBundleExecutable'] = app_name
                    
        except ImportError:
            print ("Failed to import NSBundle, couldn't change menubar name." )
            
    
    __version__ = "v. 0.5"
    #print (sys.version)
    app = QApplication([])
    vmw = VerifyMainWindow()
    vmw.show()
    sys.exit(app.exec_())

##### export QT_MAC_WANTS_LAYER=1 in the Terminal might be needed to see the app
