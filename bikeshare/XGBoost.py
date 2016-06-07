
# coding: utf-8

# In[1]:

#!/usr/bin/python3.3



import pandas as pd 
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt 
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'
import xgboost as xgb
# reading data
train = pd.read_csv("sources/train.csv")
test = pd.read_csv("sources/test.csv")


# In[2]:

'''
#add a new column 'date' convert into datetime for both training and test set
train['date']=0
for i in range(len(train)) :
	train['date'][i]=datetime.strptime(train['datetime'][i],'%Y-%m-%d %H:%M:%S')

train=train.set_index("datetime")


test['date']=0
for i in range(len(test)) :
	test['date'][i]=datetime.strptime(test['datetime'][i],'%Y-%m-%d %H:%M:%S')

test=test.set_index("datetime")
'''


# In[3]:

'''
#categorize training set
train = train
train['weather'] = train['weather'].astype('category')
train['holiday'] = train['holiday'].astype('category')
train['workingday'] = train['workingday'].astype('category')
train['season'] = train['season'].astype('category')

#factorize test set
test = test
test['weather'] = test['weather'].astype('category')
test['holiday'] = test['holiday'].astype('category')
test['workingday'] = test['workingday'].astype('category')
test['season'] = test['season'].astype('category')
'''


# In[4]:

'''
#create day of week column and hour column and a year colum then convert into category for both training and test set
train['day']=0
train['hour']=0
train['year']=0
for i in range(len(train)) :
    train['day'][i] = train['date'][i].weekday()
    train['hour'][i] = train['date'][i].hour
    train['year'][i]=train['date'][i].year

test['day']=0
test['hour']=0
test['year']=0
for i in range(len(test)) :
    test['day'][i] = test['date'][i].weekday()
    test['hour'][i] = test['date'][i].hour
    test['year'][i]=test['date'][i].year
'''


# In[5]:

'''
#create ahot () variable and convert to category (4 category) for both training and test set
train['ahot'] = 4
for i in range(len(train)) :
	currentTemp = train['atemp'][i]
	if (currentTemp>=24.24 and currentTemp<31.06 ):
		train['ahot'][i] = 3
	elif (currentTemp>=16.6 and currentTemp<24.24):
		train['ahot'][i] = 2
	elif ( currentTemp<16.6) :
		train['ahot'][i] = 1


test['ahot'] = 4
for i in range(len(test)) :
	currentTemp = test['atemp'][i]
	if (currentTemp>=24.24 and currentTemp<31.06 ):
		test['ahot'][i] = 3
	elif (currentTemp>=16.6 and currentTemp<24.24):
		test['ahot'][i] = 2
	elif (currentTemp<16.6) :
		test['ahot'][i] = 1
'''


# In[6]:

'''
#create ahot () variable and convert to category (4 category) for both training and test set
train['hot'] = 4
for i in range(len(train)) :
	currentTemp = train['temp'][i]
	if (currentTemp>=20.5 and currentTemp<26.24 ):
		train['hot'][i] = 3
	elif (currentTemp>=13.94 and currentTemp<20.5):
		train['hot'][i] = 2
	elif ( currentTemp<13.94) :
		train['hot'][i] = 1


test['hot'] = 4
for i in range(len(test)) :
	currentTemp = test['temp'][i]
	if (currentTemp>=20.5 and currentTemp<26.24 ):
		test['hot'][i] = 3
	elif (currentTemp>=13.94 and currentTemp<20.5):
		test['hot'][i] = 2
	elif (currentTemp<13.94) :
		test['hot'][i] = 1
'''


# In[7]:

'''
train = train.reset_index()
train = train.drop("datetime",1)
train = train.drop(['date','registered','casual'],1)

test = test.reset_index()
result = test[['datetime']]
test = test.drop("datetime",1)
test = test.drop('date',1)
'''


# In[ ]:




# In[3]:

train.dtypes
train.


# In[2]:

X_train = train.drop("count",1)
Y_train = train['count']
T_train_xgb = xgb.DMatrix(X_train, Y_train)
params = {"objective": "reg:linear",'bst:max_depth':13,"booster":"gbtree" }
gbm = xgb.train(dtrain=T_train_xgb, params = params)
X_test = xgb.DMatrix(test)
Y_pred = gbm.predict(X_test)
print(Y_pred)
xgb.plot_importance(gbm)


# In[ ]:

plt.show()


# In[35]:

result['count'] = pd.DataFrame(Y_pred)
#result[result['count']<=0] = 0

result_final = result.set_index('datetime')
result_final[result_final['count']<=0]=0
result_final


# In[36]:

result_final.to_csv('Résultats/XGBoost/submissionXGBoost.csv')

