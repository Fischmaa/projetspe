#! $HOME/anaconda3/bin/
# -*-coding:utf-8-*

import pandas as pd

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

train = pd.read_csv('out_train.csv')
train = train['user_id']
for i in range(1,len(train)) :
	if train[i] < train[i-1]:
		print("not ordered")
		print(i)
		break

print("ordered")