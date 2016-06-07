import csv
import pickle
from datetime import datetime

def get_top5(hotel_count):
    r_count={}
    for hotel,cc in hotel_count.items():
        r_count[cc]=hotel
    tmp=[r_count[i] for i in sorted(r_count.keys(),reverse=True)]
    tmp=tmp[:min(len(tmp),5)]
    return ' '.join(tmp)

def duration(ci,co):
	try:
		arrival = datetime.strptime(ci,'%Y-%m-%d')
		departure = datetime.strptime(co,'%Y-%m-%d')
		time = departure - arrival
		return time.days 
	except:
		return 0

name='../train.csv'
count={}
fo=open('pred_sub.csv','w')
fo.write('id,hotel_cluster\n')
fo.close()

for c,row in enumerate(csv.DictReader(open(name))):

    if True:
        xx=row['srch_destination_id']
        if xx not in count:
            count[xx]={}
            count[xx][0]={}
            count[xx][1]={}
        if row['hotel_cluster'] not in count[xx][0]:
        	count[xx][0][row['hotel_cluster']] = 0
        if row['hotel_cluster'] not in count[xx][1]:
        	count[xx][1][row['hotel_cluster']] = 0
            
        trip_duration = duration(row['srch_ci'],row['srch_co'])
        
        if(trip_duration > 1):
        	count[xx][0][row['hotel_cluster']]+=1
        else:
        	count[xx][1][row['hotel_cluster']]+=1
        	
        
        if c%100000==0:
            print(c)
            print(len(count))

            
frequent={}
for dest in count:
	frequent[dest] = {}
	frequent[dest][0]=get_top5(count[dest][0])
	frequent[dest][1]=get_top5(count[dest][1])


name='../test.csv'
for c,row in enumerate(csv.DictReader(open(name))):
	if True:
		fo=open('pred_sub_trip_duration.csv','a')
		if row['srch_destination_id'] not in frequent:
			tmp=''
		else:
			if(duration(row['srch_ci'],row['srch_co']) > 1):
				tmp=frequent[row['srch_destination_id']][0]
			else:
				tmp=frequent[row['srch_destination_id']][1]
		fo.write('%d,%s\n'%(c,tmp))
		fo.close()
		
		if c%100000==0:
			print(c)
			print(len(count))
