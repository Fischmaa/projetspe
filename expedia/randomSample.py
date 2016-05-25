import pandas as pd
import numpy as np 
import time
print("get chunk from train.csv")
#get data
part=pd.read_csv('train.csv',iterator=True,chunksize=1000000)
print("convert all chunks into DataFrame")
#get first chunk to initialize train DataFrame
tic=time.time()
train = part.get_chunk()
for chunk in part:
	print("new chunk read")
	train=train.append(chunk,ignore_index=True)
toc=time.time()
print("time to parse all file = ", toc - tic)

print("extract random sample from data frame")
trainSample = train.sample(100000)
print("write random sample to trainSample.csv")
trainSample.to_csv('trainRandomSample.csv') 