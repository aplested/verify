#! /usr/bin/env python
"""
Launch verify GUI: Tk.
"""

import sys

if __name__ == "__main__":
    
    print (sys.version)
    if sys.version_info[0] < 3:
        from Tkinter import *
    else:
        from tkinter import *

    from verifyTk import *
    # initiate main frame
    master = Tk()
    app = verifyGUI(master)
    master.mainloop()



    
