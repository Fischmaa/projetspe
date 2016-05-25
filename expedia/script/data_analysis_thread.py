#! $HOME/anaconda3/bin/env
# -*-coding:utf-8-*

import pandas as pd
import time 
import math as mt
from threading import Thread, RLock
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





verrou = RLock()

start_time = time.time()
train = pd.read_csv('../train.csv', iterator = True, chunksize = 100000)
count_user = 0 
count_distance = 0

class Analyse (Thread):

	def __init__(self, train):
		Thread.__init__(self)
		self.train = train

	def run(self):
		global count_distance
		global count_user
		for chunk in self.train:
			tab = chunk['orig_destination_distance']
			for j in range(len(tab)) : 
				if not isnan(tab[j]):
					with verrou:
						count_user += 1
						count_distance += tab[j]



print("--- %s seconds ---" % (time.time() - start_time))
