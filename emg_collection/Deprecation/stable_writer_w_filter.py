#import pdb
#pdb.set_trace()
import serial
import matplotlib.pyplot as plt
import os
import numpy as np
import time


def filter_kernel(size, fs, fhp, f1, f2):
    kernel = np.ones(size)
    fh = int(fhp/(fs)*size)
    fsp1 =  int(f1/(fs)*size)
    fsp2 =  int(f2/(fs)*size)
    #flp = int(fmax/(fs)*x.shape[0])
    
    for i in xrange(0, x.shape[0]):
        if (i <=fh) or ((i>=fsp1)and(i<=fsp2)):
            kernel[i] = 0
            kernel[-i] = 0

    return kernel

def filter(x, kernel):
    return np.fft.ifft(np.multiply(x, kernel)).real

p = serial.Serial(port='/dev/cu.usbserial-A400eLxm', baudrate=115200,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=0)
#plt.axis([0, 10, 0, 1])
plt.ion()



samples = 500
x = np.arange(samples)
y = np.zeros(samples)
i = 0


max_freq = 0
min_freq = 1e13
fd = 2000.0
c =0
T =1.0/fd
r = 0
kernel = filter_kernel(samples, fd, 10.0, 55.0, 65.0)
bg = time.time()
while(1):
    try:
        plt.clf()
        plt.xlabel("Time(s)")
        plt.xlim(0, samples)
        plt.ylim(0, 5.2)

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
                T = T*(freq/(fd+42.0))
            except ValueError: pass
    
        f_real = float(samples)/(time.time() - st)
        y = filter(y, kernel)
        error = (np.abs(f_real-fd)/fd)*100
        print f_real, "%.3f"%(1/(T*(f_real/fd))),"%.3f"%error, "percent error"
        #saving
        np.savetxt("./archive/TemporaryItems/dataframe_%d"%r, y)
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

#deleting dataframes and generating one
new = np.array([])
for i in xrange(1, r):
    new  = np.append(new, np.loadtxt("./archive/TemporaryItems/dataframe_%d"%i))
    os.system("rm ./archive/TemporaryItems/dataframe_%d"%i)
np.savetxt("./archive/data.txt", new)
print "Finished"
print"\n\n\n\n"




