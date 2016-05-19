#! /usr/share/python3
# -*-coding:utf-8-*

import csv
import pandas as pa
from datetime import date
from collections import OrderedDict
from itertools import repeat
from sklearn.ensemble import RandomForestClassifier as rf
import random

random.seed(1)

tabtrain = pa.read_csv('sources/train.csv')
tabtest = pa.read_csv('sources/test.csv')

# On forme les tableaux des features
x_train = tabtrain.drop(['datetime','count','casual','registered'],1)
x_test = tabtest.drop(['datetime'],1)


# On forme les tableaux des résultats
y_train = tabtrain['count']


model = rf(1000)

model.fit(x_train, y_train)

y_test = model.predict(x_test)
y_test = pa.DataFrame(y_test)
y_test['datetime']=tabtest['datetime']
y_test.set_index('datetime')
print(y_test)
