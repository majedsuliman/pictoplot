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
import pictoplot.lib
import pictoplot.interface
import pictoplot.view
import sys
from shutil import copyfile

'''
This is the main interface to eather run as headless or with an interface
by default we will run it headless
'''


import sys, getopt

def main(argv):
    i = 0
    try:
        opts, args = getopt.getopt(argv,"hi:",["interactive="])
    except getopt.GetoptError:
        print 'pictoplot.py -i <interactive>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'pictoplot.py -i <interactive [1,0]>'
            sys.exit()
        elif opt in ("-i"):
            i = int(arg)
           
    #Our main code to run the program        
    p=pictoplot.lib.PicToPlot(port="COM3",board=57600,threshold=0.5)
    
    if i==1:
        i=pictoplot.interface.Interface(p)
        i.Process()
    elif i==2:
        #copy the test photo
        copyfile('test/photo.bmp', 'tmp/photo.bmp')
        p.Process(['convtobmp','convtosvg','fixsvg','convtog','trans'])
    elif i==3:
        #copy the test photo
        copyfile('test/photo.gcode', 'tmp/photo.gcode')
        p.Process(['trans'])
    elif i==4:
        #copy the test photo
        copyfile('test/photo.bmp', 'tmp/photo.bmp')
        p.Process(['convtobmp','convtosvg','fixsvg','convtog'])
    elif i==5:
        #render output to screen
        p.Process(['takepic','convtobmp','convtosvg','fixsvg','convtog'])
        v=pictoplot.view.ViewGCode()
        v.Render('tmp/photo.gcode',scale=8,drawbox=True)
    elif i==6:
        #Send Home
        p.Home()
    else:
        p.Process(['takepic','convtobmp','convtosvg','fixsvg','convtog','trans'])

if __name__ == "__main__":
   main(sys.argv[1:])
   






