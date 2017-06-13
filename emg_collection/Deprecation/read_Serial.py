
# coding: utf-8

# In[13]:

import multiprocessing
import numpy as np
import time


# In[14]:

def worker():
    for i in range(1, 1000):
        print "hey"


# In[19]:

p  = multiprocessing.Process(target=worker, args=())


# In[20]:


s = time.time()
p.start()
e = time.time()
print (e-s)*1000, "ms"


# In[17]:


s = time.time()
worker()
e = time.time()
print (e-s)*1000, "ms"


# In[ ]:



