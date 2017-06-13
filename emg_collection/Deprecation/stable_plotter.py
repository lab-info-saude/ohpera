#import pdb
#pdb.set_trace()
import serial
import matplotlib.pyplot as plt

import numpy as np
import time


p = serial.Serial(port='/dev/cu.usbserial-A400eLxm', baudrate=115200,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=0)
#plt.axis([0, 10, 0, 1])
plt.ion()

fd = 2000.0
samples = 2000
x = np.linspace(0,float(samples)/fd, samples )
y = np.zeros(samples)
i = 0

max_freq = 0
min_freq = 1e13

c =0
T =1.0/fd
r = 0
bg = time.time()
while(1):
    try:
        plt.clf()
        plt.xlabel("Time(s)")
        plt.xlim(0, np.max(x))
        plt.ylim(-5.2, 5.2)

        i = 0
        st = time.time()
        while i < samples:
            start = time.time()
            p.write("k")
            value = p.readline()
            try:
                value = float(value)*(5.0/1023.0)
                y[i] = value
                i = i +1
                time.sleep(T)
                delta = (time.time() - start)
                freq = 1.0/delta
                T = T*(freq/(fd+40.0))
            except ValueError: pass
    
        f_real = float(samples)/(time.time() - st)
        error = (np.abs(f_real-fd)/fd)*100
        
        print "%.2f"%f_real, "%.2f"%(1/(T*(f_real/fd))),"%.2f"%error, "percent error"
        if (error > 2.0):  c=c+1
        r = r+1
        if f_real> max_freq: max_freq = f_real
        elif f_real < min_freq: min_freq = f_real

        plt.plot(x, y)
        plt.pause(1.0/60.0)
        

    except KeyboardInterrupt:
        plt.close()
        break
fin = time.time()
p.close()

dt = fin - bg
print"\n\n\n\n"
print "\nFreq max: %.3f Hz" %(max_freq)
print "Freq min:%.3f Hz" %(min_freq)
print "Expected freq: %.3f Hz"%fd
print "Total time with error above 2pct : %.4f s"%(dt*c/r)
print "Total time: %.4fs"%(dt)
print "Percent of the time with error >= 2pct : %.2f pct"%(c*100/r)
print"\n\n\n\n"
p.close()





