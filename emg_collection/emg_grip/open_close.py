import serial
import matplotlib.pyplot as plt
import numpy as np
pd = '/dev/cu.usbserial-A400eLxm'
#pd = '/dev/cu.usbmodem0E216FE1'

p = serial.Serial(port=pd, baudrate=230400,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
p.flushInput()
plt.ion()

samples = 1024
x = np.arange(samples)
y = np.zeros(samples)
i = 0
level = np.ones(samples)

def HP(signal, fc):
    s_kernel = round(samples*(fc/1904.))
    kernel = np.hstack((np.zeros(s_kernel),np.ones(signal.shape[0]- 2*s_kernel), np.zeros(s_kernel)))
    Y = np.multiply(kernel, np.fft.fft(signal))
    return np.fft.ifft(Y).real


def LP(signal, fc):
    s_kernel = round(samples*(fc/1904.))
    kernel = np.hstack((np.ones(s_kernel), np.zeros(signal.shape[0]- 2*s_kernel), np.ones(s_kernel)))
    Y = np.multiply(kernel, np.fft.fft(signal))
    return np.fft.ifft(Y).real


while(1):
    try:
        plt.clf()
        plt.xlabel("Time(s)")
        plt.xlim(0, samples)
        plt.ylim(-0.6, 0.6)
        i = 0
        while i < samples:
            v_control = p.read() #signal normally is not 0, if 0 go to next
            if(ord(v_control) == 0):
                value1 = p.read()
                value2 = p.read()

                try:
                    v = ord(value1[0])*256 + ord(value2[0])
                    y[i] = float(v)*(1.1/1023.0)
                    x[i] = i
                    i = i +1
                except IndexError:
                    pass
        
        y = y - y.mean() # no DC allowed D:
        #for i in x: removing noise in a bad way
            #if ((y[i] >=-0.05)and(y[i]<=0.05)):
            #   y[i]= 0.


        #y = LP(HP(y,20), 500)
    
        rms = np.sqrt(pow(y,2).mean())
        print "RMS:",rms
        if (rms > 0.04):
            plt.title("The hand is open :D")
        else:
            plt.title("The hand is closed D:")
        plt.plot(x, y)
        plt.plot(rms*level, c='r')
        plt.pause(1.0/60.0)
        

    except KeyboardInterrupt:
        plt.close()
        break

p.close()





