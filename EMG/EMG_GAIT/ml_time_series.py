import numpy as np
import math as m
def generate_envelope(original_data, num_samples):
    new_Xc = np.array([])
    if num_samples < len(original_data):
        if len(original_data.shape) == 1:
            for i in np.arange(num_samples - 1, original_data.shape[0]):
                x = original_data[i - (num_samples - 1) : i+1].ravel()
                if new_Xc.shape[0] == 0:
                    new_Xc = x
                else:
                    new_Xc = np.vstack((new_Xc, x))
        else:
            for i in np.arange(num_samples - 1, original_data.shape[0]):
                x = original_data[i - (num_samples - 1) : i+1, :].ravel()
                if new_Xc.shape[0] == 0:
                    new_Xc = x
                else:
                    new_Xc = np.vstack((new_Xc, x))
    else:
        print 'num_samples must be lower than original_data.'

    return new_Xc


#Features Extractions on EMGs

## RMS ##
def rms(a, window_size):
    def subrms(a, window_size):
        a2 = np.power(a,2)
        window = np.ones(window_size)/float(window_size)
        return np.sqrt(np.convolve(a2, window, 'valid'))

    for i in range(a.shape[1]):
        if i == 0:
            Xc = subrms(a[:, i], window_size)
        else:
            Xcp = subrms(a[:, i], window_size)
            Xc = np.vstack((Xc,Xcp))
    Xc = np.transpose(Xc)
    return Xc[:-1,:]

## MAV ##
def mav(a, window_size):
    def submav(a, window_size):
        a = np.abs(a)
        window = np.ones(window_size)/float(window_size)
        return np.convolve(a, window, 'valid')


    for i in range(a.shape[1]):
        if i == 0:
            Xc = submav(a[:, i], window_size)
        else:
            Xcp = submav(a[:, i], window_size)
            Xc = np.vstack((Xc,Xcp))
    Xc = np.transpose(Xc)
    return Xc[:-1,:]


## VAR ##
def f_var(a, window_size):
    def subf(a, window_size):
        Z = np.array([])
        for i in range(len(a)-window_size):
            Z = np.append(Z,np.var(a[i:window_size+i]))
        return Z

    for i in range(a.shape[1]):
        if i == 0:
            Xc = subf(a[:, i], window_size)
        else:
            Xcp = subf(a[:, i], window_size)
            Xc = np.vstack((Xc,Xcp))
    return np.transpose(Xc)


## ENTROPY ##
def f_entropy(a, window_size):
    def subentropy(a, window_size):
        Z = np.array([])
        for i in range(len(a)-window_size):
            Z = np.append(Z,.5*m.log(2*m.pi*m.exp(1)*(np.var(a[i:window_size+i])),2))
        return Z

    for i in range(a.shape[1]):
        if i == 0:
            Xc = subentropy(a[:, i], window_size)
        else:
            Xcp = subentropy(a[:, i], window_size)
            Xc = np.vstack((Xc,Xcp))
    return np.transpose(Xc)



## WL ##
def wl(a, window_size):
    wl = []

    for j in range(a.shape[1]):
        if j == 0:
            for i in range(a.shape[0]-window_size):
                wl.append(sum(np.abs(a[i+1:window_size+i,j]-a[i:window_size+i-1,j])))
            wl = np.array(wl)

        else:
            wlp = []
            for i in range(a.shape[0]-window_size):
                wlp.append(sum(np.abs(a[i+1:window_size+i,j]-a[i:window_size+i-1,j])))
            wlp = np.array(wlp)
            wl = np.vstack((wl,wlp))

    return np.transpose(wl)

## IEMG ##
def f_iemg(a, window_size):
    def sub_f_iemg(a, window_size):
        Z = np.array([])
        for i in range(len(a)-window_size):
            Z = np.append(Z,(np.abs(a[i:window_size+i]).sum()))
        return Z

    for i in range(a.shape[1]):
        if i == 0:
            iemg = sub_f_iemg(a[:, i], window_size)
        else:
            iemgp = sub_f_iemg(a[:, i], window_size)
            iemg = np.vstack((iemg,iemgp))
    return np.transpose(iemg)


## WAMP ##

## ZC ##

def help_ml():
    print ('\n 1 - rms(Xc, window_size)\n 2 - mav(Xc, window_size)\n 3 - f_var(Xc, window_size)\n 4 - f_entropy(Xc, window_size)\n 5 - wl(Xc, window_size)\n 6 - f_iemg(Xc, window_size)\n 7 - wamp(a, alpha) - Not implemented\n 8 - zc(a, alpha) - Not implementeds')
