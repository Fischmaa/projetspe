
# coding: utf-8

# # XGBoost Implémentation 
# 
# ## Import librairies

# In[1]:

import pandas as pd
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics   #Additional scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid search

import matplotlib.pylab as plt
#get_ipython().magic('matplotlib inline')
from matplotlib.pylab import rcParams
pd.options.mode.chained_assignment = None


from datetime import date
from datetime import datetime

def changePredcitors(train):

	createTripDuration(train)
	#createTripDurationType(train)
	createOrigDestinationType(train)
	createDateETC(train)
	createSeason(train)
	createTripAnticipation(train)
	#createTripAnticipationType(train)

#return time duration in days
def duration(ci,co):
	if(str(ci) != '-999.0' or str(co)!='-999.0'):
	    arrival = datetime.strptime(str(ci),'%Y-%m-%d')
	    departure = datetime.strptime(str(co),'%Y-%m-%d')
	    time = departure - arrival
	    return time.days 
	return -1


# In[ ]:
def createTripDuration(train):
	print("create trip_duration predictor")
	train['trip_duration']=0

	for i in range(len(train)) :

		train['trip_duration'][i]=duration(train['srch_ci'][i],train['srch_co'][i])

	print("done creating trip_duration_predicor")


# In[ ]:
def createTripDurationType(train):
	print("trip_duration_type")
	train['trip_duration_type']=0
	for i in range(len(train)) :
	    if(train['trip_duration'][i]==1):
	        train['trip_duration_type'][i]=1
	    elif(train['trip_duration'][i]==2):
	         train['trip_duration_type'][i]=2
	    elif(train['trip_duration'][i]>=3 and train['trip_duration'][i]<=6):
	         train['trip_duration_type'][i]=3
	    elif(train['trip_duration'][i]>=7):
	        train['trip_duration_type'][i]=4
        


# In[23]:
def createOrigDestinationType(train):
	print("orig_destination_distance_type")
	train['orig_destination_distance_type']=0

	for i in range(len(train)) :

		if(train['orig_destination_distance'][i]>=103 and train['orig_destination_distance'][i]<=229):
			train['orig_destination_distance_type'][i]=1
		elif(train['orig_destination_distance'][i]>=230 and train['orig_destination_distance'][i]<=428):
			train['orig_destination_distance_type'][i]=2
		elif(train['orig_destination_distance'][i]>=429 and train['orig_destination_distance'][i]<=822):
			train['orig_destination_distance_type'][i]=3
		elif(train['orig_destination_distance'][i]>=823 and train['orig_destination_distance'][i]<=1177):
			train['orig_destination_distance_type'][i]=4
		elif(train['orig_destination_distance'][i]>=1178 and train['orig_destination_distance'][i]<=1641):
			train['orig_destination_distance_type'][i]=5
		elif(train['orig_destination_distance'][i]>=1642 and train['orig_destination_distance'][i]<=2253):
			train['orig_destination_distance_type'][i]=6
		elif(train['orig_destination_distance'][i]>=2254 and train['orig_destination_distance'][i]<=3609):
			train['orig_destination_distance_type'][i]=7
		elif(train['orig_destination_distance'][i]>=3610 and train['orig_destination_distance'][i]<=5439):
			train['orig_destination_distance_type'][i]=8
		elif(train['orig_destination_distance'][i]>=5440):
			train['orig_destination_distance_type'][i]=9
		else:
			continue


   


# In[24]:
def createDateETC(train):
	print("date")
	train['date']=0

	for i in range(len(train)) :
	    train['date'][i]=datetime.strptime(train['date_time'][i],'%Y-%m-%d %H:%M:%S')
	    
	# print("dayOfWeek")
	# train['dayOfWeek']=0

	# for i in range(len(train)):
	#     train['dayOfWeek'][i]=train['date'][i].isoweekday()

	print("year")
	train['year']=0

	for i in range(len(train)):
	    train['year'][i]=train['date'][i].year

	print("month")    
	train['month']=0

	for i in range(len(train)):
	    train['month'][i]=train['date'][i].month
	print("day") 
	train['day']=0

	# for i in range(len(train)):
	#     train['day'][i]=train['date'][i].day


# In[25]:

#check in
# train['date_ci']=0

# for i in range(len(train)) :
#     train['date_ci'][i]=datetime.strptime(train['srch_ci'][i],'%Y-%m-%d')
    
# train['dayOfWeek_ci']=0

# for i in range(len(train)):
#     train['dayOfWeek_ci'][i]=train['date_ci'][i].isoweekday()

#     train['year_ci']=0

# for i in range(len(train)):
#     train['year_ci'][i]=train['date_ci'][i].year
    
# train['month_ci']=0

# for i in range(len(train)):
#     train['month_ci'][i]=train['date_ci'][i].month
    
# train['day_ci']=0

# for i in range(len(train)):
#     train['day_ci'][i]=train['date_ci'][i].day
#check out 
# train['date_co']=0

# for i in range(len(train)) :
#     train['date_co'][i]=datetime.strptime(train['srch_co'][i],'%Y-%m-%d')
    
# train['dayOfWeek_co']=0

# for i in range(len(train)):
#     train['dayOfWeek_co'][i]=train['date_co'][i].isoweekday()

#     train['year_co']=0

# for i in range(len(train)):
#     train['year_co'][i]=train['date_co'][i].year
    
# train['month_co']=0

# for i in range(len(train)):
#     train['month_co'][i]=train['date_co'][i].month
    
# train['day_co']=0

# for i in range(len(train)):
#     train['day_co'][i]=train['date_co'][i].day


# In[26]:
def createSeason(train):
	print("season")
	train['season']=0

	for i in range(len(train)):

	    if(train['month'][i]>=4 and train['month'][i]<=6):
	        train['season'][i]=1
	    elif(train['month'][i]>=7 and train['month'][i]<=9):
	        train['season'][i]=2
	    elif(train['month'][i]>=10 and train['month'][i]<=12):
	        train['season'][i]=3


# In[27]:


#return time duration in days
def anticipation(date,co):
	if(str(co)!='-999.0'):
	    arrival = date.date()
	    departure = datetime.strptime(str(co),'%Y-%m-%d')
	    departure = departure.date()
	    time = departure - arrival
	    return time.days 
	return -1


# In[28]:
def createTripAnticipation(train):
	print("trip_anticipation")
	train['trip_anticipation']=0


	for i in range(len(train)) :
	    train['trip_anticipation'][i]=anticipation(train['date'][i],train['srch_ci'][i])

def createTripAnticipationType(train):
# In[29]:
	print("trip_anticipation_type")
	train['trip_anticipation_type']=0
	for i in range(len(train)) :

	    if(train['trip_anticipation'][i]>=2 and train['trip_anticipation'][i]<7):
	         train['trip_anticipation_type'][i]=1
	    elif(train['trip_anticipation'][i]>=7 and train['trip_anticipation'][i]<13):
	         train['trip_anticipation_type'][i]=2
	    elif(train['trip_anticipation'][i]>=13 and train['trip_anticipation'][i]<20):
	         train['trip_anticipation_type'][i]=3
	    elif(train['trip_anticipation'][i]>=20 and train['trip_anticipation'][i]<31):
	         train['trip_anticipation_type'][i]=4
	    elif(train['trip_anticipation'][i]>=31 and train['trip_anticipation'][i]<43):
	         train['trip_anticipation_type'][i]=5
	    elif(train['trip_anticipation'][i]>=43 and train['trip_anticipation'][i]<62):
	         train['trip_anticipation_type'][i]=6
	    elif(train['trip_anticipation'][i]>=62 and train['trip_anticipation'][i]<=89):
	         train['trip_anticipation_type'][i]=7
	    elif(train['trip_anticipation'][i]>=89 and train['trip_anticipation'][i]<141):
	         train['trip_anticipation_type'][i]=8
	    elif(train['trip_anticipation'][i]>=141):
	         train['trip_anticipation_type'][i]=9



# ## Reading data

# In[147]:

tab_train = pd.read_csv('../train.csv',iterator = True, chunksize = 100000)
train = tab_train.get_chunk()
train.fillna(-999.0,inplace=True)
changePredcitors(train)
print('creation premier tableau...')
count=0
for chunk in tab_train :
    count += 1
    print(count * 100 /38 )
    #change predictors
    train_part=chunk
    train_part.fillna(-999.0,inplace=True)
    changePredcitors(train_part)
    train = train.append(train_part,ignore_index=True)
print('fin premier tableau')

# ## Define target and columns to drop

# In[158]:



target = 'hotel_cluster'
IDcol = ['date_time','srch_ci','srch_co','date','date_ci','date_co']


# ## Create XGBoost model and perform cross-validation

# In[145]:

def modelfit(alg, dtrain, predictors,useTrainCV=True, cv_folds=5,early_stopping_rounds=50,missing=-999.0):
    
    if useTrainCV:
        xgb_param = alg.get_xgb_params()
        xgtrain = xgb.DMatrix(dtrain[predictors].values, label=dtrain[target].values,missing=missing)
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds)
        alg.set_params(n_estimators=cvresult.shape[0])
    
    #Fit the algorithm on the data
    alg.fit(dtrain[predictors], dtrain['hotel_cluster'],eval_metric='merror')
        
    #Predict training set:
    dtrain_predictions = alg.predict(dtrain[predictors])
    dtrain_predprob = alg.predict_proba(dtrain[predictors])
        
    #Print model report:
    print ("\nModel Report")
    print ("Accuracy : %.4g" % metrics.accuracy_score(dtrain['hotel_cluster'].values, dtrain_predictions))
    #print ("AUC Score (Train): %f" % metrics.roc_auc_score(dtrain['hotel_cluster'], dtrain_predprob))
                    
    feat_imp = pd.Series(alg.booster().get_fscore()).sort_values(ascending=False)
    feat_imp.plot(kind='bar', title='Feature Importances')
    plt.ylabel('Feature Importance Score')
    plt.savefig('../XGBoost/Features/FeaturesImportanceScore.png')
    
    return alg


# In[146]:
print("start training")
#Choose all predictors except target & IDcols
predictors = [x for x in train.columns if (x not in target and x not in IDcol)]

xgb1 = XGBClassifier(
 learning_rate =0.1,
 n_estimators=1000,
 max_depth=5,
 min_child_weight=1,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= "multi:softprob",
 #nthread=4,
 scale_pos_weight=1,
 seed=27
)

model = modelfit(xgb1, train, predictors,useTrainCV=False)


# ## Delete train and read test

# In[ ]:
print("delete train data frame")
#Delete data frame
cols = train.columns
del train


# In[131]:

#read test
tab_test = pd.read_csv('../test.csv',iterator = True, chunksize = 100000)
test = tab_test.get_chunk()
test.fillna(-999.0,inplace=True)
changePredcitors(test)
count=1
print('read test ...')
for chunk in tab_test :
    count += 1
    print(count * 100 /38 )
    test_part=chunk
    test_part.fillna(-999.0,inplace=True)
    changePredcitors(test_part)
    test = test.append(test_part,ignore_index=True)
print('done reading test ... ')
test.insert(19,"is_booking",1)
test.insert(20,"cnt",1)



# ## Change predictors


# ## Define target and columns to drop

# In[141]:

target = 'hotel_cluster'
IDcol = ['id','date_time','srch_ci','srch_co','date','date_ci','date_co']


# In[142]:
print("prediction")
predictors=[x for x in test.columns if (x not in target and x not in IDcol)]

predict=model.predict_proba(test[predictors])
predict = np.argsort(predict[::-1][:,:5])


# In[143]:

def concatStr(X):
    return str(X[0])+' '+str(X[1])+' '+str(X[2])+' '+str(X[3])+' '+str(X[4])


# In[144]:
print("submission")
submission = test[['id']].drop(['id'],1)
submission['hotel_cluster']='blank'
for i in range(len(submission)):
    submission['hotel_cluster'][i]=concatStr(predict[i])
submission.head()


# In[378]:
print("write submission")
#write submission 
submission.to_csv('../XGBoost/Submission/submissionXGBOOST.csv',header=True, index_label='id')

