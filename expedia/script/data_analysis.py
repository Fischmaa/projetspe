#! $HOME/anaconda3/bin/
# -*-coding:utf-8-*

import pandas as pd
import time 
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
train = pd.read_csv('train.csv', iterator = True, chunksize = 10000)
user = 0 
last_user = 0
count = 0
for chunk in train:
	tab = chunk['is_mobile']
	if last_user == 0 :
		last_user = tab[0]
	for j in range(len(tab)) : 
		user = tab[j]
		if last_user != user :
			last_user = user
			count += 1

print (count)
print("--- %s seconds ---" % (time.time() - start_time))