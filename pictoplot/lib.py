#!/usr/bin/env python
'''
Copyright (c) 2017 Andrew Pye

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
import pygame.camera
import pygame.image
from subprocess import call
from inkscape import unicornlib
import fileinput
import platform
import os
import time
from transmit import Transmitter
if platform.system()=="Windows":
        from cv2 import *
      

'''
class PicToPlot()
This class wraps the function to take picture and convert to Gcode
Dependancys:
   http://potrace.sourceforge.net/
   potrace
   mkbitmap

'''
class PicToPlot(): 
   '''
   Fields declaration
   '''
   port="COM3"
   board=57600
   threshold=0.5
   
   '''
   This is the construcot for our class
   Parameters:
      port="COM3" this is the serail port used
      board=57600 this is the board rate for the serial normally 9600 but this is slow
      threshold=0.5 this handles the Threshold for the pbm image
   '''
   def __init__(self, port="COM3",board=57600,threshold=0.5):
      self.board=board
      self.port=port
      self.threshold=threshold
         
   
   '''
   Method Process
   This just runs each of the steps one after another
   '''
   def Process(self,runitems=['takepic','convtobmp','convtosvg','fixsvg','convtog','trans']):
        if 'takepic' in runitems: self.TakePicture()
        if 'convtobmp' in runitems: self.CovertToPBM()
        if 'convtosvg' in runitems:self.ConvertToSVG()
        if 'fixsvg' in runitems: self.FixSvgHeader()
        if 'convtog' in runitems: self.ConvertToGCode()
        if 'trans' in runitems: self.Transmit()

   '''
   Method takePicture(())
   Takes a picture detect if windows or linux
   Because the camera function is turned off in Pygame i have to use cv2 libary
   but for linux pygame is used
   '''
   def TakePicture(self):
      #Code to detect the os and take a picture and store in tmp
      #First we detect what os
      if platform.system()=="Windows":
         cam = VideoCapture(0)   # 0 -> index of camera
         s, img = cam.read()
         if s:    # frame captured without any errors
            imwrite("tmp/photo.bmp",img) #save image
      else:
         #pygame.camera.init()#Init pygame
         #cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])#Select the camera
         #cam.start()#start the camera
         #print("Linux")
         #img = cam.get_image()#Geat our image
         #pygame.image.save(img, "tmp/photo.bmp")#same to the tmp folder
         #pygame.camera.quit()#tidy up


         #try:
         #   os.remove('tmp/photo.bmp')
         #except OSError:
        #    pass
         call(['streamer','-c','/dev/video0','-b','16','-s 800x600','-o','tmp/photo.jpeg'])
         call(['mogrify','-format','bmp','tmp/photo.jpeg'])



      
   
   '''
   Method CovertToPBM()
   We need to convert our Bmp into pbm this is just a black and white image
   we use mkbitmap to achive this this can be down loaded from http://potrace.sourceforge.net/
   '''
   def CovertToPBM(self):
        #Code to convert the bmp to a pbm
        print "Converting tmp/photo.bmp to tmp/photo.pbm"
        call(["mkbitmap", "-t"+str(self.threshold),"tmp/photo.bmp"])  
   
   '''
   Method convertToSVG()
   We need to convert our black and white image to SVG
   we use plotrace to achive this this can be dowloaded from
   http://potrace.sourceforge.net/
   '''
   def ConvertToSVG(self):
      #Converting tmp/photo.pbm to tmp/photo.svg
      print "Converting tmp/photo.pbm to tmp/photo.svg"
      #We -t200 handles the size of blobs we want to discard and it will convert to 40mmx40mm size
      #call(["potrace","--svg","-t200","-P 40mmx40mm","-W 40mm","-H40mm","--tight","tmp/photo.pbm"])
      call(["potrace","--svg","-t200","-P 40mmx40mm","-W 40mm","--tight","tmp/photo.pbm"]) 

   
   '''
   Method fixSvgHeader()
   The GCODe generator throws and error because there is the unit pt in the header so we have to 
   remove this also a quirk of the sofware means we have to offset the image so it all gets plotted
   dirty fix just rewrite the header
   '''
   def FixSvgHeader(self):
      #code to remove the pt
      print "Removing pt and offsetting the svg ready for plotting"
      f =fileinput.FileInput("tmp/photo.svg", inplace=True)
      for line in f:#loop through the lines
         if line.startswith("<g transform="):#find the transform line
            scale=0.0105000
            print('<g transform="translate(60.082978,20.809088) scale('+str(scale)+',-'+str(scale)+')"')#write the off set
         else:    
            print(line.replace('pt"', '"'))#remove the pt
      f.close()#Tidy up
      
   '''
   Method convertToGCode()
   This converts our svg to gcode file.
   This uses libary from inkscape 0.48 and plugin called unicorn written by Marty Mcguire
   https://github.com/martymcguire/inkscape-unicorn
   https://inkscape.org/sk/release/0.48/?latest=1
   Originally this was a manual process and on linux ubuntu i could not install 0.48 so got the elements i neeeded and 
   addded.
   https://inkscape.org/sk/about/license/
   '''
   def ConvertToGCode(self):
      #Convert svg to gcode data
      print "Convert svg to gcode data"
      e = unicornlib.MyEffect()
      e.affect(['--tab="plotter_setup"', '--pen-up-angle=50', '--pen-down-angle=30', '--start-delay=150', '--stop-delay=150', '--xy-feedrate=3500', '--z-feedrate=150', '--z-height=0', '--finished-height=0', '--register-pen=true', '--x-home=0', '--y-home=0', '--num-copies=1', '--continuous=false', '--pause-on-layer-change=false', 'tmp/photo.svg'])
      
      #Writing the gcode file
      print "Writing the gcode file"
      file = open("tmp/photo.gcode","w") 
      for c in e.context.codes:
         file.write(c + '\n') 
      file.close()
      
   def Home(self):
      #Transmit the file to the plotter
      print "Transmit the file to the plotter"
      d = Transmitter(self.port,self.board)
      d.openSerial()
      d.SendStartPos()
   
   '''
   This will transmit the gcode to the DVD plotter
   This part was originally handled by gctrl
   https://github.com/damellis/gctrl   
   but i felt i needed to rewite as a python libary
   all tis does is read the gcode file and send over seraal and wait for a reply
   before sending the the next line
   '''
   def Transmit(self):
      #Transmit the file to the plotter
      print "Transmit the file to the plotter"
      d = Transmitter(self.port,self.board)
      d.Transmit('tmp/photo.gcode')
