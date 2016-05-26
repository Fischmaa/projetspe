#! $HOME/anaconda3/bin/
# -*-coding:utf-8-*

import pandas as pd
import numpy as np


train = pd.read_csv('../train.csv', iterator = True, chunksize = 1000)

min = 1000000000000
max = 0
number_bins= 10
tab_final = np.zeros(number_bins)
for chunk in train :
	max_local = chunk['orig_destination_distance'].max(axis = 0)
	min_local = chunk['orig_destination_distance'].min(axis = 0)
	if max < max_local : 
		max = max_local
	if min > min_local : 
		min = min_local
	

print(min)
print(max)
