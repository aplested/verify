#! /usr/bin/python
from os import system
import sys
import platform
import file_tools
from trace_tools import decimate_traces
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

    def __init__(self, master):
        
        p = platform.system()
        if p == 'Darwin':
            
            try:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
                print ("Trying to force Python window to the front on macOS")
            except:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python2.7" to true' ''')
                print ("Trying to force Python 2.7 window to the front on macOS")
        
        self.master = master
        frame = Frame(master)
        frame.config(background="#dcdcdc")
        frame.config(borderwidth=5, relief=GROOVE)
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        master.title('Verify v. 0.2')    #   Main frame title
        master.config(background="#dcdcdc")
        master.geometry('850x480')
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
        b3 = Button(frame, text="Load traces", width=20, command=self.callback3, highlightbackground="#dcdcdc")
        b3.grid(row=0, column=0, columnspan=2, padx=10, pady=8, sticky=W)
        
        self.b4 = Button(frame, text="Verify traces variance", width=20, state=DISABLED, command=self.callback2, highlightbackground="#dcdcdc")
        self.b4.grid(row=1, padx=10, pady=8, column=0, columnspan=2)

        self.b5 = Button(frame, text="Plot Variance vs. current", width=20, state=DISABLED, command=self.callback5, highlightbackground="#dcdcdc")
        self.b5.grid(row=2, padx=10, pady=8, column=0, columnspan=2)
        
        #need to remove Pack to use separator
        s1 = Separator(frame, orient=VERTICAL)
        s1.grid(column=2, row=0, rowspan=40, pady=10, sticky=N+W+S)
        
        self.input_filename_label = StringVar()
        self.input_filename_label.set("No data loaded yet")
        self.l1 = Label(frame, textvariable=self.input_filename_label, width=40, bg="#dcdcdc")
        self.l1.grid(row=0, column=2, columnspan=4, pady=5)
        
        
        Label(frame, text="Baseline range (pts)", bg="#dcdcdc").grid(row=1, column=2, columnspan=2, pady=5, sticky=E)
        self.br = Entry(frame, justify=CENTER, width=5, highlightbackground="#dcdcdc")
        self.br.grid(row=1, column=4, sticky=W, pady=5)
        self.br.insert(END, '0, 50')
        
        Label(frame, text="Decimation", bg="#dcdcdc").grid(row=2, column=2, columnspan=2, pady=5, sticky=E)
        self.de = Entry(frame, justify=CENTER, width=5, highlightbackground="#dcdcdc")
        self.de.grid(row=2, column=4, sticky=W, pady=5)
        self.de.insert(END, '1')
        
        Label(frame, text="Unitary current amplitude (pA)", bg="#dcdcdc").grid(row=3, column=2, columnspan=2, pady=5, sticky=E)
        self.ua = Entry(frame, justify=CENTER, width=5, highlightbackground="#dcdcdc")
        self.ua.grid(row=3, column=4, sticky=W, pady=5)
        self.ua.insert(END, '1')
        
        Label(frame, text="Output filename", bg="#dcdcdc").grid(row=4, column=2, columnspan=2, pady=5)
        
        style = Style()
        style.theme_use('clam')
        style.configure("w.TRadiobutton", padding=2, background="#dcdcdc", foreground="black", width=15)
        style.configure("TRadiobutton", padding=2, background="#dcdcdc", foreground="black", width=8)
        
        MODES = [
                 ("verified.txt", 3),
                 ("Save as...", 2),
                 ("v_[infile]", 1),
                 ("[date:time]_v_[infile]", 0)
                 ]

        self.v = IntVar()
        self.v.set(0) # initialize

        #note this is the ttk radiobutton, the tk one doesn't select at first
        for text, mode in MODES:
            b = Radiobutton(frame, text=text, command=self.callback_fname, variable=self.v, value=mode, state=NORMAL)
            b.grid(row=5, padx=10, column=mode+2, sticky=E)
    
        #the last button in the loop (0) is the wide one, so gets the wide style.
        b.configure(style='w.TRadiobutton')
        #default unitary current is 1 pA
        
        

        s2 = Separator(frame)
        s2.grid(row=25, columnspan=6, sticky=S+E+W)
        
        message = Message(frame, text=self.introduction, width=800, font=("Courier", 12), bg="#dcdcdc")
        message.grid(row=26, rowspan=8, columnspan=6, sticky=EW)
        
        s3 = Separator(frame)
        s3.grid(row=35, columnspan=6, sticky=E+W)
        
        version_text = "\nhttps://github.com/aplested/verify\nPython version:\t" + sys.version.replace("\n", "\t")
        version = Message(frame, width=800, text=version_text, justify=LEFT, background="#dcdcdc", font=("Courier", 12))
        version.grid(row=36, columnspan=5, sticky=EW)

        self.b6 = Button(frame, text="Quit", command=master.quit, width=10, highlightbackground="#dcdcdc")
        self.b6.grid(row=36, padx=10,  pady=8, column=5, sticky=W)
    

    def on_help():
        pass

    def callback_fname(self):
    ### there is no need to do anything until the analysis starts
    #this is just for debugging
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
        self.unitary = float(self.ua.get())
        print ("Taking unitary current from GUI:  {} pA".format(self.unitary))

        self.decimation = int(self.de.get())
        print ("Decimating by {} according to GUI".format(self.decimation))

        #decimate but preserve the original files in case user wants to run again with different decimation etc
        if self.decimation > 1:
            self.dec_traces = decimate_traces(self.input_traces, self.decimation)
        else:
            self.dec_traces = self.input_traces
        
        self.baseline_range = [int(x) for x in self.br.get().split(",")]
        print ("Taking baseline range from GUI. Points from {} to {}".format(self.baseline_range[0], self.baseline_range[1]))
        
        self.input_traces, message = clean_bad_baselines(self.dec_traces, self.baseline_range)
        print ("MESSAGE FROM CLEAN BAD: "+message)
        self.input_traces, self.difference_traces, messages, self.output_header = construct_diffs(self.dec_traces, self.unitary, self.baseline_range)
        print ("MESSAGES FROM CONSTRUCT_DIFFS: "+messages)
        self.verified_output = final_prep(self.dec_traces, self.difference_traces, self.baseline_range)


        





