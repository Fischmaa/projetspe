#! /usr/share/python3
# -*-coding:utf-8-*

import csv
import pandas as pa
from datetime import date
from collections import OrderedDict
from itertools import repeat


#look if we have to set the random seed
f = open('train.csv', 'r')	
fi = open('test.csv', 'r')	


tabtrain = pa.read_csv('train.csv')
tabtest = pa.read_csv('test.csv')

#add a row name count
tabtest['count'] = 0

#create a tab for the result
submission = tabtest.loc[:,["datetime","count"]]

#create a day tab with date unique
daytab = tabtest["datetime"]
#keep the date and remove hour
for line in range(len(daytab)):
	s = daytab[line]
	s1 = s.split()[0]
	daytab[line] = s1 

#daytab without dupiclate values
daytab = daytab.drop_duplicates().reset_index()["datetime"]

testloc = tabtest


