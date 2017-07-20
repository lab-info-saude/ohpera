import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import serial
import scipy as sp
from scipy import signal
from sklearn.externals import joblib

#loading network
"""
f = open("forest.pkl", "r")
clf = pickle.loads(f.read())
f.close()
print "Model loaded"
"""
#opening port
pd = '/dev/cu.usbserial-A400eLxm'
p = serial.Serial(port=pd, baudrate=230400, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE)

## Defining the filter  for the signal
def filter_signal(emg, low_pass=10., sfreq=2000., high_band=20., low_band=450.):
    """
    emg: EMG data
    high: high-pass cut off frequency
    low: low-pass cut off frequency
    sfreq: sampling frequency
    """

    # normalise cut-off frequencies to sampling frequency
    high_band = high_band/(sfreq/2)
    low_band = low_band/(sfreq/2)

    # create bandpass filter for EMG
    b1, a1 = sp.signal.butter(4, [high_band,low_band], btype='bandpass')

    # process EMG signal: filter EMG
    emg_filtered = sp.signal.filtfilt(b1, a1, emg)

    # process EMG signal: rectify
    emg_rectified = abs(emg_filtered)

    # create lowpass filter and apply to rectified signal to get EMG envelope
    low_pass = low_pass/sfreq
    b2, a2 = sp.signal.butter(4, low_pass, btype='lowpass')
    emg_envelope = sp.signal.filtfilt(b2, a2, emg_rectified)

    return emg_envelope



####NOTCH FOR ALL
def notch_all(signal, q=28, fs=1904.):
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





#Running and classifying
samples = 499
x = np.zeros((samples)) #allocating memory
y = np.zeros((samples))
print "Running"
while(1):
        #reading data and plotting
    plt.ion()
    try:
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

        ##scaling filtered data
        X_std = scale(notch_all(filter_signal(x))).reshape((1, -1))
        #print scale(filter_signal(x))
        ## classifying 0, 1, 2 - open, close, tightly closed
        """
        result =  clf.predict(X_std)[0]
        if (result==0.): print "Hand Open"
        elif(result==0.): print "Hand Closed"
        else: print "Hand Tightly Closed"
        print X_std.max(), X_std.min(),
        """
        #point to finish the code
    except KeyboardInterrupt:
        p.close()
        break

print "Finished"
