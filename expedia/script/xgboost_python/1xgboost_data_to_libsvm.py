import pandas as pd

print('lecture des données...')

train = pd.read_csv('../../train.csv',nrows=100000)
test = pd.read_csv('../../test.csv',nrows=100000)

print('Exportation en csv des données pertinentes')

X_train = train.drop(['hotel_cluster','date_time','srch_ci','srch_co',],1).to_csv('x_train.csv',header=False,index=False)
Y_train = train['hotel_cluster'].to_csv('y_train.csv',header=False,index=False)

X_test = test.drop(['date_time','srch_ci','srch_co'],1).to_csv('x_test.csv',header=False,index=False)


