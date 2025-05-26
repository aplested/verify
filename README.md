# verify

Version 0.5
Check the variance of electrophysiological recordings for noise analysis
![ScreenShot](/screenshots/veriQt.png) 
branch python3 is updated for Python3 and MacOS Sequoia but still uses Tkinter

(May 2025) branch vqt is now the main development branch and is updated for Python3, PySide6 and Qt (because Tkinter is limiting and no longer distributed with macOS)

To run Verify on modern hardware, you need versions of packages that are not bleeding edge (for whatever reason). See requirements.txt

Clone from here, download and install miniconda (https://www.anaconda.com/download/ don't forget to restart your Terminal), move to the verify directory and issue (with up-to-date pip):

`conda create --name veriqt Python=3.9 && conda activate veriqt`

The following set of packages was tested and working on MacMini M2 Pro (Ventura 13.2.1) M1 Macbook Pro (Sequoia 15.3.2) or M1 Macbook Max (Monterey 12.2.1).

`PySide6==6.6.*`

`numpy>=1.22`

`scipy==1.7.3`

`pyobjc==7.2`

`pyqtgraph>=0.13.7`

You can do this automatically with the command:
`pip install -r requirements.txt`

then

`python veriQT.py` 
to launch

When you restart the terminal, enter:
'conda activate veriQt'

then launch with:
`python veriQT.py` 

old version (branch main with Tkinter) was tested and running under:

  MacOS 10.13, Python 2.7.15. In terminal, navigate to directory and type python verify.py
  Windows 10 Pro, Python 2.7.15 (64-bit .msi). Double-click verify.py to launch
  

Notes: 

*if you have Python 3.x, you need to use an alias to launch Python 2.7
*Interface is not fully connected up. 
