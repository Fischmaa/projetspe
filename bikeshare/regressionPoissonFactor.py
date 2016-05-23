#!/usr/bin/python3.3
# -*-coding:Utf-8 -*


import pandas as pd 
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt 
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'
# reading data
train = pd.read_csv("sources/train.csv")
test = pd.read_csv("sources/test.csv")

#add a new column 'date' convert into datetime for both training and test set
train['date']=0
for i in range(len(train)) :
	train['date'][i]=datetime.strptime(train['datetime'][i],'%Y-%m-%d %H:%M:%S')

train=train.set_index("datetime")


test['date']=0
for i in range(len(test)) :
	test['date'][i]=datetime.strptime(test['datetime'][i],'%Y-%m-%d %H:%M:%S')

test=test.set_index("datetime")

#categorize training set
train_factor = train
train_factor['weather'] = train_factor['weather'].astype('category')
train_factor['holiday'] = train_factor['holiday'].astype('category')
train_factor['workingday'] = train_factor['workingday'].astype('category')
train_factor['season'] = train_factor['season'].astype('category')

#factorize test set
test_factor = test
test_factor['weather'] = test_factor['weather'].astype('category')
test_factor['holiday'] = test_factor['holiday'].astype('category')
test_factor['workingday'] = test_factor['workingday'].astype('category')
test_factor['season'] = test_factor['season'].astype('category')

#create day of week column and hour column then convert into category for both training and test set
train_factor['day']=0
train_factor['hour']=0
for i in range(len(train_factor)) :
	train_factor['day'][i] = train_factor['date'][i].weekday()
	train_factor['hour'][i] = train_factor['date'][i].hour

train_factor['day']=train_factor['day'].astype('category')
train_factor['hour']=train_factor['hour'].astype('category')

test_factor['day']=0
test_factor['hour']=0
for i in range(len(test_factor)) :
	test_factor['day'][i] = test_factor['date'][i].weekday()
	test_factor['hour'][i] = test_factor['date'][i].hour

test_factor['day']=test_factor['day'].astype('category')
test_factor['hour']=test_factor['hour'].astype('category')

#is a day more significant ?
byday=train_factor.groupby('day')
#print(byday.describe())

#create Sunday variable and convert to category 
train_factor['Sunday'] = 0 ;
train_factor.ix[train_factor['day']==6,'Sunday']=1

train_factor['Sunday']=train_factor['Sunday'].astype('category')

test_factor['Sunday'] = 0 ;
test_factor.ix[test_factor['day']==6,'Sunday']=1

test_factor['Sunday']=test_factor['Sunday'].astype('category')

#create Hot variable and convert to category (4 category) for both training and test set
train_factor['hot'] = 0
for i in range(len(train_factor)) :
	currentTemp = train_factor['atemp'][i]
	if (currentTemp>=16.6 and currentTemp<24.24 ):
		train_factor['hot'][i] = 1
	elif (currentTemp>=24.24 and currentTemp<31.06):
		train_factor['hot'][i] = 2
	elif (currentTemp>=31.06) :
		train_factor['hot'][i] = 3

train_factor['hot']=train_factor['hot'].astype('category')

test_factor['hot'] = 0
for i in range(len(test_factor)) :
	currentTemp = test_factor['atemp'][i]
	if (currentTemp>=16.6 and currentTemp<24.24 ):
		test_factor['hot'][i] = 1
	elif (currentTemp>=24.24 and currentTemp<31.06):
		test_factor['hot'][i] = 2
	elif (currentTemp>=31.06) :
		test_factor['hot'][i] = 3

test_factor['hot']=test_factor['hot'].astype('category')

#create Hour variable and convert to category (4 category) for both training and test set
train_factor['daypart'] = 0
for i in range(len(train_factor)) :
	currentHour = train_factor['hour'][i]
	if (currentHour>=16 and currentHour<21 ):
		train_factor['daypart'][i] = 3
	elif (currentHour>=11 and currentHour<16):
		train_factor['daypart'][i] = 2
	elif (currentHour>=4 and currentHour<11) :
		train_factor['daypart'][i] = 1

train_factor['daypart']=train_factor['daypart'].astype('category')

test_factor['daypart'] = 0
for i in range(len(test_factor)) :
	currentHour = test_factor['hour'][i]
	if (currentHour>=16 and currentHour<21 ):
		test_factor['daypart'][i] = 3
	elif (currentHour>=11 and currentHour<16):
		test_factor['daypart'][i] = 2
	elif (currentHour>=4 and currentHour<11) :
		test_factor['daypart'][i] = 1

test_factor['daypart']=test_factor['daypart'].astype('category')
#linear regression
formula = "count ~ season + weather + humidity + hour + holiday + atemp + hot + daypart "

train_factor_weekday=train_factor[(train_factor['day']!=5)]
train_factor_weekday=train_factor_weekday[(train_factor_weekday['day']!=6)]
regression_weekday=smf.glm(formula,data=train_factor_weekday,family=sm.families.Poisson(link=sm.families.links.log))
regression_weekday=regression_weekday.fit()

test_factor_weekday=test_factor[(test_factor['day']!=5)]
test_factor_weekday=test_factor_weekday[(test_factor_weekday['day']!=6)]

formula = "count ~ season + weather + humidity  + hour + Sunday + atemp + hot "
train_factor_weekend=train_factor[(train_factor['day']!=0)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=1)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=2)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=3)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=4)]
regression_weekend=smf.glm(formula,data=train_factor_weekend,family=sm.families.Poisson(link=sm.families.links.log))
regression_weekend=regression_weekend.fit()

test_factor_weekend=test_factor[(test_factor['day']!=0)]
test_factor_weekend=test_factor_weekend[(test_factor_weekend['day']!=1)]
test_factor_weekend=test_factor_weekend[(test_factor_weekend['day']!=2)]
test_factor_weekend=test_factor_weekend[(test_factor_weekend['day']!=3)]
test_factor_weekend=test_factor_weekend[(test_factor_weekend['day']!=4)]

#prediction 
prediction_weekday=regression_weekday.predict(test_factor_weekday)
prediction_weekday[prediction_weekday<0]=0 # bike demand is positive

prediction_weekend=regression_weekend.predict(test_factor_weekend)
prediction_weekend[prediction_weekend<0]=0 # bike demand is positive


#convert to dataframe
prediction_weekend=pd.DataFrame(prediction_weekend)
prediction_weekend.columns=['count']
prediction_weekend["datetime"]=test_factor_weekend.index.values
prediction_weekend = prediction_weekend.set_index("datetime")

prediction_weekday=pd.DataFrame(prediction_weekday)
prediction_weekday.columns=['count']
prediction_weekday["datetime"]=test_factor_weekday.index.values
prediction_weekday = prediction_weekday.set_index("datetime")

prediction=prediction_weekend;
prediction=prediction.append(prediction_weekday)
prediction.sort_index()

#write the submission
prediction.to_csv("Résultats/regressionPoissonFactor.csv")

