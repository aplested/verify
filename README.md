# verify

Version 0.5
Check the variance of electrophysiological recordings for noise analysis

branch python3 is updated for Python3 and MacOS Sequoia but still Tkinter
branch vqt is updated for Python3, PySide6 and Qt (because Tkinter is limiting and no longer distributed with macOS)

To run Verify on modern hardware, you need versions of packages that are not bleeding edge (for whatever reason). See requirements.txt

The following set of packages was tested and working on M1 Macbook Pro with Sequoia 15.3.2  (May 2025)

`PySide6==6.6.*`
`numpy>=1.20`
`scipy==1.6.3`
`pyobjc==7.2`
`pyqtgraph>=0.13.3`

Clone from here, move to directory and issue (with up-to-date pip):

`conda create --name veriqt Python=3.8 && conda activate veriqt`

`pip install -r requirements.txt`

then

`python veriQT.py` 
to launch



old version (branch main with Tkinter) was tested and running under:

  MacOS 10.13, Python 2.7.15. In terminal, navigate to directory and type python verify.py
  Windows 10 Pro, Python 2.7.15 (64-bit .msi). Double-click verify.py to launch
  
![ScreenShot](/screenshots/veriQt.png) 
Notes: 

*if you have Python 3.x, you need to use an alias to launch Python 2.7
*Interface is not fully connected up. 
