#! $HOME/anaconda3/lib/python3.5
# -*-coding:utf-8-*

import pandas as pa
from sklearn.ensemble import RandomForestClassifier as rf
import matplotlib.pyplot as plt
from datetime import datetime
pa.options.mode.chained_assignment = None  # default='warn'

tabtrain = pa.read_csv('sources/train.csv')
tabtest = pa.read_csv('sources/test.csv')

# On ajoute une colonne contenant le date au format Datetime
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


# Création de la colonne contenant l'heure de la journée
tabtrain['hour']=0
for i in range(len(tabtrain)) :
	tabtrain['hour'][i] = tabtrain['date'][i].hour

tabtrain['hour']=tabtrain['hour'].astype('category')

tabtest['hour']=0
for i in range(len(tabtest)) :
	tabtest['hour'][i] = tabtest['date'][i].hour

tabtest['hour']=tabtest['hour'].astype('category')

# Tableaux d'entrainement
y_train = tabtrain['count']
x_train = tabtrain.drop(['datetime','count','casual','registered','date'],1)

# On forme les tableaux des résultats
x_test = tabtest.drop(['datetime','date'],1)

model = rf(200)

model.fit(x_train, y_train)

y_test = model.predict(x_test)
y_test = pa.DataFrame(y_test)
y_test.index = tabtest['datetime']

y_test.to_csv('csv/rf_matthias_1.csv')

