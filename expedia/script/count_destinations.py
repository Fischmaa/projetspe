from include.count_items import *

len,dest = count_values("../test.csv", "srch_destination_id",2528000)

dest.to_csv('dests_test.csv')

