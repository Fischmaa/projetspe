
## Regression linéaire

Pour une première approche de prédiction on utilise un algorithme de regression linéaire.

### R

#### Régression linéaire avec données continues

La toute première solution envisagée était d'effectuer une régression linéaire directement sur les données du problème.

```R
# Utilisation de librairies pour la gestion de la date et du stepAIC
library(MASS)
library(lubridate)
 
# Lecture des données
train <- read.csv("./sources/train.csv")

# Traduction de la date en jour, sous forme d'entier entre 1 et 7 :  
train$date<-wday(ymd_hms(train$datetime), label=TRUE)
train$date<-as.integer(train$date)

# Supprime la date "String" pour avoir une matrice de corrélation et essayer de voir le lien entre les 
# différentes variables
train<-train[,-c(1)]
cor(train)

# Regression linéaire (on retire les variables registred et casual)
train<-train[,-c(9)]
train<-train[,-c(9)]
mylm<-lm(count~.,data=train)
stepAIC(mylm)

#Coefficients:
#(Intercept)       season      weather         temp        atemp     humidity  
#   125.3005      22.6820       5.8493       1.6584       5.8229      -3.0411  
#  windspeed         date  
#     0.7966       1.9603

test <- read.csv("./sources/test.csv")
test$hour  <- hour(ymd_hms(test$datetime))
test$day <- wday(ymd_hms(test$datetime), label=TRUE)
test$day<-as.integer(test$day)

# On pré-remplit le résultat final !
submission <- data.frame(datetime=test$datetime, count=NA)

# On applique le modèle
for (i in 1:nrow(test)){
	submission[i,2] = max(125.3005+test$season[i]*22.6820+test$weather[i]*5.8493+test$temp[i]*1.6584+test$atemp[i]*5.8229+test$humidity[i]*-3.0411+test$windspeed[i]*0.7966+test$day[i]*1.9603,0)
}

# Ecriture du fichier à soumettre 
write.csv(submission, file = "./Résultats/linear_model.csv", row.names=FALSE)

```

Nous avons alors soumis le résultat à Kaggle et obtenu le score suivant :

![Modèle 1](http://nsa38.casimages.com/img/2016/05/19/160519095057129443.png)

#### Régression linéaire avec 2 modèles - semaine vs. week-end

Le résultat était loin d'être satisfaisant : après avoir exploré les forums de discussion de Kaggle nous avons vu qu'il était possible de descendre à un score proche 0,7. Nous avons essayé d'identifier ce qui pourrait expliquer le problème de convergence de notre modèle; après étude graphique des données, nous nous sommes rendus compte qu'il fallait trouver un modèle différent pour la semaine et pour le week-end. Nous avons donc découpé le jeu de données selon la valeur de day et avons effectué une regression linéaire pour chaque ensemble.

![WE vs. semaine (par *Beata Strubel*)](http://nsa37.casimages.com/img/2016/05/19/160519102759976692.png)

```R
# Librairies : dates et stepAIC
library(MASS)
library(lubridate) 

# Lecture de données
train <- read.csv("./sources/train.csv")

# Traduction de la date et retrait de la date "String"
train$hour  <- hour(ymd_hms(train$datetime))
train$day <- wday(ymd_hms(train$datetime), label=TRUE)
train$day<-as.integer(train$day)
train<-train[,-c(1)]
train<-train[,-c(9)]
train<-train[,-c(9)]

# Découpage des données en deux ensembles
weekend_train<-subset(train,day==6 | day==7)
semaine_train<-subset(train,day<6)

# SEMAINE

mylm_semaine<-lm(count~.,data=semaine_train)
stepAIC(mylm_semaine)
#Coefficients:
#(Intercept)       season      weather         temp        atemp     humidity  
#     5.8248      22.0184      -7.3750      -5.5177      11.1996      -1.9762  
#  windspeed         hour          day  
#     0.7709       7.8518       2.1974  

# WEEK-END

mylm_we<-lm(count~.,data=weekend_train)
stepAIC(mylm_we)
#Coefficients:
#(Intercept)       season      holiday      weather         temp        atemp  
#     64.358       20.180      -50.868        9.958        5.918        2.024  
#   humidity         hour  
#     -2.853        6.788  

# Chargement des données de test :
test <- read.csv("./sources/test.csv")
test$hour  <- hour(ymd_hms(test$datetime))
test$day <- wday(ymd_hms(test$datetime), label=TRUE)
test$day<-as.integer(test$day)

# On pré-remplit le résultat final
submission <- data.frame(datetime=test$datetime, count=NA)

# Application du modèle selon qu'on soit en semaine ou en w-e
for (i in 1:nrow(test)){
	if (test[i,11]<6) {
		submission[i,2] = max((5.8248+22.0184*test$season[i]-7.3750*test$weather[i]-5.5177*test$temp[i]+11.1996*test$atemp[i]-1.9762*test$humidity[i]+0.7709*test$windspeed[i]+7.8518*test$hour[i]+2.1974*test$day[i]),0)
	} else {
		submission[i,2] = max((64.358+20.18*test$season[i]-50.868*test$holiday[i]+9.958*test$weather[i]+5.918*test$temp[i]+2.024*test$atemp[i]-2.853*test$humidity[i]+6.788*test$hour[i]),0)
	}
}

write.csv(submission, file = "./Résultats/linear_double_model.csv", row.names=FALSE)
```
Nous avons alors soumis le résultat à Kaggle et obtenu le score suivant :

![Modèle 2](http://nsa37.casimages.com/img/2016/05/19/160519100724814761.png)

#### Régression linéaire avec données discrètes et découpage du problème

Le résultat ne nous semblant pas satisfaisant, nous avons relu les différentes données et observé que ces dernières n'étaient pas continues mais bien discrètes; en R, il nous fallait utiliser des `factor`. Nous avons donc recommencé le processus en utilisant cette commande sur les données discrètes : day, hour, humidity, etc.

```R
library(MASS)
library(lubridate) 

train <- read.csv("./sources/train.csv")
train$hour  <- hour(ymd_hms(train$datetime))
train$day <- wday(ymd_hms(train$datetime), label=TRUE)
train$day<-as.integer(train$day)
train<-train[,-c(1)]
train<-train[,-c(9)]
train<-train[,-c(9)]

# Utilisation des données discrètes
train$season<-as.factor(train$season)
train$holiday<-as.factor(train$holiday)
train$workingday<-as.factor(train$workingday)
train$weather<-as.factor(train$weather)
train$hour<-as.factor(train$hour)
train$day<-as.factor(train$day)

weekend_train<-subset(train,day==6|day==7)
semaine_train<-subset(train,day==1|day==2|day==3|day==4|day==5)


mylm_semaine<-lm(count~.,data=semaine_train)
stepAIC(mylm_semaine)

#Coefficients SEMAINE:
#(Intercept)      season2      season3      season4     weather2     weather3  
#   -50.0786      36.6715      25.1435      65.4588      -7.5642     -66.2426  
#   weather4        atemp     humidity    windspeed        hour1        hour2  
#  -162.7082       5.6239      -0.8513      -0.3689     -14.2564     -23.7641  
#      hour3        hour4        hour5        hour6        hour7        hour8  
#   -31.4254     -29.8396     -12.7936      53.2585     204.1481     350.2259  
#      hour9       hour10       hour11       hour12       hour13       hour14  
#   170.3309     100.8405     120.1680     157.8629     149.1133     130.1037  
#     hour15       hour16       hour17       hour18       hour19       hour20  
#   141.0937     216.4165     407.9490     384.3493     261.1313     175.9108  
#     hour21       hour22       hour23         day2         day3         day4  
#   118.6451      74.7748      29.7653       3.9519       7.3319      11.4758  
#       day5  
#    13.1366

mylm_we<-lm(count~.,data=weekend_train)
stepAIC(mylm_we)

#Coefficients WE:
#(Intercept)      season2      season3      season4     holiday1     weather2  
#      3.280       37.554        5.952       64.561      -56.696       -2.438  
#   weather3         temp     humidity    windspeed        hour1        hour2  
#    -52.653        7.609       -1.180       -1.484      -20.878      -33.024  
#      hour3        hour4        hour5        hour6        hour7        hour8  
#    -48.523      -52.569      -39.744        3.264       94.678      228.199  
#      hour9       hour10       hour11       hour12       hour13       hour14  
#    151.200      126.615      164.506      206.085      208.754      193.470  
#     hour15       hour16       hour17       hour18       hour19       hour20  
#    202.987      235.425      310.524      255.343      177.771      107.417  
#     hour21       hour22       hour23  
#     75.212       64.078       41.828  

test <- read.csv("./sources/test.csv")
test$hour  <- hour(ymd_hms(test$datetime))
test$day <- wday(ymd_hms(test$datetime), label=TRUE)
test$day <- as.integer(test$day)

# On pré-remplit le résultat final !
submission <- data.frame(datetime=test$datetime, count=NA)

# On remplit avec une boucle :
for (i in 1:nrow(test)){
	if (test$day[i]!=6 & test$day[i]!=7) {
		submission[i,2] = max(0,-50.0786
					+as.integer(test$season[i]==2)*36.6715
					+as.integer(test$season[i]==3)*25.1435
					+as.integer(test$season[i]==4)*65.4588
					+as.integer(test$weather[i]==2)*-7.5642
					+as.integer(test$weather[i]==3)*-66.2426
					+as.integer(test$weather[i]==4)*-162.7082
					+test$atemp[i]*5.6239
					+test$humidity[i]*-0.8513
					+test$windspeed[i]*-0.3689
					+as.integer(test$hour[i]==1)*-14.2564
					+as.integer(test$hour[i]==2)*-23.7641
					+as.integer(test$hour[i]==3)*-31.4254
					+as.integer(test$hour[i]==4)*-29.8396
					+as.integer(test$hour[i]==5)*-12.7936
					+as.integer(test$hour[i]==6)*53.2585
					+as.integer(test$hour[i]==7)*204.1481
					+as.integer(test$hour[i]==8)*350.2259
					+as.integer(test$hour[i]==9)*170.3309
					+as.integer(test$hour[i]==10)*100.8405
					+as.integer(test$hour[i]==11)*120.1680
					+as.integer(test$hour[i]==12)*157.8629
					+as.integer(test$hour[i]==13)*149.1133
					+as.integer(test$hour[i]==14)*130.1037
					+as.integer(test$hour[i]==15)*141.0937
					+as.integer(test$hour[i]==16)*216.4165
					+as.integer(test$hour[i]==17)*407.9490
					+as.integer(test$hour[i]==18)*384.3493
					+as.integer(test$hour[i]==19)*261.1313
					+as.integer(test$hour[i]==20)*175.9108
					+as.integer(test$hour[i]==21)*118.6451
					+as.integer(test$hour[i]==22)*74.7748
					+as.integer(test$hour[i]==23)*29.7653
					+as.integer(test$day[i]==2)*3.9519
					+as.integer(test$day[i]==3)*7.3319
					+as.integer(test$day[i]==4)*11.4758
					+as.integer(test$day[i]==5)*13.1366)
	} else {
		submission[i,2] = max(0,3.280
					+as.integer(test$season[i]==2)*37.554
					+as.integer(test$season[i]==3)*5.952
					+as.integer(test$season[i]==4)*64.561
					+as.integer(test$holiday[i]==1)*-56.696
					+as.integer(test$weather[i]==2)*-2.438
					+as.integer(test$weather[i]==3)*-53.653
					+test$temp[i]*7.609
					+test$humidity[i]*-1.180
					+test$windspeed[i]*-1.484
					+as.integer(test$hour[i]==1)*-20.878
					+as.integer(test$hour[i]==2)*-33.024
					+as.integer(test$hour[i]==3)*-48.523
					+as.integer(test$hour[i]==4)*-52.569
					+as.integer(test$hour[i]==5)*-39.744
					+as.integer(test$hour[i]==6)*3.264
					+as.integer(test$hour[i]==7)*94.678
					+as.integer(test$hour[i]==8)*228.199
					+as.integer(test$hour[i]==9)*151.200
					+as.integer(test$hour[i]==10)*126.615
					+as.integer(test$hour[i]==11)*164.506
					+as.integer(test$hour[i]==12)*206.085
					+as.integer(test$hour[i]==13)*208.754
					+as.integer(test$hour[i]==14)*193.470
					+as.integer(test$hour[i]==15)*202.987
					+as.integer(test$hour[i]==16)*235.425
					+as.integer(test$hour[i]==17)*310.524
					+as.integer(test$hour[i]==18)*255.343
					+as.integer(test$hour[i]==19)*177.771
					+as.integer(test$hour[i]==20)*107.417
					+as.integer(test$hour[i]==21)*75.212
					+as.integer(test$hour[i]==22)*64.078
					+as.integer(test$hour[i]==23)*41.828)
	}
}

write.csv(submission, file = "./Résultats/linear_factor_model.csv", row.names=FALSE)
```
Nous avons alors soumis le résultat à Kaggle et obtenu le score suivant :

![Modèle 3](http://nsa38.casimages.com/img/2016/05/19/160519101030615704.png)


#### Régression linéaire avec données discrètes, découpage du problème et modélisation de Poisson

Malgré la bonne représentation des données, nous n'arrivions pas à attendre cette erreur de 0,7. Nous nous sommes demandé d'où venait le problème et avons réalisé que le choix de famille de modèle pour la régression linéaire n'était pas bon. En effet, notre problème est un problème de *comptage*. Or, pour un problème de comptage avec un temps d'attente aléatoire (représenté par une loi exponentielle), le modèle le plus adapté est celui de Poisson et non Binomial (valeur par défaut lors de l'utilisation de la commande lm en R). Nous avons donc décidé d'utiliser la commande `glm` avec l'option `family=poisson`.

```R
library(MASS)
library(lubridate) 

train <- read.csv("./sources/train.csv")
train$hour  <- hour(ymd_hms(train$datetime))
train$day <- wday(ymd_hms(train$datetime), label=TRUE)
train$day<-as.integer(train$day)
train<-train[,-c(1)]
train<-train[,-c(9)]
train<-train[,-c(9)]

train$season<-as.factor(train$season)
train$holiday<-as.factor(train$holiday)
train$workingday<-as.factor(train$workingday)
train$weather<-as.factor(train$weather)
train$hour<-as.factor(train$hour)
train$day<-as.factor(train$day)

weekend_train<-subset(train,day==6|day==7)
semaine_train<-subset(train,day==1|day==2|day==3|day==4|day==5)


mylm_semaine<-glm(count~.,family=poisson,data=semaine_train)
stepAIC(mylm_semaine)

#Coefficients SEMAINE:
#(Intercept)      season2      season3      season4     holiday1     weather2  
#   3.130707     0.306955     0.261947     0.458529     0.031317    -0.029764  
#   weather3     weather4         temp        atemp     humidity    windspeed  
#  -0.446305    -0.280125    -0.027459     0.052148    -0.003349    -0.001507  
#      hour1        hour2        hour3        hour4        hour5        hour6  
#  -0.480038    -0.868608    -1.476324    -1.963302    -0.720236     0.671073  
#      hour7        hour8        hour9       hour10       hour11       hour12  
#   1.690574     2.148028     1.530881     1.168629     1.290751     1.473194  
#     hour13       hour14       hour15       hour16       hour17       hour18  
#   1.438200     1.352814     1.406096     1.695269     2.203607     2.164263  
#     hour19       hour20       hour21       hour22       hour23         day2  
#   1.852338     1.558092     1.278076     0.979048     0.505867     0.014545  
#       day3         day4         day5  
#   0.035558     0.059364     0.077021 

mylm_we<-glm(count~.,family=poisson,data=weekend_train)
stepAIC(mylm_we)

#Coefficients WE:
#(Intercept)      season2      season3      season4     holiday1     weather2  
#   3.720409     0.307315     0.179893     0.440373    -0.343101    -0.046036  
#   weather3         temp        atemp     humidity    windspeed        hour1  
#  -0.419899     0.026352     0.006714    -0.003647    -0.003207    -0.433234  
#      hour2        hour3        hour4        hour5        hour6        hour7  
#  -0.825576    -1.579685    -2.343833    -1.489425    -0.213172     0.761262  
#      hour8        hour9       hour10       hour11       hour12       hour13  
#   1.379637     1.071734     0.968406     1.133156     1.267780     1.266597  
#     hour14       hour15       hour16       hour17       hour18       hour19  
#   1.219325     1.247909     1.348306     1.559823     1.423719     1.193381  
#     hour20       hour21       hour22       hour23  
#   0.899586     0.716428     0.630703     0.449692 

test <- read.csv("./sources/test.csv")
test$hour  <- hour(ymd_hms(test$datetime))
test$day <- wday(ymd_hms(test$datetime), label=TRUE)
test$day <- as.integer(test$day)

# On pré-remplit le résultat final
submission <- data.frame(datetime=test$datetime, count=NA)

# On remplit avec une boucle :
for (i in 1:nrow(test)){
	if (test$day[i]!=6 & test$day[i]!=7) {
		submission[i,2] = max(0,exp(3.130707
					+as.integer(test$season[i]==2)*0.306955
					+as.integer(test$season[i]==3)*0.261947
					+as.integer(test$season[i]==4)*0.458529
					+as.integer(test$holiday[i]==1)*0.031317
					+as.integer(test$weather[i]==2)*-0.029764
					+as.integer(test$weather[i]==3)*-0.446305
					+as.integer(test$weather[i]==4)*-0.380125
					+test$temp[i]*-0.027459
					+test$atemp[i]*0.052148
					+test$humidity[i]*-0.003349
					+test$windspeed[i]*-0.001507
					+as.integer(test$hour[i]==1)*-0.480038
					+as.integer(test$hour[i]==2)*-0.868608
					+as.integer(test$hour[i]==3)*-1.476324
					+as.integer(test$hour[i]==4)*-1.963302
					+as.integer(test$hour[i]==5)*-0.720236
					+as.integer(test$hour[i]==6)*0.671073
					+as.integer(test$hour[i]==7)*1.690574
					+as.integer(test$hour[i]==8)*2.148028
					+as.integer(test$hour[i]==9)*1.530881
					+as.integer(test$hour[i]==10)*1.168629
					+as.integer(test$hour[i]==11)*1.290751
					+as.integer(test$hour[i]==12)*1.473194
					+as.integer(test$hour[i]==13)*1.438200
					+as.integer(test$hour[i]==14)*1.352814
					+as.integer(test$hour[i]==15)*1.406096
					+as.integer(test$hour[i]==16)*1.695269
					+as.integer(test$hour[i]==17)*2.203607
					+as.integer(test$hour[i]==18)*2.164263
					+as.integer(test$hour[i]==19)*1.852338
					+as.integer(test$hour[i]==20)*1.558092
					+as.integer(test$hour[i]==21)*1.278076
					+as.integer(test$hour[i]==22)*0.979048
					+as.integer(test$hour[i]==23)*0.505867
					+as.integer(test$day[i]==2)*0.014545
					+as.integer(test$day[i]==3)*0.035558
					+as.integer(test$day[i]==4)*0.059364
					+as.integer(test$day[i]==5)*0.077021))
	} else {
		submission[i,2] = max(0,exp(3.720409
					+as.integer(test$season[i]==2)*0.307315
					+as.integer(test$season[i]==3)*0.179893
					+as.integer(test$season[i]==4)*0.440373
					+as.integer(test$holiday[i]==1)*-0.343101
					+as.integer(test$weather[i]==2)*-0.046036
					+as.integer(test$weather[i]==3)*-0.419899
					+test$temp[i]*0.026352
					+test$atemp[i]*0.006714
					+test$humidity[i]*-0.003647
					+test$windspeed[i]*-0.003207
					+as.integer(test$hour[i]==1)*-0.433234
					+as.integer(test$hour[i]==2)*-0.825576
					+as.integer(test$hour[i]==3)*-1.579685
					+as.integer(test$hour[i]==4)*-2.343833
					+as.integer(test$hour[i]==5)*-1.489425
					+as.integer(test$hour[i]==6)*-0.213172
					+as.integer(test$hour[i]==7)*0.761262
					+as.integer(test$hour[i]==8)*1.379637
					+as.integer(test$hour[i]==9)*1.071734
					+as.integer(test$hour[i]==10)*0.968406
					+as.integer(test$hour[i]==11)*1.133156
					+as.integer(test$hour[i]==12)*1.267780
					+as.integer(test$hour[i]==13)*1.266597
					+as.integer(test$hour[i]==14)*1.219325
					+as.integer(test$hour[i]==15)*1.247909
					+as.integer(test$hour[i]==16)*1.348306
					+as.integer(test$hour[i]==17)*1.559823
					+as.integer(test$hour[i]==18)*1.423719
					+as.integer(test$hour[i]==19)*1.193381
					+as.integer(test$hour[i]==20)*0.899586
					+as.integer(test$hour[i]==21)*0.716428
					+as.integer(test$hour[i]==22)*0.630703
					+as.integer(test$hour[i]==23)*0.449692))
	}
}

write.csv(submission, file = "./Résultats/linear_poisson_factor_model.csv", row.names=FALSE)
```

Nous avons alors soumis le résultat à Kaggle et obtenu le score suivant, plutôt satisfaisant :

![Modèle 4](http://nsa38.casimages.com/img/2016/05/19/160519101616150129.png)

### Python

Regression de Poisson avec différents ajouts de variables : 
* ahot : chaleur ressentie (discrétisation de atemp)
* hot : chaleur ( discrétisation de temp)
* year
* day
* hour
* Sunday
```python
import pandas as pd 
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt 
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'
# reading data
train = pd.read_csv("sources/train.csv")
test = pd.read_csv("sources/test.csv")
```


```python
#add a new column 'date' convert into datetime for both training and test set
train['date']=0
for i in range(len(train)) :
	train['date'][i]=datetime.strptime(train['datetime'][i],'%Y-%m-%d %H:%M:%S')

train=train.set_index("datetime")


test['date']=0
for i in range(len(test)) :
	test['date'][i]=datetime.strptime(test['datetime'][i],'%Y-%m-%d %H:%M:%S')

test=test.set_index("datetime")
```


```python
#categorize training set
train_factor = train
train_factor['weather'] = train_factor['weather'].astype('category')
train_factor['holiday'] = train_factor['holiday'].astype('category')
train_factor['workingday'] = train_factor['workingday'].astype('category')
train_factor['season'] = train_factor['season'].astype('category')

#factorize test set
test_factor = test
test_factor['weather'] = test_factor['weather'].astype('category')
test_factor['holiday'] = test_factor['holiday'].astype('category')
test_factor['workingday'] = test_factor['workingday'].astype('category')
test_factor['season'] = test_factor['season'].astype('category')
```


```python
#create day of week column and hour column and a year colum then convert into category for both training and test set
train_factor['day']=0
train_factor['hour']=0
train_factor['year']=0
for i in range(len(train_factor)) :
    train_factor['day'][i] = train_factor['date'][i].weekday()
    train_factor['hour'][i] = train_factor['date'][i].hour
    train_factor['year'][i]=train_factor['date'][i].year

train_factor['day']=train_factor['day'].astype('category')
train_factor['hour']=train_factor['hour'].astype('category')
train_factor['year']=train_factor['year'].astype('category')

test_factor['day']=0
test_factor['hour']=0
test_factor['year']=0
for i in range(len(test_factor)) :
    test_factor['day'][i] = test_factor['date'][i].weekday()
    test_factor['hour'][i] = test_factor['date'][i].hour
    test_factor['year'][i]=test_factor['date'][i].year

test_factor['day']=test_factor['day'].astype('category')
test_factor['hour']=test_factor['hour'].astype('category')
test_factor['year']=test_factor['year'].astype('category')
```


```python
#is a day more significant ?
byday=train_factor.groupby('day')
print(byday.describe())
print('Sunday seems to be an important predictor')
```

                     atemp       casual        count     humidity   registered  \
    day                                                                          
    0   count  1551.000000  1551.000000  1551.000000  1551.000000  1551.000000   
        mean     24.178507    29.843972   190.390716    62.508059   160.546744   
        std       8.413965    35.909764   180.943376    18.314346   160.634673   
        min       5.305000     0.000000     1.000000    15.000000     0.000000   
        25%      17.425000     4.000000    39.000000    48.000000    33.000000   
        50%      25.000000    16.000000   146.000000    63.000000   120.000000   
        75%      31.060000    44.000000   277.500000    77.000000   221.500000   
        max      42.425000   242.000000   968.000000   100.000000   857.000000   
    1   count  1539.000000  1539.000000  1539.000000  1539.000000  1539.000000   
        mean     24.252898    22.979207   189.723847    63.662768   166.744639   
        std       8.500099    25.735518   186.719673    18.890279   169.318892   
        min       3.790000     0.000000     1.000000    17.000000     0.000000   
        25%      16.665000     3.000000    36.000000    49.000000    32.000000   
        50%      25.000000    13.000000   146.000000    65.000000   120.000000   
        75%      31.060000    36.000000   274.000000    79.000000   230.000000   
        max      42.425000   168.000000   970.000000   100.000000   839.000000   
    2   count  1551.000000  1551.000000  1551.000000  1551.000000  1551.000000   
        mean     23.764271    22.521599   188.411348    64.299162   165.889749   
        std       8.682894    28.743482   190.942004    19.443204   172.205508   
        min       0.760000     0.000000     1.000000    19.000000     0.000000   
        25%      16.665000     3.000000    38.000000    49.000000    33.000000   
        50%      24.240000    11.000000   136.000000    63.000000   119.000000   
        75%      31.060000    32.000000   270.500000    82.000000   230.500000   
        max      43.940000   237.000000   977.000000   100.000000   886.000000   
    3   count  1553.000000  1553.000000  1553.000000  1553.000000  1553.000000   
        mean     23.641465    24.007083   197.296201    58.397939   173.289118   
        std       8.482853    27.351838   187.606619    19.765084   169.286079   
        min       3.790000     0.000000     1.000000     0.000000     0.000000   
        25%      16.665000     3.000000    44.000000    44.000000    39.000000   
        50%      24.240000    13.000000   155.000000    58.000000   133.000000   
        75%      31.060000    37.000000   280.000000    73.000000   234.000000   
        max      43.940000   145.000000   901.000000   100.000000   812.000000   
    4   count  1529.000000  1529.000000  1529.000000  1529.000000  1529.000000   
        mean     23.066609    31.001962   197.844343    59.913015   166.842381   
        std       8.170464    34.723374   172.518208    18.951775   149.309872   
        min       6.060000     0.000000     1.000000     8.000000     0.000000   
        25%      15.910000     4.000000    52.000000    45.000000    45.000000   
        50%      22.725000    17.000000   167.000000    59.000000   139.000000   
        75%      30.305000    49.000000   290.000000    75.000000   239.000000   
        max      40.910000   240.000000   900.000000   100.000000   757.000000   
    5   count  1584.000000  1584.000000  1584.000000  1584.000000  1584.000000   
        mean     23.121266    63.625000   196.665404    61.253157   133.040404   
        std       8.418103    78.782825   180.917795    20.366222   108.727956   
        min       3.030000     0.000000     1.000000    12.000000     0.000000   
        25%      15.910000     6.000000    45.000000    45.000000    38.000000   
        50%      22.725000    28.000000   141.500000    61.000000   106.000000   
        75%      31.060000    98.250000   309.500000    78.000000   214.000000   
        max      43.940000   367.000000   783.000000   100.000000   474.000000   
    6   count  1579.000000  1579.000000  1579.000000  1579.000000  1579.000000   
        mean     23.569766    57.051298   180.839772    63.151995   123.788474   
        std       8.580719    67.881480   167.022145    18.198273   105.406905   
        min       2.275000     0.000000     1.000000    17.000000     0.000000   
        25%      16.665000     7.000000    43.000000    49.000000    34.000000   
        50%      22.725000    25.000000   119.000000    64.000000    93.000000   
        75%      31.060000    88.000000   298.000000    78.000000   201.000000   
        max      45.455000   304.000000   757.000000   100.000000   510.000000   
    
                      temp    windspeed  
    day                                  
    0   count  1551.000000  1551.000000  
        mean     20.620542    12.921691  
        std       7.778770     8.315761  
        min       4.100000     0.000000  
        25%      14.760000     7.001500  
        50%      21.320000    12.998000  
        75%      26.240000    16.997900  
        max      37.720000    47.998800  
    1   count  1539.000000  1539.000000  
        mean     20.732307    13.338829  
        std       7.821476     8.380758  
        min       4.100000     0.000000  
        25%      14.760000     7.001500  
        50%      21.320000    12.998000  
        75%      26.240000    19.001200  
        max      38.540000    51.998700  
    2   count  1551.000000  1551.000000  
        mean     20.323417    12.635379  
        std       7.912896     8.281205  
        min       0.820000     0.000000  
        25%      13.940000     7.001500  
        50%      20.500000    11.001400  
        75%      26.650000    19.001200  
        max      38.540000    43.000600  
    3   count  1553.000000  1553.000000  
        mean     20.251835    13.138079  
        std       7.806716     7.984815  
        min       4.100000     0.000000  
        25%      13.940000     7.001500  
        50%      20.500000    12.998000  
        75%      26.240000    19.001200  
        max      38.540000    46.002200  
    4   count  1529.000000  1529.000000  
        mean     19.993198    12.398527  
        std       7.649513     7.918166  
        min       3.280000     0.000000  
        25%      13.940000     7.001500  
        50%      19.680000    11.001400  
        75%      26.240000    16.997900  
        max      37.720000    40.997300  
    5   count  1584.000000  1584.000000  
        mean     19.668611    12.670136  
        std       7.780560     8.255741  
        min       4.100000     0.000000  
        25%      13.120000     7.001500  
        50%      18.860000    11.001400  
        75%      26.240000    16.997900  
        max      41.000000    50.002100  
    6   count  1579.000000  1579.000000  
        mean     20.041963    12.499344  
        std       7.750044     7.973855  
        min       3.280000     0.000000  
        25%      13.940000     7.001500  
        50%      18.860000    11.001400  
        75%      26.240000    16.997900  
        max      39.360000    56.996900  
    Sunday seems to be an important predictor



```python
#create Sunday variable and convert to category 
train_factor['Sunday'] = 0 ;
train_factor.ix[train_factor['day']==6,'Sunday']=1

train_factor['Sunday']=train_factor['Sunday'].astype('category')

test_factor['Sunday'] = 0 ;
test_factor.ix[test_factor['day']==6,'Sunday']=1

test_factor['Sunday']=test_factor['Sunday'].astype('category')
```


```python
train_factor['temp'].describe()
```




    count    10886.00000
    mean        20.23086
    std          7.79159
    min          0.82000
    25%         13.94000
    50%         20.50000
    75%         26.24000
    max         41.00000
    Name: temp, dtype: float64




```python
#create daypart variable and convert to category (8 category) for both training and test set
train_factor['daypart'] = 8
for i in range(len(train_factor)) :
    currentHour = train_factor['hour'][i]
    if (currentHour==20 and currentHour==21 ):
        train_factor['daypart'][i] = 7
    elif (currentHour==18 and currentHour==19):
        train_factor['daypart'][i] = 6
    elif (currentHour>9 and currentHour<18):
        train_factor['daypart'][i] = 5
    elif (currentHour==9):
        train_factor['daypart'][i] = 4
    elif (currentHour==8 ):
        train_factor['daypart'][i] = 3
    elif (currentHour<8):
        train_factor['daypart'][i] = 2
    elif (currentHour>=22 ):
        train_factor['daypart'][i] = 1
          
train_factor['daypart']=train_factor['daypart'].astype('category')

test_factor['daypart'] = 8
for i in range(len(test_factor)) :
    currentHour = test_factor['hour'][i]
    if (currentHour==20 and currentHour==21 ):
        test_factor['daypart'][i] = 7
    elif (currentHour==18 and currentHour==19):
        test_factor['daypart'][i] = 6
    elif (currentHour>9 and currentHour<18) :
        test_factor['daypart'][i] = 5
    elif (currentHour==9):
        test_factor['daypart'][i] = 4
    elif (currentHour==8) :
        test_factor['daypart'][i] = 3
    elif (currentHour<8):
        test_factor['daypart'][i] = 2
    elif (currentHour>=22) :
        test_factor['daypart'][i] = 1
test_factor['daypart']=test_factor['daypart'].astype('category')
```


```python
#create ahot () variable and convert to category (4 category) for both training and test set
train_factor['ahot'] = 4
for i in range(len(train_factor)) :
	currentTemp = train_factor['atemp'][i]
	if (currentTemp>=24.24 and currentTemp<31.06 ):
		train_factor['ahot'][i] = 3
	elif (currentTemp>=16.6 and currentTemp<24.24):
		train_factor['ahot'][i] = 2
	elif ( currentTemp<16.6) :
		train_factor['ahot'][i] = 1

train_factor['ahot']=train_factor['ahot'].astype('category')

test_factor['ahot'] = 4
for i in range(len(test_factor)) :
	currentTemp = test_factor['atemp'][i]
	if (currentTemp>=24.24 and currentTemp<31.06 ):
		test_factor['ahot'][i] = 3
	elif (currentTemp>=16.6 and currentTemp<24.24):
		test_factor['ahot'][i] = 2
	elif (currentTemp<16.6) :
		test_factor['ahot'][i] = 1

test_factor['ahot']=test_factor['ahot'].astype('category')
```


```python
train_factor['temp'].describe()
```




    count    10886.00000
    mean        20.23086
    std          7.79159
    min          0.82000
    25%         13.94000
    50%         20.50000
    75%         26.24000
    max         41.00000
    Name: temp, dtype: float64




```python
#create ahot () variable and convert to category (4 category) for both training and test set
train_factor['hot'] = 4
for i in range(len(train_factor)) :
	currentTemp = train_factor['temp'][i]
	if (currentTemp>=20.5 and currentTemp<26.24 ):
		train_factor['hot'][i] = 3
	elif (currentTemp>=13.94 and currentTemp<20.5):
		train_factor['hot'][i] = 2
	elif ( currentTemp<13.94) :
		train_factor['hot'][i] = 1

train_factor['hot']=train_factor['hot'].astype('category')

test_factor['hot'] = 4
for i in range(len(test_factor)) :
	currentTemp = test_factor['temp'][i]
	if (currentTemp>=20.5 and currentTemp<26.24 ):
		test_factor['hot'][i] = 3
	elif (currentTemp>=13.94 and currentTemp<20.5):
		test_factor['hot'][i] = 2
	elif (currentTemp<13.94) :
		test_factor['hot'][i] = 1

test_factor['hot']=test_factor['hot'].astype('category')
```


```python
train_factor.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>season</th>
      <th>holiday</th>
      <th>workingday</th>
      <th>weather</th>
      <th>temp</th>
      <th>atemp</th>
      <th>humidity</th>
      <th>windspeed</th>
      <th>casual</th>
      <th>registered</th>
      <th>count</th>
      <th>date</th>
      <th>day</th>
      <th>hour</th>
      <th>year</th>
      <th>Sunday</th>
      <th>daypart</th>
      <th>ahot</th>
      <th>hot</th>
    </tr>
    <tr>
      <th>datetime</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2011-01-01 00:00:00</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>9.84</td>
      <td>14.395</td>
      <td>81</td>
      <td>0.0</td>
      <td>3</td>
      <td>13</td>
      <td>16</td>
      <td>2011-01-01 00:00:00</td>
      <td>5</td>
      <td>0</td>
      <td>2011</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2011-01-01 01:00:00</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>9.02</td>
      <td>13.635</td>
      <td>80</td>
      <td>0.0</td>
      <td>8</td>
      <td>32</td>
      <td>40</td>
      <td>2011-01-01 01:00:00</td>
      <td>5</td>
      <td>1</td>
      <td>2011</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2011-01-01 02:00:00</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>9.02</td>
      <td>13.635</td>
      <td>80</td>
      <td>0.0</td>
      <td>5</td>
      <td>27</td>
      <td>32</td>
      <td>2011-01-01 02:00:00</td>
      <td>5</td>
      <td>2</td>
      <td>2011</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2011-01-01 03:00:00</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>9.84</td>
      <td>14.395</td>
      <td>75</td>
      <td>0.0</td>
      <td>3</td>
      <td>10</td>
      <td>13</td>
      <td>2011-01-01 03:00:00</td>
      <td>5</td>
      <td>3</td>
      <td>2011</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2011-01-01 04:00:00</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>9.84</td>
      <td>14.395</td>
      <td>75</td>
      <td>0.0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>2011-01-01 04:00:00</td>
      <td>5</td>
      <td>4</td>
      <td>2011</td>
      <td>0</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
#split into weekday and weekend
train_factor_weekday=train_factor[(train_factor['day']!=5)]
train_factor_weekday=train_factor_weekday[(train_factor_weekday['day']!=6)]

test_factor_weekday=test_factor[(test_factor['day']!=5)]
test_factor_weekday=test_factor_weekday[(test_factor_weekday['day']!=6)]

train_factor_weekend=train_factor[(train_factor['day']!=0)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=1)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=2)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=3)]
train_factor_weekend=train_factor_weekend[(train_factor_weekend['day']!=4)]

test_factor_weekend=test_factor[(test_factor['day']!=0)]
test_factor_weekend=test_factor_weekend[(test_factor_weekend['day']!=1)]
test_factor_weekend=test_factor_weekend[(test_factor_weekend['day']!=2)]
test_factor_weekend=test_factor_weekend[(test_factor_weekend['day']!=3)]
test_factor_weekend=test_factor_weekend[(test_factor_weekend['day']!=4)]
```

```python
#linear regression weekday/weekend 
formula = "count ~ season + workingday + holiday + humidity+ weather + temp + atemp + windspeed + day + hour + year + ahot + hot"

regression_weekday=smf.glm(formula,data=train_factor_weekday,family=sm.families.Poisson(link=sm.families.links.log))
regression_weekday=regression_weekday.fit()
print(regression_weekday.summary2())

test_factor_weekday=test_factor[(test_factor['day']!=5)]
test_factor_weekday=test_factor_weekday[(test_factor_weekday['day']!=6)]

formula = "count ~ season + humidity + weather + temp + atemp + windspeed + day + hour + year + ahot + hot"

regression_weekend=smf.glm(formula,data=train_factor_weekend,family=sm.families.Poisson(link=sm.families.links.log))
regression_weekend=regression_weekend.fit()
print(regression_weekend.summary2())

```

                    Results: Generalized linear model
    =================================================================
    Model:               GLM              AIC:            144956.9543
    Link Function:       log              BIC:            26863.2539 
    Dependent Variable:  count            Log-Likelihood: -72432.    
    Date:                2016-05-24 07:34 LL-Null:        -6.7370e+05
    No. Observations:    7723             Deviance:       95587.     
    Df Model:            45               Pearson chi2:   9.72e+04   
    Df Residuals:        7677             Scale:          1.0000     
    Method:              IRLS                                        
    -----------------------------------------------------------------
                     Coef.  Std.Err.     z     P>|z|   [0.025  0.975]
    -----------------------------------------------------------------
    Intercept        1.8349   0.0076  241.9668 0.0000  1.8200  1.8497
    season[T.2]      0.2994   0.0033   91.2880 0.0000  0.2930  0.3058
    season[T.3]      0.3037   0.0040   76.3823 0.0000  0.2959  0.3115
    season[T.4]      0.4462   0.0029  155.5122 0.0000  0.4406  0.4519
    workingday[T.1]  0.9401   0.0041  229.0417 0.0000  0.9321  0.9481
    holiday[T.1]     0.8947   0.0047  191.5829 0.0000  0.8856  0.9039
    weather[T.2]    -0.0514   0.0021  -24.7919 0.0000 -0.0554 -0.0473
    weather[T.3]    -0.4757   0.0041 -116.1373 0.0000 -0.4837 -0.4676
    weather[T.4]    -0.6109   0.0783   -7.8072 0.0000 -0.7643 -0.4576
    day[T.1]         0.0124   0.0027    4.5817 0.0000  0.0071  0.0177
    day[T.2]         0.0240   0.0027    8.9689 0.0000  0.0188  0.0293
    day[T.3]         0.0453   0.0027   16.8428 0.0000  0.0400  0.0505
    day[T.4]         0.0670   0.0027   24.8757 0.0000  0.0617  0.0722
    day[T.5]         0.0000   0.0000  128.7584 0.0000  0.0000  0.0000
    day[T.6]         0.0000   0.0000   41.4884 0.0000  0.0000  0.0000
    hour[T.1]       -0.7778   0.0162  -47.9403 0.0000 -0.8096 -0.7460
    hour[T.2]       -1.3974   0.0205  -68.0121 0.0000 -1.4377 -1.3571
    hour[T.3]       -1.9828   0.0269  -73.8153 0.0000 -2.0354 -1.9301
    hour[T.4]       -1.9108   0.0260  -73.6111 0.0000 -1.9617 -1.8600
    hour[T.5]       -0.3999   0.0145  -27.5717 0.0000 -0.4284 -0.3715
    hour[T.6]        1.0426   0.0106   98.1702 0.0000  1.0217  1.0634
    hour[T.7]        2.0693   0.0096  214.9871 0.0000  2.0504  2.0882
    hour[T.8]        2.5448   0.0094  270.8807 0.0000  2.5264  2.5632
    hour[T.9]        1.8490   0.0097  190.0723 0.0000  1.8299  1.8681
    hour[T.10]       1.2597   0.0102  123.1782 0.0000  1.2396  1.2797
    hour[T.11]       1.3841   0.0101  137.2628 0.0000  1.3643  1.4039
    hour[T.12]       1.5973   0.0099  161.1837 0.0000  1.5779  1.6168
    hour[T.13]       1.5629   0.0099  157.2035 0.0000  1.5434  1.5824
    hour[T.14]       1.4687   0.0100  146.4672 0.0000  1.4491  1.4884
    hour[T.15]       1.5521   0.0100  155.7479 0.0000  1.5325  1.5716
    hour[T.16]       1.9259   0.0097  198.1730 0.0000  1.9068  1.9449
    hour[T.17]       2.5232   0.0095  266.7817 0.0000  2.5046  2.5417
    hour[T.18]       2.4748   0.0095  261.6999 0.0000  2.4562  2.4933
    hour[T.19]       2.1374   0.0096  223.5650 0.0000  2.1186  2.1561
    hour[T.20]       1.8204   0.0097  187.2119 0.0000  1.8014  1.8395
    hour[T.21]       1.5430   0.0099  155.4294 0.0000  1.5236  1.5625
    hour[T.22]       1.2714   0.0102  124.6875 0.0000  1.2515  1.2914
    hour[T.23]       0.8483   0.0108   78.5672 0.0000  0.8271  0.8695
    year[T.2012]     0.4886   0.0017  284.7171 0.0000  0.4852  0.4919
    ahot[T.2]        0.0932   0.0057   16.4482 0.0000  0.0821  0.1043
    ahot[T.3]       -0.5025   0.0237  -21.2186 0.0000 -0.5489 -0.4561
    ahot[T.4]       -0.4448   0.0249  -17.8434 0.0000 -0.4936 -0.3959
    hot[T.2]         0.0635   0.0055   11.5408 0.0000  0.0527  0.0743
    hot[T.3]         0.7969   0.0233   34.1276 0.0000  0.7511  0.8426
    hot[T.4]         0.7989   0.0248   32.1505 0.0000  0.7502  0.8476
    humidity        -0.0018   0.0001  -28.4746 0.0000 -0.0019 -0.0017
    temp            -0.0135   0.0010  -12.8878 0.0000 -0.0156 -0.0115
    atemp            0.0217   0.0010   22.6215 0.0000  0.0198  0.0236
    windspeed       -0.0012   0.0001  -10.8193 0.0000 -0.0014 -0.0010
    =================================================================
    
                   Results: Generalized linear model
    ================================================================
    Model:              GLM              AIC:            57542.7737 
    Link Function:      log              BIC:            11924.2519 
    Dependent Variable: count            Log-Likelihood: -28731.    
    Date:               2016-05-24 07:34 LL-Null:        -2.6131e+05
    No. Observations:   3163             Deviance:       37093.     
    Df Model:           39               Pearson chi2:   3.64e+04   
    Df Residuals:       3123             Scale:          1.0000     
    Method:             IRLS                                        
    ----------------------------------------------------------------
                     Coef.  Std.Err.    z     P>|z|   [0.025  0.975]
    ----------------------------------------------------------------
    Intercept        2.5880   0.0092 281.2308 0.0000  2.5700  2.6061
    season[T.2]      0.2836   0.0056  50.6644 0.0000  0.2726  0.2945
    season[T.3]      0.2547   0.0066  38.4282 0.0000  0.2417  0.2677
    season[T.4]      0.4121   0.0046  88.9643 0.0000  0.4030  0.4212
    weather[T.2]    -0.0847   0.0036 -23.8557 0.0000 -0.0917 -0.0778
    weather[T.3]    -0.4457   0.0072 -61.9561 0.0000 -0.4598 -0.4316
    weather[T.4]    -0.0000   0.0000  -4.5971 0.0000 -0.0000 -0.0000
    day[T.1]        -0.0000   0.0000  -5.1104 0.0000 -0.0000 -0.0000
    day[T.2]         0.0000   0.0000 126.6602 0.0000  0.0000  0.0000
    day[T.3]         0.0000   0.0000 171.7424 0.0000  0.0000  0.0000
    day[T.4]        -0.0000   0.0000 -88.4113 0.0000 -0.0000 -0.0000
    day[T.5]         1.3466   0.0047 287.7944 0.0000  1.3375  1.3558
    day[T.6]         1.2414   0.0049 253.7715 0.0000  1.2318  1.2510
    hour[T.1]       -0.2355   0.0134 -17.5816 0.0000 -0.2618 -0.2093
    hour[T.2]       -0.5193   0.0146 -35.4489 0.0000 -0.5480 -0.4906
    hour[T.3]       -1.2503   0.0190 -65.7493 0.0000 -1.2876 -1.2130
    hour[T.4]       -2.3548   0.0309 -76.2636 0.0000 -2.4153 -2.2942
    hour[T.5]       -2.3378   0.0307 -76.1880 0.0000 -2.3980 -2.2777
    hour[T.6]       -1.6055   0.0223 -72.0334 0.0000 -1.6491 -1.5618
    hour[T.7]       -0.7949   0.0162 -48.9713 0.0000 -0.8267 -0.7631
    hour[T.8]        0.0643   0.0124   5.1938 0.0000  0.0401  0.0886
    hour[T.9]        0.5758   0.0110  52.1744 0.0000  0.5542  0.5975
    hour[T.10]       0.9577   0.0104  92.4353 0.0000  0.9374  0.9780
    hour[T.11]       1.1442   0.0101 112.8066 0.0000  1.1243  1.1641
    hour[T.12]       1.2825   0.0101 127.5457 0.0000  1.2628  1.3022
    hour[T.13]       1.2841   0.0101 127.2420 0.0000  1.2643  1.3038
    hour[T.14]       1.2592   0.0102 123.7529 0.0000  1.2393  1.2792
    hour[T.15]       1.2527   0.0102 122.9589 0.0000  1.2327  1.2726
    hour[T.16]       1.2179   0.0102 119.3362 0.0000  1.1979  1.2380
    hour[T.17]       1.1513   0.0103 112.0713 0.0000  1.1312  1.1715
    hour[T.18]       0.9889   0.0104  95.1633 0.0000  0.9685  1.0093
    hour[T.19]       0.8143   0.0106  77.1004 0.0000  0.7936  0.8350
    hour[T.20]       0.5531   0.0110  50.2450 0.0000  0.5315  0.5747
    hour[T.21]       0.3463   0.0114  30.2963 0.0000  0.3239  0.3687
    hour[T.22]       0.1871   0.0119  15.7760 0.0000  0.1638  0.2103
    hour[T.23]      -0.0517   0.0127  -4.0844 0.0000 -0.0765 -0.0269
    year[T.2012]     0.4243   0.0027 155.1919 0.0000  0.4190  0.4297
    ahot[T.2]        0.1325   0.0101  13.0607 0.0000  0.1126  0.1524
    ahot[T.3]        0.3810   0.0054  70.9426 0.0000  0.3705  0.3916
    ahot[T.4]        0.4477   0.0071  63.2337 0.0000  0.4338  0.4616
    hot[T.2]         0.2274   0.0096  23.6423 0.0000  0.2086  0.2463
    hot[T.3]         0.3740   0.0056  66.6990 0.0000  0.3631  0.3850
    hot[T.4]         0.4547   0.0070  64.8650 0.0000  0.4409  0.4684
    humidity        -0.0018   0.0001 -18.2026 0.0000 -0.0020 -0.0016
    temp            -0.0287   0.0017 -16.9220 0.0000 -0.0320 -0.0253
    atemp            0.0194   0.0015  12.5319 0.0000  0.0164  0.0224
    windspeed       -0.0033   0.0002 -18.9181 0.0000 -0.0036 -0.0029
    ================================================================
    

```python
#prediction weekday/weekend
prediction_weekday=regression_weekday.predict(test_factor_weekday)
prediction_weekday[prediction_weekday<0]=0 # bike demand is positive

prediction_weekend=regression_weekend.predict(test_factor_weekend)
prediction_weekend[prediction_weekend<0]=0 # bike demand is positive


```

```python
#convert to dataframe
prediction_weekend=pd.DataFrame(prediction_weekend)
prediction_weekend.columns=['count']
prediction_weekend["datetime"]=test_factor_weekend.index.values
prediction_weekend = prediction_weekend.set_index("datetime")

prediction_weekday=pd.DataFrame(prediction_weekday)
prediction_weekday.columns=['count']
prediction_weekday["datetime"]=test_factor_weekday.index.values
prediction_weekday = prediction_weekday.set_index("datetime")
```
```python
#write prediction for weekend/weekday
prediction=prediction_weekend;
prediction=prediction.append(prediction_weekday)
prediction.sort_index()
```
```python
import matplotlib.pyplot as plt
prediction['day']=test_factor['day']
prediction['hour']=test_factor['hour']
```


```python
plt.scatter(prediction['day'],prediction["count"].as_matrix())
plt.xlabel('day')
plt.ylabel('count prediction')
plt.title('Count predict on testing set')
plt.axis([-1,8,-100,1100])
plt.xticks([0,1,2,3,4,5,6],['M','T','W','T','F','S','S'])
plt.grid(True)
plt.show()
```


```python
plt.scatter(prediction['hour'],prediction["count"].as_matrix())
plt.xlabel('hour')
plt.ylabel('count prediction')
plt.title('Count predict on testing set')
plt.axis([-1,25,-100,1100])
plt.grid(True)
plt.show()
```
```python
plt.scatter(train_factor["day"],train_factor["count"].as_matrix())
plt.xlabel('day')
plt.ylabel('count observed')
plt.title('Count observed on training set')
plt.axis([-1,8,-100,1100])
plt.xticks([0,1,2,3,4,5,6],['M','T','W','T','F','S','S'])
plt.grid(True)
plt.show()
```


```python
plt.scatter(train_factor["hour"],train_factor["count"].as_matrix())
plt.xlabel('hour')
plt.ylabel('count observed')
plt.title('Count observed on training set')
plt.axis([-1,25,-100,1100])
plt.grid(True)
plt.show()
```
```python
#write the submission
prediction.to_csv("Résultats/regressionPoissonFactorWeekend_Weekday.csv")

```
```python
from sklearn.linear_model import LogisticRegression
import numpy as np
```


```python
lr=LogisticRegression()
```


```python
#algorithme de sélection de var.
from sklearn.feature_selection import RFE
selecteur=RFE(estimator=lr)
```


```python
train_factor.head()
```


```python
data_X_weekday=train_factor_weekday.drop(["casual","registered","count","date"],1)
data_Y_weekday=train_factor_weekday['count']
data_Y_weekday=data_Y_weekday.as_matrix()
data_X_weekday=data_X_weekday.as_matrix()

data_X_weekend=train_factor_weekend.drop(["casual","registered","count","date"],1)
data_Y_weekend=train_factor_weekend['count']
data_Y_weekend=data_Y_weekend.as_matrix()
data_X_weekend=data_X_weekend.as_matrix()
```


```python
predictor_weekday=selecteur.fit(data_X_weekday,data_Y_weekday)
predictor_weekend=selecteur.fit(data_X_weekend,data_Y_weekend)
```


```python
print(predictor_weekday)
print(predictor_weekend)
```

    RFE(estimator=LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False),
      estimator_params=None, n_features_to_select=None, step=1, verbose=0)
    RFE(estimator=LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False),
      estimator_params=None, n_features_to_select=None, step=1, verbose=0)



```python
print(train_factor_weekday.drop(["casual","registered","count","date"],1).head())
print(predictor_weekday.support_)
print(predictor_weekday.ranking_)
print(predictor_weekend.support_)
print(predictor_weekend.ranking_)
```
![score finale](https://raw.githubusercontent.com/matthiasbe/projetspe/master/bikeshare/R%C3%A9sultats/Avec_Graphiques/scoreRegressionPoissonFactgorFinal.png)
