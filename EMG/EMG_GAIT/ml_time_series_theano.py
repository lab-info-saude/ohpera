import numpy as np
import theano
from theano import tensor as T

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
