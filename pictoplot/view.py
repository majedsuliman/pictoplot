from turtle import *
import io

'''Draw the gcode'''
class ViewGCode():
   i=0
   gcode=[]
   scale=5
   
   #Setup the class
   def __init__(self):
      i=0
      gcode=[]
      
   #Read the file with the GCode data
   def readGcode(self,file):
      f = open(file, 'r')
      self.gcode = f.readlines()
      f.close()

   def DrawBox(self):
      pencolor("red")
      penup()
      setpos(0,0)
      pendown()
      setpos(40*self.scale,0)
      setpos(40*self.scale,40*self.scale)
      setpos(0,40*self.scale)
      setpos(0,0)
      penup()
      

   def Render(self,file,scale=5,drawbox=True):
      tracer(8, 25)
      
      self.scale=scale
      title("Welcome to the PictoPlot")
      self.readGcode(file)
      if drawbox:
         self.DrawBox()
      speed("fastest")
      pencolor("black")
      penup()
      for line in self.gcode:
         e=line.split(" ")
         if e[0]=="G1":
            setpos(float(e[1].replace("X",""))*self.scale,float(e[2].replace("Y",""))*self.scale)
         elif e[0]=="M300":
            if e[1]=="S30.00":#pend down
               pendown()
            elif e[1]=="S50.00":#pen up
               penup()
      exitonclick()
      done()
      
