#!/usr/bin/python3.3
# -*-coding:Utf-8 -*

import pandas as pd 
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt 
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'
# reading data
train = pd.read_csv("data/train.csv")
test = pd.read_csv("data/test.csv")

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
print(byday.describe())
print('Sunday seems to be an important predictor')

#create Sunday variable and convert to category 
train_factor['Sunday'] = 0 ;
train_factor.ix[train_factor['day']==6,'Sunday']=1

train_factor['Sunday']=train_factor['Sunday'].astype('category')

test_factor['Sunday'] = 0 ;
test_factor.ix[test_factor['day']==6,'Sunday']=1

test_factor['Sunday']=test_factor['Sunday'].astype('category')

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
formula = "count ~ season + weather + temp +  windspeed + humidity + daypart + hour + Sunday"

train_factor_weekday=train_factor[(train_factor['day']!=5)]
train_factor_weekday=train_factor_weekday[(train_factor_weekday['day']!=6)]
regression_weekday=smf.glm(formula,data=train_factor_weekday,family=sm.families.Poisson(link=sm.families.links.log))
regression_weekday=regression_weekday.fit()
print(regression_weekday.summary2())

train_factor_weekend=train_factor[(train_factor['day']!=0)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=1)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=2)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=3)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=4)]
regression_weekend=smf.glm(formula,data=train_factor_weekend,family=sm.families.Poisson(link=sm.families.links.log))
regression_weekend=regression_weekend.fit()
print(regression_weekend.summary2())

#prediction 
prediction_weekday=regression_weekday.predict(test_factor_weekday)
prediction_weekday[prediction_weekday<0]=0 # bike demand is positive

prediction_weekend=regression_weekend.predict(test_factor_weekend)
prediction_weekend[prediction_weekend<0]=0 # bike demand is positive



#convert to dataframe
prediction=pd.DataFrame(prediction_weekday)
prediction.columns=['weekday']
prediction['weekend']=pd.DataFrame(prediction_weekend)
prediction["datetime"]=test_factor.index.values
prediction = prediction.set_index("datetime")

prediction['count']=round(prediction['count'])
print(prediction)

#write the submission
prediction.to_csv("regressionSubmission.csv")

