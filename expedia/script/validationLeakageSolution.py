# coding: utf-8
#################################
#      Simple Validation        #
#################################
# contributors:
# ZFTurbo - idea, main part
# Kagglers - tuning, development
# Grzegorz Sionkowski - simple validation



import datetime
from heapq import nlargest
from operator import itemgetter
from collections import defaultdict
from datetime import datetime
import gzip
# validation ###############
validate = 1  # 1 - validation, 0 - submission
N0 = 38        # total number of parts
N1 = 1        # number of part
#--------------------------
def duration(ci,co):
    if(ci!='' and co!=''):
        arrival = datetime.strptime(ci, '%Y-%m-%d').date()
        departure = datetime.strptime(co, '%Y-%m-%d').date()
        return (departure - arrival).days
    return 0

def duration_type(duration):
    if (duration==0):
        return 0
    if(duration<=2):
        return 1
    elif(duration<=4):
        return 2
    else:
        return 3

def run_solution():
    print('Preparing arrays...')
    f = gzip.open("../train.csv.gz", "r")
    f.readline()
    best_hotels_od_ulc = defaultdict(lambda: defaultdict(int))
    best_hotels_search_dest = defaultdict(lambda: defaultdict(int))
    best_hotels_search_dest1 = defaultdict(lambda: defaultdict(int))
    best_hotels_search_dest2 = defaultdict(lambda: defaultdict(int))
    best_hotel_country = defaultdict(lambda: defaultdict(int))
    hits = defaultdict(int)
    tp = defaultdict(float)

    popular_hotel_cluster = defaultdict(int)
    total = 0

    # Calc counts
    while 1:
        line = f.readline().strip()
        total += 1
        if total % 1000000 == 0:
            print('Read {} lines...'.format(total))
        if line == '':
            break
        print(line)
        arr = line.split(",")
        book_year = int(arr[0][:4])
        book_month = int(arr[0][5:7])
        user_location_city = arr[5]
        orig_destination_distance = arr[6]
        user_id = int(arr[7])
        is_package = int(arr[9])
        srch_destination_id = arr[16]
        is_booking = int(arr[18])
        hotel_country = arr[21]
        hotel_market = arr[22]
        hotel_cluster = arr[23]
        # ci = arr[11]
        # co = arr[12]
        # trip_duration = duration(ci,co)
        # trip_duration_type = duration_type(trip_duration)


        if validate == 1 and user_id % N0 == N1:
            continue

        append_0 = (book_year - 2012)*12 + book_month
        append_1 = ((book_year - 2012)*12 + book_month) * (1 + 10*is_booking)
        append_2 = ((book_year - 2012)*12 + book_month) * (1 + 5*is_booking)
        # append_3 = ((book_year - 2012)*12 + book_month) * (1 + 15*is_booking)


        if user_location_city != '' and orig_destination_distance != '':
            best_hotels_od_ulc[(user_location_city, orig_destination_distance)][hotel_cluster] += append_0

        # if srch_destination_id != '' and hotel_country != '' and hotel_market != '' and book_year != '' and trip_duration_type!=0:
        #     best_hotels_search_dest2[(srch_destination_id, hotel_country, hotel_market,is_package,trip_duration_type)][hotel_cluster] += append_3

        if srch_destination_id != '' and hotel_country != '' and hotel_market != '' and book_year != '':
            best_hotels_search_dest[(srch_destination_id, hotel_country, hotel_market,is_package)][hotel_cluster] += append_1

        if srch_destination_id != '':
            best_hotels_search_dest1[srch_destination_id][hotel_cluster] += append_1

        if hotel_country != '':
            best_hotel_country[hotel_country][hotel_cluster] += append_2

        popular_hotel_cluster[hotel_cluster] += 1

    f.close()
    ###########################
    now = datetime.now()
    if validate == 1:
        print('Validation...')
        f = gzip.open("../train.csv.gz", "r")
        path = 'validation/' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
    else:
        print('Generate submission...')
        f = gzip.open("../test.csv.gz", "r")
        path = 'submission/' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
    out = open(path, "w")
    f.readline()
    total = 0
    totalv = 0
    leak = 0
    out.write("id,hotel_cluster\n")
    topclasters = nlargest(5, sorted(popular_hotel_cluster.items()), key=itemgetter(1))

    while 1:
        line = f.readline().strip()
        total += 1
        if total % 10000000 == 0:
            print('Write {} lines...'.format(total))

        if line == '':
            break

        arr = line.split(",")
        if validate == 1:
            book_year = int(arr[0][:4])
            book_month = int(arr[0][5:7])
            user_location_city = arr[5]
            orig_destination_distance = arr[6]
            user_id = int(arr[7])
            is_package = int(arr[9])
            srch_destination_id = arr[16]
            is_booking = int(arr[18])
            hotel_country = arr[21]
            hotel_market = arr[22]
            hotel_cluster = arr[23]
            # ci = arr[11]
            # co = arr[12]
            # trip_duration = duration(ci,co)
            # trip_duration_type = duration_type(trip_duration)
            id = 0
            # if user_id % N0 != N1:
            #     continue
            if (user_id % N0 == 0 or user_id % N0 == N1 + 1):
                continue
            if is_booking == 0:
                continue
        else:
            id = arr[0]
            user_location_city = arr[6]
            orig_destination_distance = arr[7]
            user_id = int(arr[8])
            is_package = int(arr[10])
            srch_destination_id = arr[17]
            hotel_country = arr[20]
            hotel_market = arr[21]
            is_booking = 1
            # ci = arr[12]
            # co = arr[13]
            # trip_duration = duration(ci,co)
            # trip_duration_type = duration_type(trip_duration)

        totalv += 1
        out.write(str(id) + ',')
        filled = []

        s1 = (user_location_city, orig_destination_distance)
        # if(orig_destination_distance!=''):
        #     s1 = (user_location_city, int(float(orig_destination_distance)))

        if s1 in best_hotels_od_ulc:
            leak +=1
            d = best_hotels_od_ulc[s1]
            topitems = nlargest(5, d.items(), key=itemgetter(1))
            for i in range(len(topitems)):
                if len(filled) == 5:
                    break
                if topitems[i][0] in filled:
                    continue
                out.write(' ' + topitems[i][0])
                filled.append(topitems[i][0])
                if validate == 1:
                    if topitems[i][0]==hotel_cluster:
                        hits[len(filled)] +=1

        # s12 = (srch_destination_id, hotel_country, hotel_market,is_package,trip_duration_type)
        # if s12 in best_hotels_search_dest2:
        #     d = best_hotels_search_dest[s12]
        #     topitems = nlargest(5, d.items(), key=itemgetter(1))
        #     for i in range(len(topitems)):
        #         if len(filled) == 5:
        #             break
        #         if topitems[i][0] in filled:
        #             continue
        #         out.write(' ' + topitems[i][0])
        #         filled.append(topitems[i][0])
        #         if validate == 1:
        #             if topitems[i][0]==hotel_cluster:
        #                 hits[len(filled)] +=1

        s2 = (srch_destination_id, hotel_country, hotel_market,is_package)
        if s2 in best_hotels_search_dest:
            d = best_hotels_search_dest[s2]
            topitems = nlargest(5, d.items(), key=itemgetter(1))
            for i in range(len(topitems)):
                if len(filled) == 5:
                    break
                if topitems[i][0] in filled:
                    continue
                out.write(' ' + topitems[i][0])
                filled.append(topitems[i][0])
                if validate == 1:
                    if topitems[i][0]==hotel_cluster:
                        hits[len(filled)] +=1

        if srch_destination_id in best_hotels_search_dest1:
            d = best_hotels_search_dest1[srch_destination_id]
            topitems = nlargest(5, d.items(), key=itemgetter(1))
            for i in range(len(topitems)):
                if len(filled) == 5:
                    break
                if topitems[i][0] in filled:
                    continue
                out.write(' ' + topitems[i][0])
                filled.append(topitems[i][0])
                if validate == 1:
                    if topitems[i][0]==hotel_cluster:
                        hits[len(filled)] +=1


        if hotel_country in best_hotel_country:
            d = best_hotel_country[hotel_country]
            topitems = nlargest(5, d.items(), key=itemgetter(1))
            for i in range(len(topitems)):
                if len(filled) == 5:
                    break
                if topitems[i][0] in filled:
                    continue
                out.write(' ' + topitems[i][0])
                filled.append(topitems[i][0])
                if validate == 1:
                    if topitems[i][0]==hotel_cluster:
                        hits[len(filled)] +=1


        for i in range(len(topclasters)):
            if len(filled) == 5:
                    break
            if topclasters[i][0] in filled:
                continue
            out.write(' ' + topclasters[i][0])
            filled.append(topclasters[i][0])
            if validate == 1:
                if topclasters[i][0]==hotel_cluster:
                    hits[len(filled)] +=1


        out.write("\n")
    out.close()
    print('Completed!')
    # validation >>>
    scores = 0.0
    classified = 0
    if validate == 1:
        for jj in range(1,6):
            scores +=  hits[jj]*1.0/jj
            tp[jj] = hits[jj]*100.0/totalv
            classified += hits[jj]
        misclassified = totalv-classified
        miscp = misclassified*100.0/totalv
        print("")
        print(" validation")
        print("----------------------------------------------------------------")
        print("position %8d %8d %8d %8d %8d %8d+" % (1,2,3,4,5,6))
        print("hits     %8d %8d %8d %8d %8d %8d " % (hits[1],hits[2],hits[3],hits[4],hits[5],misclassified))
        print("hits[%%]  %8.2f %8.2f %8.2f %8.2f %8.2f %8.2f " % (tp[1],tp[2],tp[3],tp[4],tp[5],miscp))
        print("----------------------------------------------------------------")
        print("MAP@5 = %8.4f " % (scores*1.0/totalv))
        print("leakage = %6.2f%%" % (leak*100.0/totalv))
    # <<< validation
    if validate == 0:
        print("leakage = %6.2f%%" % (leak*100.0/total))

run_solution()