import serial
import io


class Transmitter:
    """A class to ranmit the data to the dvd plotter"""
    streaming = 1
    gcode=[]
    i = 0
    port="COM3"
    board=57600
    ser=""

    #Setup the class
    def __init__(self, port="COM3",board=57600):
        self.board=board
        self.port=port
        self.filename=""
        self.gcode=[];
        self.streaming = 1
        self.i=0
 
    #Read the Hanshake
    def readHandShake(self):
        while True:
            line = self.ser.readline()
            if line!="":
                print(line)
                if line.startswith("Y range is from"):
                    return True
	
    def SendStartPos(self):
        print("start")
        self.ser.write('G90\nG20\nG00 X0.000 Y0.000 Z0.000\n')

	
	
    #Open the searial port
    def openSerial(self):
        self.ser = serial.Serial(self.port, self.board, timeout=1)  # open serial port
        print(self.ser.name)         # check which port was really used
        #self.SendStartPos
    
    #Read the file with the GCode data
    def readGcode(self,file):
        f = open(file, 'r')
        self.gcode = f.readlines()
        f.close()

    #Wait for the ok back from the arduno
    def readOK(self):
        while True:
            line = self.ser.readline()
            if "ok" in line:
                print(line.rstrip())
                return 1

    #send the next gcode
    def sendGCode(self):
        if self.i>=len(self.gcode):
            return 0
        else:
            print(self.gcode[self.i].rstrip())
            if len(self.gcode[self.i].strip())>0:
                self.ser.write(self.gcode[self.i])
                return 1
            else:
                return 2

    def Transmit(self,file):
        self.readGcode(file)
        self.openSerial()
        
        self.streaming=self.readHandShake()
        #self.SendStartPos()
        
        self.streaming=1
        while self.streaming==1:
            r=self.sendGCode()
            if r==1:
                self.readOK()
            if r==2:
                r=1
            self.streaming=r
            self.i=self.i+1
        print("trans")
        self.SendStartPos()
        self.readOK()
        
        self.ser.close() # close port
        
            



#d = GodeTransmitter()
#d.Transmit('photo.gcode')
#print("finished")


        
    

