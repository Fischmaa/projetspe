# Packages
require(xgboost)
require(methods)
require(data.table)
require(magrittr)
require(BBmisc)
require(dplyr)
require(stringr)
require(lubridate)
require(e1071)

# Lecture données
train <- fread('PROJET_SPE/train.csv', header = T, stringsAsFactors = F)
test <- fread('PROJET_SPE/test.csv', header = T, stringsAsFactors = F)

# Train ne contient que les booking
# On supprime les colonnes inutiles (cnt, hotel_cluster, id ...)
train<-train[is_booking==1]
train[,is_booking := NULL]
train[,cnt := NULL]
train[, id := NULL]
submission<-data.frame(id=test$id,hotel_cluster=NA)
test[, id := NULL]
#gc()

#Pré-traitement
train$date_time<-str_sub(train$date_time, 1, 10)
train$day_action<-day(as.Date(train$date_time))
train$month_action<-month(as.Date(train$date_time))
train$day_ci<-day(as.Date(train$srch_ci))
train$month_ci<-month(as.Date(train$srch_ci))
#train$day_co<-day(as.Date(train$srch_co))
#train$month_co<-month(as.Date(train$srch_co))
train$trip_duration<-as.numeric(as.Date(train$srch_co)-as.Date(train$srch_ci))
train$dayofyear_action<-round(as.numeric(difftime(strptime(as.Date(train$date_time), format = "%Y-%m-%d"),strptime("01.01.2012", format = "%d.%m.%Y"),units="day"))+1)%%365
train$dayofyear_ci<-round(as.numeric(difftime(strptime(as.Date(train$srch_ci), format = "%Y-%m-%d"),strptime("01.01.2012", format = "%d.%m.%Y"),units="day"))+1)%%365
train[, date_time := NULL]
train[, srch_ci := NULL]
train[, srch_co := NULL]
#gc()
# On se demande si on utilise la moyenne pour remplace les NA (?) :
# train$orig_destination_distance[is.na(train$orig_destination_distance)]<-mean(na.omit(train$orig_destination_distance))

test$date_time<-str_sub(test$date_time, 1, 10)
test$day_action<-day(as.Date(test$date_time))
test$month_action<-month(as.Date(test$date_time))
test$day_ci<-day(as.Date(test$srch_ci))
test$month_ci<-month(as.Date(test$srch_ci))
#test$day_co<-day(as.Date(test$srch_co))
#test$month_co<-month(as.Date(test$srch_co))
test$trip_duration<-as.numeric(as.Date(test$srch_co)-as.Date(test$srch_ci))
test$dayofyear_action<-round(as.numeric(difftime(strptime(as.Date(test$date_time), format = "%Y-%m-%d"),strptime("01.01.2012", format = "%d.%m.%Y"),units="day"))+1)%%365
test$dayofyear_ci<-round(as.numeric(difftime(strptime(as.Date(test$srch_ci), format = "%Y-%m-%d"),strptime("01.01.2012", format = "%d.%m.%Y"),units="day"))+1)%%365
test[, date_time := NULL]
test[, srch_ci := NULL]
test[, srch_co := NULL]
#gc()

# Création du modèle :
classifier<-naiveBayes(as.factor(hotel_cluster)~.,data=train)

# Prédiction :
# RAPPEL : nrow(test) = 2528243

for (i in 1:nrow(test)){
	res<-rev((order(predict(classifier, test[i], type="raw"))-1)[96:100])
	submission$hotel_cluster[i]<-paste(res[1],res[2],res[3],res[4],res[5],sep=" ")
}


write.csv(submission, file = "submission_Naive_Bayes.csv", row.names=FALSE)

# Copier jusqu'ici pour avoir l'exec de la dernière ligne ;)
