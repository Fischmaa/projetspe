# Packages
require(methods)
require(data.table)
require(magrittr)
require(BBmisc)
require(dplyr)
require(stringr)
require(lubridate)
require(e1071)

# Pseudo-aléatoire
set.seed(42)

# Lecture de données
train <- fread('./train.csv', header = T, stringsAsFactors = F)
test <- fread('./test.csv', header = T, stringsAsFactors = F)
train = train[sample(1:nrow(train), 2000000, replace=FALSE)]

# On supprime les colonnes inutiles (cnt, hotel_cluster, id ...)
train[,is_booking := NULL]
train[,cnt := NULL]
submission<-data.frame(id=test$id,hotel_cluster=character(1))
test[, id := NULL]
#gc()

#Pré-traitement
train$date_time<-str_sub(train$date_time, 1, 10)
train$day_action<-day(as.Date(train$date_time))
train$month_action<-month(as.Date(train$date_time))
train$day_ci<-day(as.Date(train$srch_ci))
train$month_ci<-month(as.Date(train$srch_ci))
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
test$trip_duration<-as.numeric(as.Date(test$srch_co)-as.Date(test$srch_ci))
test$dayofyear_action<-round(as.numeric(difftime(strptime(as.Date(test$date_time), format = "%Y-%m-%d"),strptime("01.01.2012", format = "%d.%m.%Y"),units="day"))+1)%%365
test$dayofyear_ci<-round(as.numeric(difftime(strptime(as.Date(test$srch_ci), format = "%Y-%m-%d"),strptime("01.01.2012", format = "%d.%m.%Y"),units="day"))+1)%%365
test[, date_time := NULL]
test[, srch_ci := NULL]
test[, srch_co := NULL]
#gc()

# Création du modèle :
classifier<-naiveBayes(as.factor(hotel_cluster)~.,data=train, laplace=1)
submission$hotel_cluster<-gsub(",","",toString(rev((order(predict(classifier, test, type="raw"))-1)[96:100])))

write.csv(submission, file = "submission_Naive_Bayes_3.csv", row.names=FALSE)

# Copier jusqu'ici pour avoir l'exec de la dernière ligne ;)
