
# coding: utf-8

# ## Premiers tests de xgBoost avec Python.
# On n'utilise pas ici Pypy, et on prend uniquement les 10 000 premières valeurs d'entraînement.
# 
# **Références :** [Exemple de code](https://www.kaggle.com/datacanary/titanic/xgboost-example-python/code) utilisant Pandas pour lire les données et xgBoost pour faire les prédictions. 
# 
# **Remarque :** On peut utiliser pickle pour sauvegarder les données en binaire et les chargé plus rapidement.
# 
# ```python
# pickle.dump(train,open('train.bin','wb')protocol=4)
# pickle.load(open('train.bin','rb'))
# ```

# In[3]:

# Importation des bibliothèques

import xgboost as xgb
import pandas as pd
import numpy as np


# In[4]:

# Lecture du csv avec Pandas

train = pd.read_csv('../train.csv',iterator = True, chunksize = 1000000)
test = pd.read_csv('../test.csv' , iterator = True, chunksize = 1000000)

tab_train = train.get_chunk()
tab_test = test_train.get_chunk()
for chunk in train :
	tab_train = tab_train.concat(chunk)

for chunk in test :
	tab_test = tab_test.concat(chunk)

print (len(tab_train))
print(len(tab_test))
# In[8]:

# On prépare les données pour l'algorithme

#X_train = train.drop(['hotel_cluster','date_time','srch_ci','srch_co',],1).as_matrix()
#Y_train = train['hotel_cluster'].as_matrix()

#X_test = test.drop(['date_time','srch_ci','srch_co'],1).as_matrix()
#result = test[['id']]
#type(result)


# In[ ]:

#gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)

#gbm.fit(X_train,Y_train)

#Y_test = gbm.predict(X_test)


# In[ ]:

#result["hotel_cluster"]=pd.DataFrame(Y_test)
#result


# In[112]:

#get_ipython().magic('matplotlib inline')

#counts = train['hotel_cluster'].value_counts()
#counts

