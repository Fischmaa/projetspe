import csv
import pickle

def get_top5(count):
    freq={}
    c = 0
    for dest in count:
        hotel_count = count[dest]
        r_count={}
        for hotel,cc in hotel_count.items():
            r_count[cc]=hotel
        tmp=[r_count[i] for i in sorted(r_count.keys(),reverse=True)]
        tmp=tmp[:min(len(tmp),5)]
        freq[dest]=' '.join(tmp)
       
        if c%10000==0:
            print('sorting tables', c, len(count))
        c += 1
    return freq

name='../train.csv'
count={}
fo=open('pred_sub.csv','w')
fo.write('id,hotel_cluster\n')
fo.close()
for c,row in enumerate(csv.DictReader(open(name))):
    if True:
        xx=row['user_id']
        if xx not in count:
            count[xx]={}
        if row['hotel_cluster'] not in count[xx]:
            count[xx][row['hotel_cluster']]=0
        count[xx][row['hotel_cluster']]+=1
        if c%100000==0:
            print('building tables', c)
frequent=get_top5(count)

name='../test.csv'
for c,row in enumerate(csv.DictReader(open(name))):
    if True:
        fo=open('pred_sub_users.csv','a')
        if row['user_id'] not in frequent:
            tmp=''
        else:
            tmp=frequent[row['user_id']]
        fo.write('%d,%s\n'%(c,tmp))
        fo.close()
        
        if c%10000==0:
            print('printing results', c)
