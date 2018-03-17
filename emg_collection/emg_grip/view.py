import serial
import matplotlib.pyplot as plt
import numpy as np
#pd = '/dev/cu.usbserial-A400eLxm'
pd = '/dev/cu.usbmodem0E216FE1'

p = serial.Serial(port=pd, baudrate=230400,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
p.flushInput()
plt.ion()

samples = 2048
x = np.arange(samples)
y = np.zeros(samples)
i = 0
level = np.ones(samples)

def HP(signal, fc):
    s_kernel = int(round(samples*(fc/2500.)))
    kernel = np.hstack((np.zeros(s_kernel),np.ones(signal.shape[0]- 2*s_kernel), np.zeros(s_kernel)))
    Y = np.multiply(kernel, np.fft.fft(signal))
    return np.fft.ifft(Y).real


def LP(signal, fc):
    s_kernel = int(round(samples*(fc/2500.)))
    kernel = np.hstack((np.ones(s_kernel), np.zeros(signal.shape[0]- 2*s_kernel), np.ones(s_kernel)))
    Y = np.multiply(kernel, np.fft.fft(signal))
    return np.fft.ifft(Y).real

####NOTCH FOR ALL
def notch_all(signal, q=28, fs=2500.):
    s_60 = int(round(signal.shape[0]*(60./fs)))
    s_120 = int(round(signal.shape[0]*(120./fs)))
    s_180 = int(round(signal.shape[0]*(180./fs)))
    s_240 = int(round(signal.shape[0]*(240./fs)))
    s_300 = int(round(signal.shape[0]*(300./fs)))
    s_420 = int(round(signal.shape[0]*(420./fs)))
    
    k1 = np.hstack((np.ones(s_60 - int(q/2)), np.zeros(q), np.ones(signal.shape[0]-q - 2*s_60), np.zeros(q),np.ones(s_60 - int(q/2))))
    k2 = np.hstack((np.ones(s_120 - int(q/2)), np.zeros(q), np.ones(signal.shape[0]-q - 2*s_120), np.zeros(q),np.ones(s_120 - int(q/2))))
    k3 = np.hstack((np.ones(s_180 - int(q/2)), np.zeros(q), np.ones(signal.shape[0]-q - 2*s_180), np.zeros(q),np.ones(s_180 - int(q/2))))
    k4 = np.hstack((np.ones(s_240 - int(q/2)), np.zeros(q), np.ones(signal.shape[0]-q - 2*s_240), np.zeros(q),np.ones(s_240 - int(q/2))))
    k5 = np.hstack((np.ones(s_300 - int(q/2)), np.zeros(q), np.ones(signal.shape[0]-q - 2*s_300), np.zeros(q),np.ones(s_300 - int(q/2))))
    k6 = np.hstack((np.ones(s_420 - int(q/2)), np.zeros(q), np.ones(signal.shape[0]-q - 2*s_420), np.zeros(q),np.ones(s_420 - int(q/2))))
    
    Y = np.multiply(np.multiply(np.multiply(np.multiply(np.multiply(np.multiply(k1, k2), k3), k4),k5), k6), np.fft.fft(signal))
    return np.fft.ifft(Y).real


while(1):
    try:
        plt.clf()
        plt.xlabel("Time(s)")
        plt.xlim(0, samples)
        plt.ylim(-0.5, 0.5)
        i = 0
        while i < samples:
            #v_control = p.read() #signal normally is not 0, if 0 go to next
                #if(ord(v_control) == 0):
            value1 = p.read()
            value2 = p.read()

            try:
                v = ord(value1[0])*256 + ord(value2[0])
                y[i] = float(v)*(3.6/4095.)#(1.1/1023.0)
                x[i] = i
                i = i +1
            except IndexError:
                pass
        
        #y = y - y.mean()

        y = notch_all(LP(HP(y,20), 500))
    
        rms = np.sqrt(pow(y,2).mean())
        #print "RMS:",rms
        plt.title("RMS(x1000) %.3f"%(rms*1000))
        plt.plot(x, y)
        plt.plot(rms*level, c='r')
        plt.pause(1.0/60.0)
        

    except KeyboardInterrupt:
        plt.close()
        break

p.close()





