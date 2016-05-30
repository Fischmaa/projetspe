#!/usr/bin/python
# coding: utf-8
__author__ = 'michael kim'

import datetime
import math
from heapq import nlargest
from operator import itemgetter
import sys

#sys.argv note first argument is always python file

#make arguments path,numclasses.

#path to write to should be system argv

#assume first column of train has ground truth
def prepare_arrays_match():
    f = open(sys.argv[1]+'tmptrain.csv', "r")
    line = f.readline().strip()
    header = line.split(",")
    nbdict  = dict()
    total = 0

    # Calc counts
    while 1:
#    for zz in xrange(3290000):
        line = f.readline().strip()
        total += 1

        if total % 2000000 == 0:
            print('Read {} lines...'.format(total))

        if line == '':
            break


        arr = line.split(",")
        hotel_cluster = arr[0]
        arrlen = len(arr)
        featlist = []
        for jj in xrange(1,arrlen):
          featlist.append(header[jj]+'_'+arr[jj])


        for val in featlist:
          if hotel_cluster in nbdict:
            nbdict[hotel_cluster]['_total'] += 1
            if val in nbdict[hotel_cluster]:
              nbdict[hotel_cluster][val] += 1
            else:
              nbdict[hotel_cluster][val] = 1
          else:
            nbdict[hotel_cluster] = dict() 
            nbdict[hotel_cluster][val] = 1
            nbdict[hotel_cluster]['_total'] = 1

      
    f.close()
    return nbdict, total


def gen_submission(nbdict0, total0, nclasses):
    out = open(sys.argv[1]+'tmptestpred.csv', "w")
    f = open(sys.argv[1]+'tmptest.csv', "r")
    line = f.readline().strip()
    header = line.split(",")
    total = 0
#    out.write("id,hotel_cluster\n")
#    topclasters = nlargest(5, sorted(popular_hotel_cluster.items()), key=itemgetter(1))

    while 1:
        line = f.readline().strip()
        total += 1

        if total % 100000 == 0:
            print('Write {} lines...'.format(total))

        if line == '':
            break

        arr = line.split(",")
        #id = arr[0]#need to engin date features and best script features like interactions.
        #out.write(str(id) + ',')
        filled = []

        arrlen = len(arr)
        scoredict = dict()
        tmpS = [str(x) for x in range(int(nclasses))]          

        for kk in tmpS:
          scoredict[kk] = math.log(nbdict0[kk]['_total']/float(total0))
          for jj in xrange(arrlen):
            tmpfeat = header[jj]+'_'+arr[jj]
            if tmpfeat in nbdict0[kk]:
              numer = nbdict0[kk][tmpfeat]
            else:
              numer = 0
            scoredict[kk] += math.log((1.0+numer)/nbdict0[kk]['_total'])

         

#        topclasters = nlargest(5, sorted(scoredict.items()), key=itemgetter(1))
        tmpline = [str(scoredict[x]) for x in tmpS]
        out.write(','.join(tmpline)+"\n")

    out.close()


nbdict1, total1 = prepare_arrays_match()
gen_submission(nbdict1, total1, sys.argv[2])
