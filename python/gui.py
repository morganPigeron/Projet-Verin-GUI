import time
from pySerialTransfer import pySerialTransfer as txfer
from tkinter import Tk

import functions
import classes 


app = classes.Application()
app.after(33,app.refresh)
app.mainloop()