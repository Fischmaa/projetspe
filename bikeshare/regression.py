#!/usr/bin/python3.3
# -*-coding:Utf-8 -*

import csv
from sklearn import linear_model

# On lit les données
with open('data/train.csv', 'r') as file:
        training = csv.reader(file)


