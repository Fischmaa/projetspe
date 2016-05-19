ENSIMAG - Projet de spé 2016 - kaggle challenge

# Objectif du projet

Nous avons décider de résoudres différents projets kaggle afin de comprendre le principe de prédiction sur un échantillon de donnée quand on possède un jeu de données d'entrainement. Cette étude s'inscrit dans le cursus de l'ENSIMAG en constituant une application pour les cours d'option de fouille de donnée et de système intelligents.

# 1er problème : Bikesharing problem

**Objectif :** Soumission d'une solution au problème kaggle : Bike Sharing Demand

[Lien vers le challenge](https://www.kaggle.com/c/bike-sharing-demand)

**Résumé du problème :** On possède les données de circulation des vélos du type des *velib* parisiens entre différentes stations ainsi que les données météo associées. On cherche à prédire dans quelles quantitée sont loués les vélos, dans le système de location de vélo de la ville de Washigton.

**Données disponible :** Données sur deux ans. Les 19 premiers jours de chaque mois constituent les `training set`, il s'agit des données permettant de calibrer le classificateur. Le reste du mois correspond aux données pour tester le classificateur.

On possède une jeu de données contenant des informations différentes selon le types de données :

*Entrainement (train.csv) et Test (test.csv)*

* Jour et heure
* Saison
* Vacances, semaine ou weekend
* Temps qu'il fait
* Températures : ressentie et réelle
* Humidité
* Vitesse du vent

*Entrainement uniquement*

* Nombre de vélos loués par des inscrits
* Nombre de vélos loués par des non-inscrits
* Nombre de vélos loués au total




## Introduction

Nous avons mis en place différents modèles prédictifs, en abordant le problème de manière différente à chaque itération. Nous allons détailler les différents raisonnements suivis, puis nous comparerons les résultats.

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

TODO

## Random Forest et Feature Engineering

Après avoir exploré le forum du sujet [Bike Sharing](https://www.kaggle.com/c/bike-sharing-demand/scripts) et lu l'article sur le [Titanic](http://trevorstephens.com/post/73770963794/titanic-getting-started-with-r-part-5-random), nous avons voulu voir les résultats atteignables avec la méthode de Random Forest. Nous avons donc utilisé le code de [Ben Hamner](https://www.kaggle.com/benhamner/bike-sharing-demand/random-forest-benchmark) et obtenu sur Kaggle une erreur de 0.59, soit seulement 13% de mieux que notre régression linéaire. Malgré la complexité du modèle Random Forest, nous avons découvert qu'avec une [regression linéaire plus affinée](http://brandonharris.io/kaggle-bike-sharing/) il était possible de faire un score encore meilleur (~0.49). Ainsi, l'expérience nous a démontré l'importance de bien traiter le données et de chercher à leur donner le plus de sens possible avant de se lancer dans des processus complexes.

## Remarques

### Choix du modèle - représentation des données
TODO - Représentation PC ?
