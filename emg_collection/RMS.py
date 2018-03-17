 import serial
import matplotlib.pyplot as plt

import numpy as np
import time
pd = '/dev/cu.usbserial-A400eLxm'
#pd = '/dev/cu.usbmodem0E216FE1'

p = serial.Serial(port=pd, baudrate=230400,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
plt.ion()

samples = 50
y = np.zeros(samples)
i  = 0
n = 2000/samples
j = 0
f = np.zeros((n))
x = np.arange(n)
while(1):
    try:
        plt.clf()
        plt.xlabel("Time(s)")
        plt.xlim(0, n)
        plt.ylim(0, 1)

        j =0
        while j < n:

            i = 0
            while i < samples:
                value1 = p.read()
                value2 = p.read()

                try:
                    v = ord(value1[0])*256 + ord(value2[0])
                    y[i] = float(v)*(1.1/1023.0)
                    i = i +1
                except IndexError:
                    pass
  
            f[j] = np.sqrt(pow(y,2).mean())
            x[j] = j
            j = j + 1
        plt.plot(x, f)
        plt.pause(1.0/60.0)


    except KeyboardInterrupt:
        plt.close()
        break
p.close()





