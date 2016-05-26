
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[20]:

data = pd.read_csv('trainRandomSample.csv')


# In[21]:

data=data.drop('Unnamed: 0',1)
data=data.sort_values("date_time")


# In[22]:

data.head()


# In[23]:

data=data.reset_index()
data=data.drop("index",1)


# In[24]:

data


# In[26]:

data = data.drop_duplicates(['date_time'], keep='last')


# In[28]:

data.to_csv('randomTrain.csv')


# In[55]:




# In[ ]:



