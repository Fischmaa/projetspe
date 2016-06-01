
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
import os

# In[4]:

# Lecture du csv avec Pandas

train = pd.read_csv('../train.csv',iterator = True, chunksize = 1000000)
tab_train = train.get_chunk()
print('creation premier tableau...')
for chunk in train :
	tab_train = pd.concat([tab_train, chunk])
print('fin premier tableau')

# On prépare les données pour l'algorithme
print ('début pretraitement...')
X_train = tab_train.drop(['hotel_cluster','date_time','srch_ci','srch_co',],1).as_matrix()
Y_train = tab_train['hotel_cluster'].as_matrix()
print ('fin pretraitement')
print('suppresion premier tableau')
del tab_train
#creation du modèle avec fitting
print('début modèle...')
gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.05)
gbm.fit(X_train,Y_train)
print('fin modèle...')
del X_train
del Y_train
#sauvegarde modèle
print('sauvegarde du modèle...')
if not os.path.isdir('modeles'):
	os.mkdir('modeles')
gbm.booster().save_model('modeles/premier.model')
print('fin sauvegarde...')

#sauvegarde feature
print('sauvegarde feature...')
if not os.path.isdir('features'):
	os.mkdir('features')
feature = pd.Series(gbm.booster().get_fscore()).sort_values(ascending = False)
feature.to_csv('features/premier_feature.csv')
print('fin sauvegarde...')



#on utilise le tableau test
test = pd.read_csv('../test.csv' , iterator = True, chunksize = 1000000)
tab_test = test.get_chunk()
print('creation second tableau...')
for chunk in test :
	tab_test = pd.concat([tab_test, chunk])
print('fin second tableau...')

X_test = tab_test.drop(['date_time','srch_ci','srch_co'],1).as_matrix()

#prédiction pour le test
print('début prédiction...')
Y_test = gbm.predict(X_test)
print('fin prédiction...')

#on recupère le résultat
result = tab_test[['id']]
result = result.drop(['id'],1)
result["hotel_cluster"]=pd.DataFrame(Y_test)

print('début exportation...')
if not os.path.isdir('resultat'):
	os.mkdir('resultat')

result.to_csv('resultat/out_xgboost.csv')
