from include.count_items import *

len,dest = count_values("../test.csv", "user_id",37670000)

dest.to_csv('users_in_test.csv');

