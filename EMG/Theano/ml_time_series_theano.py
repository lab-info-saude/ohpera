import os
import numpy as np
import theano
from theano import tensor as T
import timeit
import ml_time_series as mls

def generate_envelope_T(original_data, num_samples):
    # initialize
    new_Xc = np.array([])
    x = T.fmatrix('x')
    w = theano.shared(num_samples-1)
    update = [(w, w + 1)]
    envelope1d = x[0][w - (num_samples - 1) : w+1].ravel()

    # compile model
    net_input = theano.function(inputs=[x],
                                updates=update,
                                outputs=envelope1d)

    # execute
    X_input =  np.array([(original_data)],
                          dtype=theano.config.floatX)
    if num_samples < len(original_data):
        new_Xc = net_input(X_input)
        for i in np.arange(num_samples , original_data.shape[0]):
            new_Xc = np.vstack((new_Xc, net_input(X_input)))
    else:
        print 'num_samples must be lower than original_data.'

    return new_Xc

def generate_envelope_nd_T(original_data, num_samples):
    # initialize
    new_Xc = np.array([])
    x = T.dmatrix('x')
    w = theano.shared(num_samples-1)
    update = [(w, w + 1)]
    envelope_nd = x[w-(num_samples-1):w+1][0 : num_samples, :].ravel()

    # compile model
    net_input = theano.function(inputs=[x],
                                updates=update,
                                outputs=envelope_nd)
    # execute
    X_input =  np.array((original_data),
                          dtype=theano.config.floatX)

    if num_samples < len(original_data):
        new_Xc = net_input(X_input)
        for i in np.arange(num_samples, original_data.shape[0]):
            new_Xc = np.vstack((new_Xc, net_input(X_input)))

    else:
        print 'num_samples must be lower than original_data.'
    return new_Xc


################################## Processing ##################################

def proccess_data_t(FILE_,DATA,NUM_SAMPLES,LABEL):

    Xc = np.genfromtxt('DB_nd/'+FILE_+'.txt', delimiter=",", usecols=(1,2,3,4))

    print '\nXc shape ', Xc.shape

    #Create temporal serie
    Xc = mls.generate_envelope(Xc, NUM_SAMPLES)
    print 'Xc temporal-serie shape ', Xc.shape

    #Labeling the type of movement
    C = (np.ones(len(Xc))*LABEL).reshape((len(Xc),1))
    Xc = np.hstack((Xc.reshape(Xc.shape),C.reshape((len(Xc),1))))
    print 'Xc labeled shape ', Xc.shape

    np.save('./preprocessed_data_t/'+FILE_, Xc, allow_pickle=False)
    print FILE_+'.npy'

    DATA.append(FILE_+'.npy')

def proccess_data(FILE_,DATA,NUM_SAMPLES,LABEL):

    Xc = np.genfromtxt('DB_nd/'+FILE_+'.txt', delimiter=",", usecols=(1,2,3,4))

    print '\nXc shape ', Xc.shape

    #Create temporal serie
    Xc = mls.generate_envelope(Xc, NUM_SAMPLES)
    print 'Xc temporal-serie shape ', Xc.shape

    #Labeling the type of movement
    C = (np.ones(len(Xc))*LABEL).reshape((len(Xc),1))
    Xc = np.hstack((Xc.reshape(Xc.shape),C.reshape((len(Xc),1))))
    print 'Xc labeled shape ', Xc.shape

    np.save('./preprocessed_data/'+FILE_, Xc, allow_pickle=False)
    print FILE_+'.npy'

    DATA.append(FILE_+'.npy')

#files_w = ['data_w_1', 'data_w_2', 'data_w_3', 'data_w_4', 'data_w_5']
files_w = ['data_w_1']

NUM_SAMPLES = 500
DATA = []

start = timeit.default_timer()
print ('Envelopamento sem Theano.')
for i in files_w:
    proccess_data(i,DATA,NUM_SAMPLES,0)
stop = timeit.default_timer()
ti1 = stop - start

start = timeit.default_timer()
print ('Envelopamento com Theano.')
for i in files_w:
    proccess_data_t(i,DATA,NUM_SAMPLES,0)
stop = timeit.default_timer()
ti2 = stop - start

print ('Tempo total para o envelopamento sem Theano: %.2f min' % (ti1/60))
print ('Tempo total para o envelopamento com Theano: %.2f min' % (ti2/60))
