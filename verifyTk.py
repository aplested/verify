#! /usr/bin/python
from os import system
import sys
from platform import system as platform
if sys.version_info[0] < 3:
    from Tkinter import *
else:
    from tkinter import *


__author__="Andrew"
__date__ ="$07-Nov-2018$"


class verifyGUI:
    introduction = """
        Verify fluctuations from ion channel noise in difference records
        according to expectation of not exceeding 7 S.D.
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
        #master.geometry('450x480')
        menubar = Menu(master)
        
        message = Message(frame, text="Noise analysis\n"+self.introduction, justify=LEFT, padx=10, width=500, font=("Helvetica", 12), bg="#dcdcdc")
        message.grid(row=0, column=0, rowspan=12, columnspan=2, sticky=W)
        
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
        
        Label(lframe, text="\nPlease select a test to run:", background="#dcdcdc").pack(anchor=W)
        b2 = Button(lframe, text="Randomisation test : Continuous data", width=30, pady=8, command=self.on_rantest_continuous, highlightbackground="#dcdcdc")
        
        b4 = Button(lframe, text="Fieller's theorem for SD of a ratio", width=30, pady=8, command=self.on_fieller, highlightbackground="#dcdcdc")
        b2.pack()
        
        b4.pack()
        
        Label(lframe, text="", background="#dcdcdc").pack()
        picture = PhotoImage(file="GUI/dca2.gif")
        dcpic = Label(lframe, image=picture, pady=8)
        dcpic.image = picture
        dcpic.pack(fill=X)
        dcpic.frame = 0
        frame.after(500, self._play_gif, frame, dcpic, 500)
        
        Label(lframe, text="David Colquhoun", background="#dcdcdc", pady=5, font=("Helvetica", 12)).pack()
        lframe.pack()
        frame.pack()
        
        """
        b3 = Button(frame, text="Load traces from Excel Tab-delimited.txt file", command=self.callback3, highlightbackground="#dcdcdc")
        b3.grid(row=16, column=0,  sticky=W, padx=30)
        b5 = Button(frame, text="Quit", command=master.quit, width=10, highlightbackground="#dcdcdc", pady=8)
        b5.grid(row=20, column=0, rowspan=1, columnspan=2, sticky=W)
        
        version = Message(frame, width=350, text="https://github.com/aplested/DC-Stats\n\nPython version: " + sys.version, background="#dcdcdc", font=("Helvetica", 10))
        version.grid(row=22, column=0, rowspan=3, columnspan=2, sticky=W)
        """
        
        if platform() == 'Darwin':
            print ("Trying to force window to the front on Mac OSX")
            try:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
            except:
                system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python2.7" to true' ''')

    def _play_gif(self, frame, w, interval):
        # animates the GIF by rotating through
        # the GIF animation frames
        # modified from http://pyinmyeye.blogspot.de/2012/08/tkinter-animated-labels-demo.html
        try:
            opt = "GIF -index {}".format(w.frame)
            w.image.configure(format=opt)
        except TclError:
            w.frame = 0
            self._play_gif(frame, w, interval)
            return
        
        w.frame += 1
        frame.after(interval, self._play_gif, frame, w, interval)
    
    def on_fieller(self):
        f = Toplevel(self.master)
        FrameFieller(f)

    def on_help():
        pass

if __name__ == "__main__":

    print (sys.version) #parentheses necessary in python 3  
    
    #
    """
    
    def callback3(self):
        'Called by TAKE DATA FROM excel button'
        self.traces, self.dfile = self.read_Data('excel')
        #dfile contains source data path and filename
        self.data_source = 'Data from ' + self.dfile
        #self.e5.delete(0, END)
        #self.e5.insert(END, '5000')     #reset to low value
        #self.getResult()
    
    def read_Data(self, file_type):
        """"Asks for a tab delimited text file or excel tab-delim to use in randomization test.
        file_type :string, can be txt or excel
        """
            
        data_file_name = tkFileDialog.askopenfilename()
        #Convert file into lines of tab delimited text
        traces = file_tools.file_read(data_file_name, file_type)
        
        # Imagine taking a header here, with data titles?

        return traces, data_file_name






