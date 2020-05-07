import time
from pySerialTransfer import pySerialTransfer as txfer
import tkinter as tk
import tkinter.ttk as ttk

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
        self.verinH = 0
        self.verinB = 0

        self.nema1G = 0
        self.nema1D = 0
        self.nema1vit = tk.IntVar(0)

        self.nema2G = 0
        self.nema2D = 0
        self.nema2vit = tk.IntVar(0)

        self.servo = 0

        #create buffer
        self.refreshBuf()

        #init widget
        self.initWidget()

        self.initDebugLog()


    def refreshBuf(self):
        self.buffer = [
            self.verinH,
            self.verinB,
            self.nema1G,
            self.nema1D,
            self.nema1vit,
            self.nema2G,
            self.nema2D,
            self.nema2vit,
            self.servo,        
        ]


    def refresh(self):
        
        self.nema1vit = self.sliderNema1D.get()

        self.nema2vit = self.sliderNema2D.get()

        self.refreshBuf()

        sending = self.sendCom(self.buffer)
        receiving = self.readCom()

        #log
        self.textLog.insert(tk.INSERT, str(sending) + "\n")
        self.textLog.insert(tk.INSERT, str(receiving) + "\n")
        self.textLog.yview(tk.END)

        self.after(33, self.refresh)


    def initWidget(self):

        self.frameCtrl = tk.Frame(self)
        self.frameCtrl.pack(side='top')

        self.frameCtrl2 = tk.Frame(self)
        self.frameCtrl2.pack(side='top')

        self.frameSlider = tk.Frame(self)
        self.frameSlider.pack(side='top')

        self.btnVerinHaut = ttk.Button(self.frameCtrl, text='V+')
        self.btnVerinHaut.pack(side="top")
        self.btnVerinHaut.bind("<ButtonPress>", self.vUonPress)
        self.btnVerinHaut.bind("<ButtonRelease>", self.vUonRelease)

        self.btnVerinBas = ttk.Button(self.frameCtrl, text='V-')
        self.btnVerinBas.pack(side="bottom")
        self.btnVerinBas.bind("<ButtonPress>", self.vDonPress)
        self.btnVerinBas.bind("<ButtonRelease>", self.vDonRelease)

        self.btnNema1G = ttk.Button(self.frameCtrl, text='<N1')
        self.btnNema1G.pack(side="left")
        self.btnNema1G.bind("<ButtonPress>", self.nema1GPress)
        self.btnNema1G.bind("<ButtonRelease>", self.nema1GRelease)

        self.btnServo = ttk.Button(self.frameCtrl, text='Servo')
        self.btnServo.pack(side="left")
        self.btnServo.bind("<ButtonPress>", self.servoPress)
        self.btnServo.bind("<ButtonRelease>", self.servoRelease)

        self.btnNema1D = ttk.Button(self.frameCtrl, text='N1>')
        self.btnNema1D.pack(side="right")
        self.btnNema1D.bind("<ButtonPress>", self.nema1DPress)
        self.btnNema1D.bind("<ButtonRelease>", self.nema1DRelease)

        self.btnNema2G = ttk.Button(self.frameCtrl2, text='<N2')
        self.btnNema2G.pack(side="left")
        self.btnNema2G.bind("<ButtonPress>", self.nema2GPress)
        self.btnNema2G.bind("<ButtonRelease>", self.nema2GRelease)

        self.btnNema2D = ttk.Button(self.frameCtrl2, text='N2>')
        self.btnNema2D.pack(side="right")
        self.btnNema2D.bind("<ButtonPress>", self.nema2DPress)
        self.btnNema2D.bind("<ButtonRelease>", self.nema2DRelease)

        self.sliderNema1D = tk.Scale(self.frameSlider, variable = self.nema1vit,orient=tk.HORIZONTAL,label='Nema 1',relief="ridge")
        self.sliderNema1D.pack(side="left")

        self.sliderNema2D = tk.Scale(self.frameSlider, variable = self.nema2vit,orient=tk.HORIZONTAL,label='Nema 2',relief="ridge")
        self.sliderNema2D.pack(side="right")


    def initDebugLog(self):

        self.frameLog = tk.Frame(self)
        self.frameLog.pack(side='bottom')
        
        self.textLog = tk.Text(self.frameLog, height='3', width='50')
       
        self.scrollLog = tk.Scrollbar(self.frameLog, command=self.textLog.yview)

        self.textLog.configure(yscrollcommand=self.scrollLog.set)

        self.textLog.pack(side="bottom")
        #self.scrollLog.pack()

    #HANDLER 

    def vUonPress(self, event):
        self.verinH = 1

    def vUonRelease(self, event):
        self.verinH = 0        

    def vDonPress(self, event):
        self.verinB = 1

    def vDonRelease(self, event):
        self.verinB = 0    

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
        