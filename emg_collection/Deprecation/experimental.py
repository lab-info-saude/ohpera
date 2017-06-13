#import pdb
#pdb.set_trace()
import serial

import numpy as np
import time
import matplotlib.pyplot as plt

p = serial.Serial(port='/dev/cu.usbserial-A400eLxm', baudrate=115200,
                  bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)
freq = 2025 # hertz
timeWindow = 3 # seconds
bufferSize = timeWindow * freq
buffer = []
plt.ion()
tamanho = 0
while(1):
    try:
        value = p.readline()
        if (value != ""):
            tamanho = tamanho + len (value)
            value = float(value)
            if (len(buffer) < bufferSize) :
                buffer.append(value)
            else:
                print(buffer)
                print(tamanho)
                buffer =[]
                tamanho = 0;
    except KeyboardInterrupt:
        plt.close()
        break
p.close()
