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
    def __init__(self, master):
        self.master = master
        frame = Frame(master)
        frame.config(background="#565656")
        #frame.pack()
        master.title('Verify v. 0.1')    #   Main frame title
        master.config(background="#dcdcdc")
        #master.geometry('450x480')
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
        lframe = LabelFrame(master, width = 450, text="Welcome to DC's statistics tools", background="#dcdcdc")
        
        Label(lframe, text="\nPlease select a test to run:", background="#dcdcdc").pack(anchor=W)
        b2 = Button(lframe, text="Randomisation test : Continuous data", width=30, pady=8, command=self.on_rantest_continuous, highlightbackground="#dcdcdc")
        b3 = Button(lframe, text="Randomisation test : Binomial data", width=30, pady=8, command=self.on_rantest_binomial, highlightbackground="#dcdcdc")
        b4 = Button(lframe, text="Fieller's theorem for SD of a ratio", width=30, pady=8, command=self.on_fieller, highlightbackground="#dcdcdc")
        b2.pack()
        b3.pack()
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
        
        b5 = Button(frame, text="Quit", command=master.quit, width=10, highlightbackground="#dcdcdc", pady=8)
        b5.pack(anchor=E)
        
        version = Message(frame, width=350, text="https://github.com/aplested/DC-Stats\n\nPython version: " + sys.version, background="#dcdcdc", font=("Helvetica", 10))
        version.pack(side=BOTTOM)
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
    







