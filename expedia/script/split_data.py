#! $HOME/anaconda3/bin/env
# -*-coding:utf-8-*

import pandas as pd
import time
import os

os.remove('first_data.csv')
os.remove('second_data.csv')
os.remove('third_data.csv')

start_time = time.time()
train = pd.read_csv('../train.csv', iterator = True, chunksize = 100000)
i = 1
with open('first_data.csv','a') as first_file:
	train.get_chunk().to_csv(first_file)
	i += 1
	while i<=100 : 
		train.get_chunk().to_csv(first_file, header = False)
		i += 1

print('--------fin 1 -----')
with open('second_data.csv', 'a') as second_file:
	train.get_chunk().to_csv(second_file)
	i += 1
	while i<=200:
		train.get_chunk().to_csv(second_file, header = False)
		i += 1
print('--------fin 2 -------')
with open('third_data.csv','a') as third_file:
	train.get_chunk().to_csv(third_file)
	i += 1
	for chunk in train : 
		chunk.to_csv(third_file, header = False)


print(time.time() - start_time)