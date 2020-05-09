import time
from pySerialTransfer import pySerialTransfer as txfer
import tkinter as tk

import functions

#Class to communicate with arduino __________________________________
class Link:
    def __init__(self, com):
        self.com = com

        self.link = txfer.SerialTransfer(com)

        self.list_size = 0

        self.list_ = []

        self.link.open()
        # allow some time for the Arduino to completely reset
        time.sleep(2) 

    def sendCom(self, buffer):
        
        self.list_ = buffer

        self.list_size = self.link.tx_obj(self.list_)
        
        self.link.send(self.list_size)

        print('SENT: {}'.format(self.list_))

        return 'SENT: {}'.format(self.list_)

    def readCom(self):

        # If something is available
        if self.link.available():
            
            # Error handling
            if self.link.status < 0:
                if self.link.status == -1:
                    print('ERROR: CRC_ERROR')
                elif self.link.status == -2:
                    print('ERROR: PAYLOAD_ERROR')
                elif self.link.status == -3:
                    print('ERROR: STOP_BYTE_ERROR')

            rec_list_  = self.link.rx_obj(
                                            obj_type=type(self.list_),
                                            obj_byte_size=self.list_size, 
                                            list_format='i'
                                        )
        
            print('RCVD: {}'.format(rec_list_))

            return ('RCVD: {}'.format(rec_list_))

    def closeCom(self):
        self.link.close()

    def getPort(self):
        return self.com


#GUI class __________________________________________________________
class Application(tk.Tk, Link):

    def __init__(self):

        #init parent class
        tk.Tk.__init__(self)
        try:
            Link.__init__(self, functions.findComPort())
        except:
            print("!!! ERR : AUCUN ARDUINO !!!")

        #change title
        self.title("Arduino sur : " + str(self.getPort()))

        #init statusVar
        self.inter1 = 0
        self.inter2 = 0

        self.nema1G = 0
        self.nema1D = 0
        self.nema1vit = tk.IntVar(0)

        self.nema2G = 0
        self.nema2D = 0
        self.nema2vit = tk.IntVar(0)

        self.nema3G = 0
        self.nema3D = 0
        self.nema3vit = tk.IntVar(0)

        self.servo = 0

        #create buffer
        self.refreshBuf()

        #init widget
        self.initWidget()
        
        #init text box with arduino communication
        self.initDebugLog()

        #init keyboard control
        self.initKeyboardControl()


    def refreshBuf(self):
        self.buffer = [
            self.nema1G,
            self.nema1D,
            self.nema1vit,
            self.nema2G,
            self.nema2D,
            self.nema2vit,
            self.nema3G,
            self.nema3D,
            self.nema3vit,
            self.servo,  
            self.inter1,
            self.inter2,      
        ]


    def refresh(self):
        
        self.nema1vit = self.sliderNema1D.get()

        self.nema2vit = self.sliderNema2D.get()

        self.nema3vit = self.sliderNema3D.get()

        self.refreshBuf()

        sending = self.sendCom(self.buffer)
        receiving = self.readCom()

        #log
        self.textLog.insert(tk.INSERT, str(sending) + "\n")
        self.textLog.insert(tk.INSERT, str(receiving) + "\n")
        self.textLog.yview(tk.END)

        self.after(33, self.refresh)


    def initWidget(self):

        self.bigFrameTop = tk.Frame(self)
        self.bigFrameTop.pack(side='top')

        self.bigFrameMiddle = tk.Frame(self)
        self.bigFrameMiddle.pack(side='top')

        self.bigFrameBottom = tk.Frame(self)
        self.bigFrameBottom.pack(side='top')

        self.frameCtrlL = tk.Frame(self.bigFrameTop)
        self.frameCtrlL.pack(side='left', padx=10, pady=10)

        self.frameCtrlM = tk.Frame(self.bigFrameTop)
        self.frameCtrlM.pack(side='left', padx=10, pady=10)

        self.frameCtrlR = tk.Frame(self.bigFrameTop)
        self.frameCtrlR.pack(side='left', padx=10, pady=10)

        self.frameSlider = tk.Frame(self.bigFrameBottom)
        self.frameSlider.pack(side='bottom')

        self.btnNema1G = tk.Button(self.frameCtrlL, text='<N1', height = 2, width = 5)
        self.btnNema1G.pack(side="top", pady=10)
        self.btnNema1G.bind("<ButtonPress>", self.nema1GPress)
        self.btnNema1G.bind("<ButtonRelease>", self.nema1GRelease)

        self.btnNema1D = tk.Button(self.frameCtrlR, text='N1>', height = 2, width = 5)
        self.btnNema1D.pack(side="top", pady=10)
        self.btnNema1D.bind("<ButtonPress>", self.nema1DPress)
        self.btnNema1D.bind("<ButtonRelease>", self.nema1DRelease)

        self.btnNema2G = tk.Button(self.frameCtrlL, text='<N2', height = 2, width = 5)
        self.btnNema2G.pack(side="top", pady=10)
        self.btnNema2G.bind("<ButtonPress>", self.nema2GPress)
        self.btnNema2G.bind("<ButtonRelease>", self.nema2GRelease)

        self.btnServo = tk.Button(self.frameCtrlM, text='Servo', height = 5, width = 5)
        self.btnServo.pack()
        self.btnServo.bind("<ButtonPress>", self.servoPress)
        self.btnServo.bind("<ButtonRelease>", self.servoRelease)

        self.btnNema2D = tk.Button(self.frameCtrlR, text='N2>', height = 2, width = 5)
        self.btnNema2D.pack(side="top", pady=10)
        self.btnNema2D.bind("<ButtonPress>", self.nema2DPress)
        self.btnNema2D.bind("<ButtonRelease>", self.nema2DRelease)

        self.btnNema3G = tk.Button(self.frameCtrlL, text='<N3', height = 2, width = 5)
        self.btnNema3G.pack(side="top", pady=10)
        self.btnNema3G.bind("<ButtonPress>", self.nema3GPress)
        self.btnNema3G.bind("<ButtonRelease>", self.nema3GRelease)

        self.btnNema3D = tk.Button(self.frameCtrlR, text='N3>', height = 2, width = 5)
        self.btnNema3D.pack(side="top", pady=10)
        self.btnNema3D.bind("<ButtonPress>", self.nema3DPress)
        self.btnNema3D.bind("<ButtonRelease>", self.nema3DRelease)
        
        self.btnInter1 = tk.Button(self.bigFrameMiddle, text='S1 OFF',relief="groove", height = 2, width = 5)
        self.btnInter1.pack(side="left", pady=10, padx=50)
        self.btnInter1.bind("<ButtonPress>", self.inter1Press)

        self.btnInter2 = tk.Button(self.bigFrameMiddle, text='S2 OFF',relief="groove", height = 2, width = 5)
        self.btnInter2.pack(side="left", pady=10, padx=50)
        self.btnInter2.bind("<ButtonPress>", self.inter2Press)

        self.sliderNema1D = tk.Scale(self.frameSlider, variable = self.nema1vit,orient=tk.HORIZONTAL,label='Nema 1',relief="ridge")
        self.sliderNema1D.pack(side="left")

        self.sliderNema2D = tk.Scale(self.frameSlider, variable = self.nema2vit,orient=tk.HORIZONTAL,label='Nema 2',relief="ridge")
        self.sliderNema2D.pack(side="left")

        self.sliderNema3D = tk.Scale(self.frameSlider, variable = self.nema3vit,orient=tk.HORIZONTAL,label='Nema 3',relief="ridge")
        self.sliderNema3D.pack(side="left")


    def initDebugLog(self):

        self.frameLog = tk.Frame(self)
        self.frameLog.pack(side='bottom')
        
        self.textLog = tk.Text(self.frameLog, height='3', width='50')
       
        self.scrollLog = tk.Scrollbar(self.frameLog, command=self.textLog.yview)

        self.textLog.configure(yscrollcommand=self.scrollLog.set)

        self.textLog.pack(side="bottom")
        #self.scrollLog.pack()

    def initKeyboardControl(self):
        #UP
        self.bind('<KeyPress-Up>', self.nema1GPress)
        self.bind('<KeyRelease-Up>', self.nema1GRelease)

        #DOWN
        self.bind('<KeyPress-Down>', self.nema1DPress)
        self.bind('<KeyRelease-Down>', self.nema1DRelease)

        #LEFT
        self.bind('<KeyPress-Left>', self.nema2GPress)
        self.bind('<KeyRelease-Left>', self.nema2GRelease)

        #RIGHT
        self.bind('<KeyPress-Right>', self.nema2DPress)
        self.bind('<KeyRelease-Right>', self.nema2DRelease)

        #ENTER
        self.bind('<KeyPress-Return>', self.servoPress)
        self.bind('<KeyRelease-Return>', self.servoRelease)

        #A
        self.bind('<KeyPress-a>', self.nema3GPress)
        self.bind('<KeyRelease-a>', self.nema3GRelease)

        #R
        self.bind('<KeyPress-r>', self.nema3DPress)
        self.bind('<KeyRelease-r>', self.nema3DRelease)

        #W
        self.bind('<KeyPress-w>', self.inter1Press)

        #C
        self.bind('<KeyPress-c>', self.inter2Press)

    #HANDLER 

    def nema1GPress(self, event):
        self.nema1G = 1

    def nema1GRelease(self, event):
        self.nema1G = 0

    def nema1DPress(self, event):
        self.nema1D = 1

    def nema1DRelease(self, event):
        self.nema1D = 0
        
    def servoPress(self, event):
        self.servo = 1

    def servoRelease(self, event):
        self.servo = 0  

    def nema2GPress(self, event):
        self.nema2G = 1

    def nema2GRelease(self, event):
        self.nema2G = 0

    def nema2DPress(self, event):
        self.nema2D = 1

    def nema2DRelease(self, event):
        self.nema2D = 0

    def nema3GPress(self, event):
        self.nema3G = 1

    def nema3GRelease(self, event):
        self.nema3G = 0

    def nema3DPress(self, event):
        self.nema3D = 1

    def nema3DRelease(self, event):
        self.nema3D = 0

    def inter1Press(self, event):
        
        if(self.inter1):
            self.btnInter1["text"] = "S1 OFF"
            self.inter1 = 0 
        else:
            self.btnInter1["text"] = "S1 ON"
            self.inter1 = 1
        
    def inter2Press(self, event):
        
        if(self.inter2):
            self.btnInter2["text"] = "S2 OFF"
            self.inter2 = 0 
        else:
            self.btnInter2["text"] = "S2 ON"
            self.inter2 = 1