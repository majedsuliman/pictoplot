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

import pygame
import pictoplot.lib


'''
Class to help with pygame iterface
'''
class Interface():
        c=None
        screen=None
        p=None
        
        def __init__(self,pictoplotlib,full=False):
                self.c = pygame.time.Clock() # create a clock object for timing
                #Set up pygame
                pygame.init()
                size=(640,480)
                #size=pygame.FULLSCREEN
                if full:
                        self.screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
                else:
                        self.screen = pygame.display.set_mode(size)
                self.p=pictoplotlib
                
        #Wait for the space bar to be pressed
        def Continue(self):
                events = pygame.event.get()
                for event in events:
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                        return False
                                if event.key == pygame.K_q:
                                        pygame.quit()
                                        quit
                return True
                                        
        #Wait for the space bar to be pressed
        def YesNo(self):
                events = pygame.event.get()
                for event in events:
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_y:
                                        return (False,True)
                                if event.key == pygame.K_n:
                                        return (False,False)
                                if event.key == pygame.K_q:
                                        pygame.quit()
                                        quit
                return (True,False)

        #Close pygame
        def ClosePyGame(self):
                pygame.quit()
        
        '''
        Method DisplaySplashScreen()
        This will display a splash screen and wait for spae bar to be pressed
        '''
        def DisplaySplashScreen(self):
                #Load the splash screen
                img=pygame.image.load("img/splash.bmp")#Load the splash screeen
                w, h = pygame.display.get_surface().get_size()
                img = pygame.transform.scale(img, (w, h))#scale the image to fit
                loop=True
                while loop:
                        self.screen.blit(img,(0,0))
                        pygame.display.flip() # update the display
                        self.c.tick(10) # only three images per second
                        loop=self.Continue()
               


        def showPhotoPreview(self):
                loop=True
                while loop:
                        self.p.TakePicture()
                        img=pygame.image.load("tmp/photo.bmp")
                        w, h = pygame.display.get_surface().get_size()
                        img = pygame.transform.scale(img, (w, h))#scale the image to fit
                        self.screen.blit(img,(0,0))
                        pygame.display.flip() # update the display
                        self.c.tick(10) # only three images per second
                        loop=self.Continue()

                            
        def showPBMPreview(self):
                loop=True
                while loop:
                        img=pygame.image.load("tmp/photo.pbm")
                        img2=pygame.image.load("img/overlay.png").convert_alpha()
                        #img2.set_alpha(128)
                        w, h = pygame.display.get_surface().get_size()
                        img = pygame.transform.scale(img, (w, h))#scale the image to fit
                        img2 = pygame.transform.scale(img2, (w, h))#scale the image to fit
                        self.screen.blit(img,(0,0))
                        self.screen.blit(img2,(0,0))
                        pygame.display.flip() # update the display
                        self.c.tick(10) # only three images per second
                        loop,s=self.YesNo()
                return s


        def showProcessing(self):
                loop=True
                img=pygame.image.load("tmp/photo.pbm")
                img2=pygame.image.load("img/processing.png").convert_alpha()
                w, h = pygame.display.get_surface().get_size()
                img = pygame.transform.scale(img, (w, h))#scale the image to fit
                img2 = pygame.transform.scale(img2, (w, h))#scale the image to fit
                self.screen.blit(img,(0,0))
                self.screen.blit(img2,(0,0))
                pygame.display.flip() # update the display
   
        def showPrinting(self):
                loop=True
                img=pygame.image.load("tmp/photo.pbm")
                img2=pygame.image.load("img/printing.png").convert_alpha()
                w, h = pygame.display.get_surface().get_size()
                img = pygame.transform.scale(img, (w, h))#scale the image to fit
                img2 = pygame.transform.scale(img2, (w, h))#scale the image to fit
                self.screen.blit(img,(0,0))
                self.screen.blit(img2,(0,0))
                pygame.display.flip() # update the display

        def Process(self):
                #p=PicToPlot(port="COM3",board=57600,threshold=0.5)
                #o=PicToPlotInterface(p)
                self.DisplaySplashScreen()
                MainLoop=True
                while MainLoop:
                        loop=True
                        while loop:
                                self.showPhotoPreview()
                                self.p.CovertToPBM()
                                loop=not self.showPBMPreview()

                        self.showProcessing()
                        self.p.ConvertToSVG()
                        self.p.FixSvgHeader()
                        self.p.ConvertToGCode()
                        self.showPrinting()
                        self.p.Transmit()
                        self.DisplaySplashScreen()

                self.ClosePyGame()

