#! /usr/bin/python
from os import system
import sys
import platform
import file_tools
from noise import *

if sys.version_info[0] < 3:
    from Tkinter import *
    from ttk import Separator
    import tkFileDialog
    #print (str(sys.version_info) +" Tkinter")
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
        Takes input from tab-delimited Excel file 'file.txt' with columns being current traces
        Mean and variance are computed for the set to use in noise limit test
        Baseline noise is determined for each difference trace from the first hundred points (2 ms at 50 kHz)
        Traces that exceed the limit are popped from the list and the failing points are explicitly listed to the terminal
        Output is tab delimited text file with columns consisting of verified traces 'verified.txt'
        """

    def __init__(self, master):
        
        p = platform.system()
        if p == 'Darwin':
            print ("Trying to force window to the front on Mac OSX")
            try:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            except:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python2.7" to true' ''')
        
        self.master = master
        frame = Frame(master)
        frame.config(background="#dcdcdc")
        frame.pack()
        master.title('Verify v. 0.1')    #   Main frame title
        master.config(background="#dcdcdc")
        master.geometry('640x480')
        menubar = Menu(master)
        
        self.input_filename_label = StringVar()
        self.input_filename_label.set("No data loaded yet")
        
        
        
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
      """
        b3 = Button(frame, text="Load traces from .txt file", command=self.callback3, highlightbackground="#99dcdc", pady=8)
        b3.grid(row=14, column=0, columnspan=2, sticky=W)
        
        self.l1 = Label(frame, textvariable=self.input_filename_label, bg="#dcdcdc")
        self.l1.grid(row=14, column=1, columnspan=3, pady=5, sticky=E)
        
        Label(frame, text="Unitary current amplitude (pA):", bg="#dcdcdc").grid(row=18, column=1, pady=5, sticky=E)
        
        #default unitary current is 1 pA
        self.e5 = Entry(frame, justify=CENTER, width=12, highlightbackground="#dcdcdc")
        self.e5.grid(row=18, column=2, sticky=W, pady=5)
        self.e5.insert(END, '1')
        
        self.b4 = Button(frame, text="Verify traces variance", state=DISABLED, command=self.callback2, highlightbackground="#dcdcdc")
        self.b4.grid(row=22, padx=10, pady=8, column=0, sticky=W)
        self.b5 = Button(frame, text="Plot Variance vs current", state=DISABLED, command=self.callback5, highlightbackground="#dcdcdc")
        self.b5.grid(row=22, padx=10, pady=8, column=1, sticky=W)

        self.b6 = Button(frame, text="Quit", command=master.quit, width=10, highlightbackground="#dcdcdc")
        self.b6.grid(row=22, padx=10,  pady=8, column=2, sticky=W)
        
        message = Message(master, text=self.introduction, justify=LEFT, padx=10, width=600, font=("Helvetica", 12), bg="#dceedc")
        message.pack(side=BOTTOM)
        
        version = Message(master, width=600, text="https://github.com/aplested/verify\tPython version: " + sys.version, background="#99dcee", font=("Helvetica", 10))
        version.pack(side=BOTTOM)
    
    

    def on_help():
        pass

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
        self.input_traces, self.difference_traces, messages, header = construct_diffs(self.input_traces)
        print ("MESSAGES FROM CONSTRUCT_DIFFS: "+messages)
        verified_output = final_prep(self.input_traces, self.difference_traces)
        write_output (verified_output, header, "verified.txt")

        





