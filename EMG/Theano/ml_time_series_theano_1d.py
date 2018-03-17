import os
import numpy as np
import theano
from theano import tensor as T
import timeit
import ml_time_series as mls

def generate_envelope_1d_T(original_data, num_samples):
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

    # Remove header, Nan and trash
    data = np.load('DB_1d/'+FILE_+'.npy')
    Xc_1 = data[:10000 ,0]
    Xc_2 = data[10000: ,0]

    print '\nXc_1 cleaned shape ', Xc_1.shape
    print 'Xc_2 cleaned shape ', Xc_2.shape

    #Create temporal serie
    NUM_SAMPLES = 50
    #NUM_COLS = Xc_1.shape[1]


    Xc_1 = generate_envelope_1d_T(Xc_1, NUM_SAMPLES)
    Xc_2 = generate_envelope_1d_T(Xc_2, NUM_SAMPLES)


    print 'Xc_1 temporal-serie shape ', Xc_1.shape
    print 'Xc_2 temporal-serie shape ', Xc_2.shape

    #Labeling the type of movement
    C = (np.ones(len(Xc_1))*0).reshape((len(Xc_1),1))
    Xc_1 = np.hstack((Xc_1.reshape(Xc_1.shape),C.reshape((len(Xc_1),1))))


    C = (np.ones(len(Xc_2))*1).reshape((len(Xc_2),1))
    Xc_2 = np.hstack((Xc_2.reshape(Xc_2.shape),C.reshape((len(Xc_2),1))))

    print 'Xc labeled shape ', Xc_1.shape
    print 'Xc labeled shape ', Xc_2.shape

    # Salving in file on the folder <classifier_data>
    np.save('./preprocessed_data_t/'+FILE_+'ot', Xc_1, allow_pickle=False)
    print FILE_+'op.npy'

    np.save('./preprocessed_data_t/'+FILE_+'pt', Xc_2, allow_pickle=False)
    print FILE_+'pp.npy'

    DATA.append(FILE_+'ot.npy')
    DATA.append(FILE_+'pt.npy')

def proccess_data(FILE_,DATA,NUM_SAMPLES,LABEL):

    # Remove header, Nan and trash
    data = np.load('DB_1d/'+FILE_+'.npy')
    Xc_1 = data[:10000 ,0]
    Xc_2 = data[10000: ,0]

    print '\nXc_1 cleaned shape ', Xc_1.shape
    print 'Xc_2 cleaned shape ', Xc_2.shape

    #Create temporal serie
    NUM_SAMPLES = 50
    #NUM_COLS = Xc_1.shape[1]


    Xc_1 = mls.generate_envelope(Xc_1, NUM_SAMPLES)
    Xc_2 = mls.generate_envelope(Xc_2, NUM_SAMPLES)

    #Labeling the type of movement
    C = (np.ones(len(Xc_1))*0).reshape((len(Xc_1),1))
    Xc_1 = np.hstack((Xc_1.reshape(Xc_1.shape),C.reshape((len(Xc_1),1))))


    C = (np.ones(len(Xc_2))*1).reshape((len(Xc_2),1))
    Xc_2 = np.hstack((Xc_2.reshape(Xc_2.shape),C.reshape((len(Xc_2),1))))

    print 'Xc labeled shape ', Xc_1.shape
    print 'Xc labeled shape ', Xc_2.shape

    # Salving in file on the folder <classifier_data>
    np.save('./preprocessed_data/'+FILE_+'op', Xc_1, allow_pickle=False)
    print FILE_+'op.npy'

    np.save('./preprocessed_data/'+FILE_+'pp', Xc_2, allow_pickle=False)
    print FILE_+'pp.npy'

    DATA.append(FILE_+'op.npy')
    DATA.append(FILE_+'pp.npy')

files_w = ['data_220833','data_220853','data_220915','data_220933', 'data_220951',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
            '14', '15', '16', '17', '18', '18', '20', '21', '22', '23', '24',
            '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
            '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46',
            '47', '48', '49', '50']

NUM_SAMPLES = 50
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
