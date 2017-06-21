import serial
import matplotlib.pyplot as plt
import os
import numpy as np
import time

p = serial.Serial(port='/dev/cu.usbserial-A400eLxm', baudrate=230400,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=None)
#plt.axis([0, 10, 0, 1])
plt.ion()

samples = 1024
x = np.arange(samples)
y = np.zeros(samples)
i = 0

max_freq = 0
min_freq = 1e13
fail_counter = 0
n = 0
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
            except ValueError:
                print "fail"
                fail_counter=fail_counter+1
        #saving
        np.save("./archive/TemporaryItems/dataframe_%d"%n, y)
        n = n+1
        plt.plot(x, y)
        plt.pause(1.0/60.0)
        

    except KeyboardInterrupt:
        plt.close()
        break
p.close()

print "total fails in normal mode:", fail_counter
#deleting dataframes and generating one
new = np.array([])
for i in xrange(1, n):
    new  = np.append(new, np.load("./archive/TemporaryItems/dataframe_%d.npy"%i))
    os.system("rm ./archive/TemporaryItems/dataframe_%d.npy"%i)
np.savetxt("./archive/data.txt", new)
print "Finished"
print"\n\n\n\n"






