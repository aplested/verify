#! /usr/bin/python
from os import system
import sys
from platform import system as platform
import file_tools
from noise import *

if sys.version_info[0] < 3:
    from Tkinter import *
    from ttk import Separator
    import tkFileDialog
    print (str(sys.version_info) +" Tkinter")
else:
    from tkinter import *
    from tkinter.ttk import Separator
    from tkinter import filedialog as tkFileDialog

__author__="Andrew"
__date__ ="$07-Nov-2018$"


class verifyGUI:
    introduction = """
        Verify fluctuations from ion channel noise in difference records according to expectation of not exceeding 7 S.D.
        from Heinemann and Conti Methods in Enzymology 207
        Andrew Plested 2006
        Takes input from tab-delimited Excel file 'file.txt'.
        Columns are current traces
        Mean and variance are computed for the set to use in limit calculation
        Baseline noise is determined for each difference trace from the first hundred points (2 ms at 50 kHz)
        Traces that exceed the limit are popped from the list and the failing points are explicitly listed to the terminal
        Output is tab delimited columns of verified traces 'verified.txt'
        """

    def __init__(self, master):
        self.master = master
        frame = Frame(master)
        frame.config(background="#565656")
        frame.pack()
        master.title('Verify v. 0.1')    #   Main frame title
        master.config(background="#dcdcdc")
        master.geometry('640x480')
        menubar = Menu(master)
        
        self.input_filename_label = StringVar()
        self.input_filename_label.set("No data loaded yet")
        
        message = Message(frame, text="Noise analysis\n"+self.introduction, justify=LEFT, padx=10, width=500, font=("Helvetica", 12), bg="#dcdcdc")
        message.grid(row=0, column=0, rowspan=12, columnspan=4)
        
        """statmenu = Menu(menubar,tearoff=0)
        statmenu.add_command(label="Fieller", command=self.on_fieller)
        
        statmenu.rantest = Menu(statmenu)
        statmenu.rantest.add_command(label="Continuously variable data", command=self.on_rantest_continuous)
        statmenu.rantest.add_command(label="Binomial data (each result= yes or no)", command=self.on_rantest_binomial)
        statmenu.add_cascade(label="Randomisation test", menu=statmenu.rantest)
        
        statmenu.add_command(label="Help", command=self.on_help, state=DISABLED)
        statmenu.add_command(label="Quit", command=master.quit)
        
        menubar.add_cascade(label="Statistical Tests", menu=statmenu)
        master.config(menu=menubar)
        lframe = LabelFrame(master, width = 450, text="Welcome to DC's statistics tools", background="#dcdcdc")
        """
        b3 = Button(frame, text="Load traces from Excel Tab-delimited.txt file", command=self.callback3, highlightbackground="#00dcdc")
        b3.grid(row=14, column=0, columnspan=2, sticky=W)
        
        self.l1 = Label(frame, textvariable=self.input_filename_label, bg="#dcdcdc")
        self.l1.grid(row=14, column=2, columnspan=2, pady=5, sticky=E)
        
        Label(frame, text="Unitary current amplitude (pA):", bg="#dcdcdc").grid(row=18, column=1, pady=5, sticky=E)
        
        #default unitary current is 1 pA
        self.e5 = Entry(frame, justify=CENTER, width=12, highlightbackground="#dcdcdc")
        self.e5.grid(row=18, column=2, sticky=E, pady=5)
        self.e5.insert(END, '1')
        
        self.b4 = Button(frame, text="Verify trace variance", state=DISABLED, command=self.callback2,highlightbackground="#dcdcdc", pady=8)
        self.b4.grid(row=22, padx=40, column=0, sticky=W)
        self.b5 = Button(frame, text="Plot Variance vs current", state=DISABLED, command=self.callback5,highlightbackground="#dcdcdc", pady=8)
        self.b5.grid(row=22, padx=40, column=1, sticky=W)
        """
        
        
        lframe.pack()
        frame.pack()
        
        """
        

        self.b6 = Button(frame, text="Quit", command=master.quit, width=10, highlightbackground="#dcdcdc", pady=8)
        self.b6.grid(row=22, column=2, sticky=W)
        
        version = Message(frame, width=350, text="https://github.com/agplested/verify\n\nPython version: " + sys.version, background="#dcdcdc", font=("Helvetica", 10))
        version.grid(row=26, column=0, rowspan=2, columnspan=4)
        """
        
        if platform() == 'Darwin':
            print ("Trying to force window to the front on Mac OSX")
            try:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            except:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python2.7" to true' ''')


    
    def on_fieller(self):
        f = Toplevel(self.master)
        FrameFieller(f)

    def on_help():
        pass

"""
    def callback5(self):
        'Called by PLOT variance current button.'
        #make a new routine here to plot preliminary analysis
        pass
        #PlotRandomDist(self.output, self.paired,0,1, self.meanToPlot)

    def callback3(self):
        'Called by TAKE DATA FROM excel button'
        self.input_traces, self.dfile = self.read_Data('excel')
        #dfile contains source data path and filename
        self.input_filename_label.set('Data loaded from ' + self.dfile)
        #turn on VERIFY button
        self.b4.config(state=NORMAL)
        #self.update_idletasks()
    
        #self.e5.insert(END, '5000')     #reset to low value
        #self.getResult()
        
    def callback2(self):
        'Called by VERIFY button'
        #send traces to be checked
        #self.update_idletasks()
        print ("Verify")
        pass
        #self.e5.insert(END, '5000')     #reset to low value
        self.getResult()
    
    def read_Data(self, file_type):
        """"Asks for a excel tab-delim to use for verification test.
        file_type :string, can be txt or excel... no meaning here.
        """
            
        data_file_name = tkFileDialog.askopenfilename()
        #Convert file into lines of tab delimited text
        data_in_lines = file_tools.file_read(data_file_name)#, file_type)
    
        input_traces = lines_into_traces (data_in_lines)
        #input_traces = traces_scale(in_traces,5)            # optional scaling if gain wrong
        print ("Read {} traces from file".format(len(input_traces)))
    
        # Imagine taking a header here, with data titles?

        return input_traces, data_file_name

    def getResult(self):
        self.unitary = float(self.e5.get())
        self.input_traces, message = clean_bad_baselines(self.input_traces)
        print ("MESSAGE FROM CLEAN BAD: "+message)
        self.input_traces, self.difference_traces, messages = construct_diffs(self.input_traces)
        print ("MESSAGES FROM CONSTRUCT_DIFFS: "+messages)
        verified_output = final_prep(self.input_traces, self.difference_traces)
        write_output (verified_output, "verified.txt")

        





