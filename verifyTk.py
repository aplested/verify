#! /usr/bin/python
from os import system
import sys
import platform
import file_tools
from noise import *
from datetime import datetime

if sys.version_info[0] < 3:
    from Tkinter import *
    from ttk import Separator, Radiobutton, Style
    import tkFileDialog
    #print (str(sys.version_info) +" Tkinter")
else:
    from tkinter import *
    from tkinter.ttk import Separator, Radiobutton, Style
    from tkinter import filedialog as tkFileDialog

__author__="Andrew"
__date__ ="$07-Nov-2018$"


class verifyGUI:
    introduction = """
        Verify fluctuations from ion channel noise in difference records
        ----------------------------------------------------------------
        according to expectation of not exceeding 7 SD
        from Heinemann and Conti 'Methods in Enzymology' 207
        Takes input from tab-delimited Excel file 'file.txt' with columns being current traces
        Mean and variance are computed for the set to use in noise limit test
        Baseline noise is determined for each difference trace from the first hundred points (2 ms at 50 kHz)
        Traces with extremely noisy baselines are removed
        Traces that exceed the 7 SD limit are removed and the failing points are explicitly listed to the terminal
        Output is tab delimited text file with columns consisting of mean, variance and verified difference traces, default to 'verified.txt'
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
        master.geometry('960x480')
        menubar = Menu(master)
        
        
        
    
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
        b3 = Button(frame, text="Load traces", width=30, command=self.callback3, highlightbackground="#dcdcdc")
        b3.grid(row=5, column=0, columnspan=2, padx=10, pady=8, sticky=W)
        
        #need to remove Pack to use separator
        #w = Separator(orient=VERTICAL)
        #w.grid(column=2, rowspan=20, pady=5, sticky=NS)
        
        self.input_filename_label = StringVar()
        self.input_filename_label.set("No data loaded yet")
        self.l1 = Label(frame, textvariable=self.input_filename_label, bg="#dcdcdc")
        self.l1.grid(row=1, column=2, columnspan=4, pady=5, sticky=E)
        
        
        Label(frame, text="Baseline range (pts):", bg="#dcdcdc").grid(row=5, column=2, pady=5, sticky=E)
        self.br = Entry(frame, justify=CENTER, width=5, highlightbackground="#dcdcdc")
        self.br.grid(row=5, column=3, sticky=W, pady=5)
        self.br.insert(END, '0,50')
        
        Label(frame, text="Decimation:", bg="#dcdcdc").grid(row=6, column=2, pady=5, sticky=E)
        self.de = Entry(frame, justify=CENTER, width=5, highlightbackground="#dcdcdc")
        self.de.grid(row=6, column=3, sticky=W, pady=5)
        self.de.insert(END, '1')
        
        Label(frame, text="Unitary current amplitude (pA):", bg="#dcdcdc").grid(row=7, column=2, pady=5, sticky=E)
        self.e5 = Entry(frame, justify=CENTER, width=5, highlightbackground="#dcdcdc")
        self.e5.grid(row=7, column=3, sticky=W, pady=5)
        self.e5.insert(END, '1')
        
        Label(frame, text="Output filename:", bg="#dcdcdc").grid(row=21, column=2, columnspan=2, pady=5, sticky=W)
        
        style = Style()
        style.configure("TRadiobutton", padding=6, foreground="black", font=("Courier", 10), space=50)
        
        MODES = [
                 ("'verified.txt'", 3),
                 ("Save as...", 2),
                 ("'v_[input]'", 1),
                 ("'{date:time}_v_[input]'", 0)
                 ]

        self.v = IntVar()
        self.v.set(0) # initialize

        #note this is the ttk radiobutton, the tk one doesn't select at first
        for text, mode in MODES:
            b = Radiobutton(frame, text=text, command=self.callback_fname, variable=self.v, value=mode, state=NORMAL)
            b.grid(row=22, column=mode+2)
    
        
        #frame.update_idletasks()

        #default unitary current is 1 pA
        
        
        self.b4 = Button(frame, text="Verify traces variance", width=30, state=DISABLED, command=self.callback2, highlightbackground="#dcdcdc")
        self.b4.grid(row=6, padx=10, pady=8, column=0, columnspan=2)
        self.b5 = Button(frame, text="Plot Variance vs current", width=30, state=DISABLED, command=self.callback5, highlightbackground="#dcdcdc")
        self.b5.grid(row=7, padx=10, pady=8, column=0, columnspan=2)

        self.b6 = Button(frame, text="Quit", command=master.quit, width=10, highlightbackground="#dcdcdc")
        self.b6.grid(row=24, padx=10,  pady=8, column=0, sticky=W)

        version = Message(master, width=700, text="https://github.com/aplested/verify\tPython version: " + sys.version, background="#99eedc", font=("Helvetica", 10))
        version.pack(side=BOTTOM, fill=X)

        message = Message(master, text=self.introduction, justify=LEFT, width=700, font=("Helvetica", 12), bg="#dceedc", relief=RAISED)
        message.pack(side=BOTTOM, fill=X)
        

    
    

    def on_help():
        pass

    def callback_fname(self):
    ### there is no need to do anything until the analysis starts
        print self.v.get()
    
    def callback5(self):
        'Called by PLOT variance current button.'
        #make a new routine here to plot preliminary analysis
        pass
        #PlotRandomDist(self.output, self.paired,0,1, self.meanToPlot)

    def callback3(self):
        'Called by TAKE DATA FROM excel button'
        self.input_traces, self.dfile = self.read_Data('excel')
        #dfile contains source data path and filename
        if self.dfile != None:
            self.input_filename_label.set('Data loaded from ' + self.dfile)
            self.b4.config(state=NORMAL)    #turn on VERIFY button
        else:
            self.input_filename_label.set('No data loaded')

    
    def callback2(self):
        'Called by VERIFY button'
        #send traces to be checked
        print ("Verify")
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
        
        write_output (self.verified_output, self.output_header, out_filename)
    
    
    def getOutputFilename(self):
        try:
            userFilename = tkFileDialog.askopenfilename()
        except:
            userFilename = "verified.txt"

        return userFilename

    def read_Data(self, file_type):
        """"Asks for a excel tab-delim to use for verification test.
        file_type :string, can be txt or excel... no meaning here.
        """
            
        data_file_name = tkFileDialog.askopenfilename()
        
        if data_file_name == "":
            return None, None
        
        try:
            data_in_lines = file_tools.file_read(data_file_name)#, file_type)
        except:
            print ("Error opening file")
            return None, None

        try:
            input_traces = lines_into_traces (data_in_lines)
        except:
            print ("error converting loaded data, check the format")
            return None, None

        #input_traces = traces_scale(in_traces,5)            # optional scaling if gain wrong
        print ("Read {} traces from file".format(len(input_traces)))
    
        # Imagine taking a header here, with data titles?

        return input_traces, data_file_name

    def getResult(self):
        self.unitary = float(self.e5.get())
        self.input_traces, message = clean_bad_baselines(self.input_traces)
        print ("MESSAGE FROM CLEAN BAD: "+message)
        self.input_traces, self.difference_traces, messages, self.output_header = construct_diffs(self.input_traces)
        print ("MESSAGES FROM CONSTRUCT_DIFFS: "+messages)
        self.verified_output = final_prep(self.input_traces, self.difference_traces)


        





