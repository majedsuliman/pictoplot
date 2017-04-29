import serial
import io

"""A class to ranmit the data to the dvd plotter"""
class GCodeTransmitter:
    #Class Fields
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
    def readHandShake(self,ser):
        while True:
            line = self.ser.readline()
            if line!="":
                print(line)
                if line.startswith("Y range is from"):
                    return True

    #Open the searial port
    def openSerial(self):
        self.ser = serial.Serial(self.port, self.board, timeout=1)  # open serial port
        print(self.ser.name)         # check which port was really used
     
    
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
        if i>len(self.gcode):
            return 0
        else:
            print(self.gcode[self.i].rstrip())
            if len(self.strip())>0:
                self.ser.write(self.gcode[self.i])
                return 1
            else:
                return 2

    #Main Method 
    def Transmit(self,file):
        self.readGcode(file)#Read the file
        self.openSerial()#Open the serial port
        self.streaming=self.readHandShake(ser)#get the handshake
        
        #Start streaming the data
        while self.streaming==1:
            r=self.sendGCode()#Send the code
            if r==1:
                self.readOK()#Wait for ok
            if r==2:r=1
            self.streaming=r#Store the streaming bool
            self.i=self.i+1#Inc the line pointer

        ser.close() # close port
        
            

if __name__ == "__main__":
    #Create the clas
    d = GodeTransmitter()
    #Send the file
    d.Transmit('photo.gcode')
    print("finished")


        
    

