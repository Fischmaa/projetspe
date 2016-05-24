
# coding: utf-8

# In[9]:

import pandas as pd
import math as mt
import matplotlib.pyplot as plt
import numpy as np

import plotly.offline as pl
import plotly.graph_objs as go

pl.offline.init_notebook_mode()


# In[10]:

train = pd.read_csv('/home/valerian/Projets/Projet_spe/projetspe/expedia/train.csv', iterator = True, chunksize = 100000)

#à la volée 
for chunk in train :
    #nuage de point
    #plt
    plt.scatter(chunk['user_id'], chunk['orig_destination_distance'])
    #pl
    data_user = pd.Series(chunk['user_id'])
    data_dist = pd.Series(chunk['orig_destination_distance'])
    
    # Create a trace
    trace = go.Scatter(
        x = data_user,
        y = data_dist,
        mode = 'markers'
    )
    
    data = [trace]
    
    pl.iplot(data)


# In[ ]:



