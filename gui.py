# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 16:05:35 2023

@author: Sergey Zhuravlev
"""

import cv2 as cv
import matplotlib.pyplot as plt
from tkinter import *
from  tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import filedialog as fd
import imageio as iio
import numpy as np
from editor import edit

class mainWin:
    def __init__(self):

        self.mainWin = Tk()
        # self.mainWin.configure(background='#FFFFFF')
        self.mainWin.geometry('940x300')
        self.mainWin.title('Image transformer')
        
        self.iniImage = Figure(figsize = (3, 2), dpi = 100)
        self.iniImagePlot = FigureCanvasTkAgg(self.iniImage, master = self.mainWin)
        
        self.tarImage = Figure(figsize = (3, 2), dpi = 100)
        self.tarImagePlot = FigureCanvasTkAgg(self.tarImage, master = self.mainWin)
        
        self.resImage = Figure(figsize = (3, 2), dpi = 100)
        self.resImagePlot = FigureCanvasTkAgg(self.resImage, master = self.mainWin)
        
        self.iniPath = ''
        self.tarPath = ''
        
        # self.ini = np.nan
        # self.tar = np.nan
        # self.res = np.nan
        
        self.loadIniImageBut = Button(text = 'Upload your initial image', width = 40)
        self.loadTarImageBut = Button(text = 'Upload your target image', width = 40)
        self.transformBut = Button(text = 'Transform', width = 18)
        self.saveBut = Button(text = 'Save', width = 18)

        
        # functions
    
        def importIniImage(event):
            filename = fd.askopenfilename()
            
            self.iniPath = filename            
            self.ini = iio.imread(filename)
            
            self.iniImage.clear()
            plt1 = self.iniImage.add_subplot(111)            
            plt1.imshow(self.ini)
            plt1.axis('off')
            self.iniImagePlot.draw()
        
        def importTarImage(event):
            filename = fd.askopenfilename()
            
            self.tarPath = filename
            self.tar = iio.imread(filename)
            self.tarImage.clear()
            plt2 = self.tarImage.add_subplot(111)            
            plt2.imshow(self.tar)
            plt2.axis('off')
            self.tarImagePlot.draw()
        
            

        def transform(event):
            
            # print(self.iniPath)
            # print(self.tarPath)
            
            self.res = edit(self.iniPath, self.tarPath)
            
            self.resImage.clear()
            plt3 = self.resImage.add_subplot(111)            
            plt3.imshow(self.res)
            plt3.axis('off')
            self.resImagePlot.draw()
 
        
        def save(event):
            filename = fd.asksaveasfile(mode='w', defaultextension=".png")
            # print(filename.name)
            iio.imsave(filename.name, self.res)
                      
            
        
        # binding

        self.loadIniImageBut.bind('<ButtonRelease-1>', importIniImage)
        self.loadTarImageBut.bind('<ButtonRelease-1>', importTarImage)
        self.transformBut.bind('<ButtonRelease-1>', transform)
        self.saveBut.bind('<ButtonRelease-1>', save)
        
        
        
        # placing
        
        self.iniImagePlot.get_tk_widget().place(x = 10, y = 30)
        self.tarImagePlot.get_tk_widget().place(x = 320, y = 30)
        self.resImagePlot.get_tk_widget().place(x = 630, y = 30)
        
        self.loadIniImageBut.place(x = 15, y = 250)
        self.loadTarImageBut.place(x = 325, y = 250)
        self.transformBut.place(x = 635, y = 250)
        self.saveBut.place(x = 780, y = 250)
        
        
               
        

    def run(self):

        self.mainWin.mainloop()

mwin = mainWin()
mwin.run()    