import serial
#import pdb; pdb.set_trace()
import matplotlib.pyplot as plt
import numpy as np
import time


p = serial.Serial(port='/dev/cu.usbserial-A400eLxm', baudrate=115200,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=0)
#plt.axis([0, 10, 0, 1])
plt.ion()

samples = 500
x = np.arange(samples)
y = np.zeros(samples)
i = 0
freq = 1000.0 #hz
T = samples/freq

f = open("data.txt","w")
start = time.time()

while(1):
    try:
        plt.clf()
        plt.xlabel("Time(s)")
        plt.xlim(0, samples)
        plt.ylim(0, 5.2)

        i = 0
        while i < samples:
            value = p.readline()
            try:
                value = float(value)*(5.0/1023.0)
                y[i] = value
                x[i] = i
                i = i +1
            except ValueError: pass
        
        end = time.time()
        if (( end - start) > T):
            for w in y:
                f.write("%f\n"%w)
            start = time.time()
        plt.plot(x[:samples/2], np.fft.fft(y).real[:samples/2])
        plt.pause(1.0/60.0)
        

    except KeyboardInterrupt:
        plt.close()
        break
f.close()
p.close()





