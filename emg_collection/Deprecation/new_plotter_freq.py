import serial
import matplotlib.pyplot as plt
#import multiprocessing
import numpy as np
import time
#import pdb
#pdb.set_trace


def worker():
    p = serial.Serial(port='/dev/cu.usbserial-A400eLxm', baudrate=230400,
                      bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=None)
    #plt.axis([0, 10, 0, 1])
    plt.ion()
    samples = 512
    y = np.zeros(samples)
    i = 0
    freq  = 2025.0
    xtick= np.linspace(-500, 500, 11)
    f = np.linspace(-float(freq)/2, float(freq)/2, samples)
    while(1):
  
        try:
            plt.clf()
            plt.xlabel("Freq(Hz)")
            #plt.xlim(100, 200)
            #plt.xticks(xtick)
            plt.xlim(-2, 100)
            plt.ylim(0, 1000)
            i = 0
            while i < samples:
                value = p.read(2)
                try:
                    if (ord(value[1]) >= ord(value[0])):
                        v = ord(value[0])*256 + ord(value[1])
                    else:
                        v = ord(value[1])*256 + ord(value[0])
                    y[i] = float(v)*(5.0/1023.0)
                    i = i +1
                except ValueError: pass
        
            Y = np.abs(np.fft.fftshift(np.fft.fft(y)))
            #Y = np.abs(np.fft.fft(y))
            st = time.time()
           #f = np.linspace(0, freq, samples)
            plt.plot(f, Y)
            print time.time() - st
            plt.pause(1.0/15.0)
        

        except KeyboardInterrupt:
            plt.close()
            p.close()
            break


worker()





