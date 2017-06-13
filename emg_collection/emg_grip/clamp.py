import serial
import numpy as np
import time
pd = '/dev/cu.usbserial-A400eLxm'
#pd = '/dev/cu.usbmodem0E216FE1'

p = serial.Serial(port=pd, baudrate=230400, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)

####KINDS
# 0 - nothing
# 1 - open
# 2 - closed

#function to acquire data
def seize(kind):
    samples = 2000 # about 1 sec
    x = np.zeros((samples))
    y = kind*np.ones((samples))
    i = 0

    while i < samples:
        v_control = p.read() #signal normally is not 0, if 0 go to next
        if(ord(v_control) == 0):

            value1 = p.read()
            value2 = p.read()
            try:
                v =  ord(value1[0])*256 + ord(value2[0])
                if (v<1024):
                    x[i] = v
                    i = i +1
            except IndexError:
                pass
    
    return np.vstack((x,y)) # (2, samples)


###BEGIN
a = raw_input("Start type 0, nothing")
k0 = seize(0)

a = raw_input("Start type 1, open")
k1 = seize(1)

a = raw_input("Start type 2, closed")
k2 = seize(2)

p.close()

##saving to file
k = np.hstack((k0,k1,k2)).T

np.save("./data/data_%s"%time.strftime("%H%M%S"), k)




