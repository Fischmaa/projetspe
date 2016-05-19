#! $HOME/anaconda3/lib/python3.5
# -*-coding:utf-8-*

import pandas as pa
from sklearn.ensemble import RandomForestClassifier as rf
import matplotlib.pyplot as plt
from datetime import datetime
pa.options.mode.chained_assignment = None  # default='warn'

tabtrain = pa.read_csv('sources/train.csv')
tabtest = pa.read_csv('sources/test.csv')

tabtrain['date']=0
for i in range(len(tabtrain)) :
	tabtrain['date'][i]=datetime.strptime(tabtrain['datetime'][i],'%Y-%m-%d %H:%M:%S')



tabtest['date']=0
for i in range(len(tabtest)) :
	tabtest['date'][i]=datetime.strptime(tabtest['datetime'][i],'%Y-%m-%d %H:%M:%S')

# On passe les variables en discret
tabtrain['season'] = tabtrain['season'].astype('category')
tabtrain['holiday'] = tabtrain['holiday'].astype('category')
tabtrain['workingday'] = tabtrain['workingday'].astype('category')
tabtrain['weather'] = tabtrain['weather'].astype('category')

tabtest['season'] = tabtest['season'].astype('category')
tabtest['holiday'] = tabtest['holiday'].astype('category')
tabtest['workingday'] = tabtest['workingday'].astype('category')
tabtest['weather'] = tabtest['weather'].astype('category')


#create day of week column and hour column then convert into category for both training and test set
tabtrain['day']=0
tabtrain['hour']=0
for i in range(len(tabtrain)) :
	tabtrain['day'][i] = tabtrain['date'][i].weekday()
	tabtrain['hour'][i] = tabtrain['date'][i].hour

tabtrain['day']=tabtrain['day'].astype('category')
tabtrain['hour']=tabtrain['hour'].astype('category')

tabtest['day']=0
tabtest['hour']=0
for i in range(len(tabtest)) :
	tabtest['day'][i] = tabtest['date'][i].weekday()
	tabtest['hour'][i] = tabtest['date'][i].hour

tabtest['day']=tabtest['day'].astype('category')
tabtest['hour']=tabtest['hour'].astype('category')

# Tableaux d'entrainement
y_train = tabtrain['count']
x_train = tabtrain.drop(['datetime','count','casual','registered','date','day'],1)

# On forme les tableaux des résultats
x_test = tabtest.drop(['datetime','date','day'],1)

model = rf(30)

model.fit(x_train, y_train)

y_test = model.predict(x_test)
y_test = pa.DataFrame(y_test)
y_test.index = tabtest['datetime']

y_test.to_csv('csv/rf_matthias_1.csv')

