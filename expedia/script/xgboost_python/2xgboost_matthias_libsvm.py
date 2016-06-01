import xgboost as xgb

print('Lecture des matrices')

X_train = xgb.DMatrix('x_train.data')
Y_train = xgb.DMatrix('y_train.csv')

gbm = xgb.XGBClassifier(max_depth=3, n_estimators=50, learning_rate=0.1)

print('fitting...')
gbm.fit(X_train,Y_train)

del X_train, Y_train

print('predict')
X_test = xgb.DMatrix('x_test.data')
Y_test = gbm.predict(X_test)

result = pd.DataFrame(test['id'])
result["hotel_cluster"] = pd.DataFrame(Y_test)

print('export')
result.to_csv("resultats_xgboost_matthias.csv")
