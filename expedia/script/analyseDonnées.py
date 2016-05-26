
# coding: utf-8

# In[2]:

import pandas as pd 
import plotly


# In[3]:

import numpy as np
from plotly import __version__
py=plotly.offline
go =plotly.graph_objs
plotly.offline.init_notebook_mode()
from datetime import datetime
pd.options.mode.chained_assignment = None


# In[5]:

#read random train sample
train_NotBooking = pd.read_csv('../sampled_not_booking.csv',index_col=0).dropna()
print("length train_NotBooking : ",len(train_NotBooking))


# In[41]:

train_IsBooking = pd.read_csv('../sampled_booking.csv',index_col=0).dropna()
print("length train_IsBooking : ",len(train_IsBooking))


# In[6]:

train_NotBooking=train_NotBooking.reset_index()

train_NotBooking['date']=0

for i in range(len(train_NotBooking)) :
    train_NotBooking['date'][i]=datetime.strptime(train_NotBooking['date_time'][i],'%Y-%m-%d %H:%M:%S')

train_NotBooking['dayOfWeek']=0

for i in range(len(train_NotBooking)):
    train_NotBooking['dayOfWeek'][i]=train_NotBooking['date'][i].isoweekday()

train_NotBooking['year']=0

for i in range(len(train_NotBooking)):
    train_NotBooking['year'][i]=train_NotBooking['date'][i].year

train_NotBooking['month']=0

for i in range(len(train_NotBooking)):
    train_NotBooking['month'][i]=train_NotBooking['date'][i].month

train_NotBooking['day']=0

for i in range(len(train_NotBooking)):
    train_NotBooking['day'][i]=train_NotBooking['date'][i].day


# In[ ]:

train_IsBooking=train_IsBooking.reset_index()

train_IsBooking['date']=0

for i in range(len(train_IsBooking)) :
    train_IsBooking['date'][i]=datetime.strptime(train_IsBooking['date_time'][i],'%Y-%m-%d %H:%M:%S')

train_IsBooking['dayOfWeek']=0

for i in range(len(train_IsBooking)):
    train_IsBooking['dayOfWeek'][i]=train_IsBooking['date'][i].isoweekday()

train_IsBooking['year']=0

for i in range(len(train_IsBooking)):
    train_IsBooking['year'][i]=train_IsBooking['date'][i].year

train_IsBooking['month']=0

for i in range(len(train_IsBooking)):
    train_IsBooking['month'][i]=train_IsBooking['date'][i].month

train_IsBooking['day']=0

for i in range(len(train_IsBooking)):
    train_IsBooking['day'][i]=train_IsBooking['date'][i].day


# In[1]:

def histogram(dataframe,data_name):
    histo = go.Histogram(
        x=dataframe[data_name]     
    )
    data=[histo]
    layout = go.Layout(
    title='Sampled Results :' + data_name,
    xaxis=dict(
        title=data_name
    ),
    yaxis=dict(
        title='Count'
    ),
    barmode='overlay',
    bargap=0.25,
    bargroupgap=0.3
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='histogram/histogramIsBooking'+data_name+'Histogram.html')
    py.iplot(fig)


# In[13]:

def duoHistogram(dataFrameIsBooking,dataframe,data_name):
    histoBooking = go.Histogram(
        x=dataframe[data_name],
        opacity=0.75,
        name='Not Booking'        
    )
    histoAll = go.Histogram(
        x=dataFrameIsBooking[data_name],
        opacity=0.75,
        name='Booking',
        
    )
    data=[histoBooking,histoAll]
    layout = go.Layout(
    title='Random Sampled Results : ' + data_name,
    xaxis=dict(
        title=data_name
    ),
    yaxis=dict(
        title='Count'
    ),
    barmode='overlay',
    bargap=0.25,
    bargroupgap=0.3
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='../histogram/duoHistogram/'+data_name+'Histogram.html')
   # py.iplot(fig)


# In[52]:

def scatter(X,X_name,Y,Y_name,title):
    trace = go.Scatter(
        x=list(X),
        y=list(Y),
        mode = 'markers'
    )
    layout = go.Layout(
        title=title,
        xaxis=dict(
            title=X_name,
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title=Y_name,
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=[trace], layout=layout)
    py.iplot(fig)


# In[15]:

for name in train_NotBooking.columns:
    duoHistogram(train_IsBooking,train_NotBooking,name)

