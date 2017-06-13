import serial
import matplotlib.pyplot as plt

import numpy as np
import time

p = serial.Serial(port='/dev/cu.usbserial-A400eLxm', baudrate=230400,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=None)
#plt.axis([0, 10, 0, 1])
plt.ion()

samples = 1000
x = np.arange(samples)
y = np.zeros(samples)
i = 0

max_freq = 0
min_freq = 1e13
fail_counter = 0

while(1):
    try:
        plt.clf()
        plt.xlabel("Time(s)")
        plt.xlim(0, samples)
        plt.ylim(0, 5.2)

        start = time.time()
        i = 0
        while i < samples:
            value = p.readline()
            try:
                value = float(value)*(5.0/1023.0)
                y[i] = value
                x[i] = i
                i = i +1
            except ValueError:
                    fail_counter = fail_counter+1
        
        freq = float(samples)/(time.time() - start)
        if freq > max_freq: max_freq = freq
        elif freq < min_freq: min_freq = freq

        plt.plot(x, y)
        plt.pause(1.0/60.0)
        

    except KeyboardInterrupt:
        plt.close()
        break

print "\nFreq max: %.3f kHz" %(max_freq/1000.0)
print "Freq min:%.3f kHz" %(min_freq/1000.0)
print "total missed:", fail_counter
p.close()





