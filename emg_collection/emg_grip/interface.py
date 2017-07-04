__author__ ='Ithallo Guimaraes'
import serial
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import Tkinter as tk
from Tkinter import *
import time

root = tk.Tk()
#opening port
pd = '/dev/cu.usbserial-A400eLxm' #pd = '/dev/cu.usbmodem0E216FE1'
p = serial.Serial(port=pd, baudrate=230400,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
p.flushInput()
### Read data from serial
def load_data(samples):
    i = 0
    y = np.zeros(samples)
    while i < samples:
        v_control = p.read() #signal normally is not 0, if 0 go to next
        if(ord(v_control) == 0):
            value1 = p.read()
            value2 = p.read()
            y[i] = ord(value1[0])*256 + ord(value2[0])
            i = i + 1
    return y

##test data
x = np.linspace(0,1./1904, 100)


def plot_things(x, y):
    fig = Figure(figsize=(5.5, 5.15))
    fig.plot(x, y)
    canv = FigureCanvasTkAgg(fig, master=root)
    canv.get_tk_widget().grid(row=0,column=0,columnspan=1)
    canv.draw()


root.title("EMG")
root.geometry("600x600+400+100")

y = load_data(100)
plot_things(x,y)


mainloop()
p.close()
