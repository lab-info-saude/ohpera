#THEANO_FLAGS=device=cpu,floatX=float64 python your_script.py
#THEANO_FLAGS=device=gpu,floatX=float32 python your_script.py

import theano
from theano import tensor as T
import numpy as np

# initialize
x = T.fmatrix(name='x')
x_sum = T.sum(x, axis=0)

# compile
calc_sum = theano.function(inputs=[x], outputs=x_sum)

# execute (Python list)
ary = [[1, 2, 3], [1, 2, 3]]
print ('Colum sum:', calc_sum(ary))

# execute (NumPy array)
ary = np.array([[1, 2, 3], [1, 2, 3]], dtype=theano.config.floatX)
print ('Colum sum:', calc_sum(ary))
