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
library(MASS)
library(lubridate)
 
train <- read.csv("./sources/train.csv")
# traduction de la date en jour, sous forme d'entier entre 1 et 7 :  
train$date<-wday(ymd_hms(train$datetime), label=TRUE)
train$date<-as.integer(train$date)

# supprimer la date "String" pour avoir une matrice de corrélation et essayer de voir le lien entre les 
# différentes variables !
train<-train[,-c(1)]
cor(train)

# Regression linéaire (on retire les variables registred et casual):
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



#### Régression linéaire avec données discrètes
```R

```

#### Régression linéaire avec données discrètes et découpage du problème
```R

```

#### Régression linéaire avec données discrètes, découpage du problème et modélisation de Poisson
```R

```

### Python

## Random Forest

## Remarques

### Choix du modèle - représentation des données
Représentation PC ?
