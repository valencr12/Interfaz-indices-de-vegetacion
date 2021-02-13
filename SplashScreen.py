# -*- coding: utf-8 -*-
"""
Created on Sat May 16 12:23:44 2020

@author: Usuario
"""

# Importación de libreria para crear la Splash Screen
try:
    from Tkinter import *  # Python2
    from Tkinter import ttk
except ImportError:
    from tkinter import *  # Python3
    from tkinter import ttk
import ctypes   
 
# Función para destruir la Splash Screen
def close_splash():
    launcher.destroy()

# Función para crear la Splash Screen
def splash_screen():
    global launcher
    class Application(ttk.Frame):
        def __init__(self, launcher):
            super().__init__(launcher)
            self.style = ttk.Style(self)
            self.style.theme_use("classic")
            self.style.configure("black.Horizontal.TProgressbar",background='#A5BF13')        
            self.progressbar = ttk.Progressbar(self, mode="determinate", style='black.Horizontal.TProgressbar')
            self.progressbar.place(x=0, y=0, width=680)
            self.progressbar.start(50)            
            self.place(x=0, y=361, width=680, height=20)
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()
            ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)          
            control_ancho = int((ancho-680)/2)
            control_alto = int((alto-381)/2)    
            launcher.geometry('{}x{}+{}+{}'.format(680, 381, control_ancho, control_alto)) 

    launcher = Tk()
    launcher.overrideredirect(True)
    launcher.attributes("-toolwindow",-1)
    imagen=PhotoImage(file="IMG0_fondo_splash.png")
    fondo=Label(launcher, image=imagen).pack()
    launcher.after(4990,close_splash)
    app = Application(launcher)
    app.mainloop()

    
