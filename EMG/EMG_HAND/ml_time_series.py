import numpy as np
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
