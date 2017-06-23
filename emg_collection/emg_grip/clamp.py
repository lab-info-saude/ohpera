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
<<<<<<< HEAD
#a = raw_input("Start type 0, nothing")
#k0 = seize(0)
print "no weight"
a = raw_input("Start type 0, open")
k1 = seize(0)
=======
a = raw_input("Start type 0, nothing")
k0 = seize(0)
>>>>>>> b46a262f9dc920634d5ed82200c3ce64a588979a

a = raw_input("Start type 1, closed midforce")
k2 = seize(1)

print "weight"
a = raw_input("Start type 1, closed allforce")
k3 = seize(2)


p.close()

##saving to file
<<<<<<< HEAD
k = np.hstack((k1,k2, k3)).T
=======
k = np.hstack((k0,k1,k2)).T
>>>>>>> b46a262f9dc920634d5ed82200c3ce64a588979a

np.save("./data/data_%s"%time.strftime("%H%M%S"), k)




