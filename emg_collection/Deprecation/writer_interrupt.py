import serial
import matplotlib.pyplot as plt
import os
import numpy as np
import time
pd = '/dev/cu.usbserial-A400eLxm'
#pd = '/dev/cu.usbmodem0E216FE1'

p = serial.Serial(port=pd, baudrate=230400,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
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
        plt.ylim(-0.5, 3.5)
        i = 0
        while i < samples:
            value1 = p.read()
            value2 = p.read()
            try:
                v = ord(value1[0])*256 + ord(value2[0])
                y[i] = float(v)*(3.3/4095) #*(5.0/1023.0)
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






