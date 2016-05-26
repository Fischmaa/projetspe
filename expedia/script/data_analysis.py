#! $HOME/anaconda3/bin/env
# -*-coding:utf-8-*

import pandas as pd
import time 
import math as mt
#move the 10000 first value from file to out_file

#train = pd.read_csv('train.csv', iterator = True, chunksize = 10000)
#test = pd.read_csv('test.csv', iterator = True, chunksize = 10000)
#dest = pd.read_csv('destinations.csv', iterator = True, chunksize = 10000)

#tabtrain = train.get_chunk()
#tabtest = test.get_chunk()
#tabdest = dest.get_chunk()

#tabtrain.to_csv('out_train.csv')
#tabtest.to_csv('out_test.csv')
#tabdest.to_csv('out_dest.csv')


start_time = time.time()
train = pd.read_csv('../train.csv', iterator = True, chunksize = 100000, usecols = ['orig_destination_distance'])
count_user = 0 
count_distance = 0
for chunk in train:
	#tab = chunk['user_id']
	tab2 = chunk['orig_destination_distance']
	#if last_user == 0 :
	#	last_user = tab[0]
	for j in range(len(tab2)) : 
		if not mt.isnan(tab2[j]):		
			count_user += 1
			count_distance += tab2[j]	
	#	user = tab[j]
	#	if last_user != user :
	#		last_user = user
	#		count += 1

print (count_user/count_distance)
print("--- %s seconds ---" % (time.time() - start_time))
