# Packages
require(methods)
require(data.table)
require(magrittr)
require(BBmisc)
require(dplyr)
require(stringr)
require(lubridate)
require(e1071)
require(tictoc)

# Lecture de données
train <- fread('./train.csv', header = T, stringsAsFactors = F)
test <- fread('./test.csv', header = T, stringsAsFactors = F)
#submission<-data.frame(id=test$id,hotel_cluster=character(1))

# On supprime les colonnes inutiles (cnt, hotel_cluster, id ...)
train[,is_booking := NULL]
train[,cnt := NULL]
test[,id := NULL]
#gc()

#Pré-traitement
train$date_time<-str_sub(train$date_time, 1, 10)
train$month_action<-month(as.Date(train$date_time))
train$trip_duration<-as.numeric(as.Date(train$srch_co)-as.Date(train$srch_ci))
train[, date_time := NULL]
train[, srch_ci := NULL]
train[, srch_co := NULL]
#gc()
# On se demande si on utilise la moyenne pour remplace les NA (?) :
# train$orig_destination_distance[is.na(train$orig_destination_distance)]<-mean(na.omit(train$orig_destination_distance))

test$date_time<-str_sub(test$date_time, 1, 10)
test$month_action<-month(as.Date(test$date_time))
test$trip_duration<-as.numeric(as.Date(test$srch_co)-as.Date(test$srch_ci))
test[, date_time := NULL]
test[, srch_ci := NULL]
test[, srch_co := NULL]
#gc()

# Création du modèle :
classifier<-naiveBayes(as.factor(hotel_cluster)~.,data=train, laplace=1)


# SOLUTION 1 - 105s :
tic()
fileConn<-file("sub.csv","w+")
writeLines("\"id\",\"hotel_cluster\"",sep="\n",con=fileConn)
for (i in 1:5000){
	writeLines(paste(toString(i-1),",\"",gsub(",","",toString(rev((order(predict(classifier, test[i], type="raw"))-1)[96:100]))),"\"",sep=""),sep="\n",con=fileConn)
}
close(fileConn)
exectime <- toc()
#


# SOLUTION 2 - Hors Compet' ... trop long :
print("----")
tic()
for (i in 1:5000){
	res<-rev((order(predict(classifier, test[i], type="raw"))-1)[96:100])
	submission$hotel_cluster[i]<-paste(res[1],res[2],res[3],res[4],res[5],sep=" ")
}
exectime <- toc()
write.csv(submission, file = "sub_2.csv", row.names=FALSE)
tic()
exectime <- toc()
#


# SOLUTION 3 - 98.5s :
tic()
sink("sink_submission.csv")
	cat("\"id\",\"hotel_cluster\"")
	for (i in 1:5000){
		cat((i-1),",",gsub(",","",toString(rev((order(predict(classifier, test[i], type="raw"))-1)[96:100]))),"\n",sep="")
	}
sink()
exectime <- toc()
#
