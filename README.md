ENSIMAG - Projet de spé 2016 - kaggle challenge

# Objectif du projet

Nous avons décider de résoudres différents projets kaggle afin de comprendre le principe de prédiction sur un échantillon de donnée quand on possède un jeu de données d'entrainement. Cette étude s'inscrit dans le cursus de l'ENSIMAG en constituant une application pour les cours d'option de fouille de donnée et de système intelligents.

# 1er problème : Bikesharing problem

**Objectif :** Soumission d'une solution au problème kaggle : Bike Sharing Demand

[Lien vers le challenge](https://www.kaggle.com/c/bike-sharing-demand)

**Résumé du problème :** On possède les données de circulation des vélo du type des *velib* parisiens entre différentes stations ainsi que les données météo associées. On cherche à prédire dans quelles vélo sont louer les vélos. Le problème est situé dans le système de location de vélo de la ville de Washigton.

**Données disponible :** Données sur deux ans. Les 19 premiers jours de chaque mois constituent les `training set`, il s'agit des données permettant de calibrer le classificateur. Le reste du mois correspond au données pour tester le classificateur.

On possède une jeu de données pour chaque heure de la journée  :

*Entrainement et tests*

* Jour et heure
* Saison
* Vacances, semaine ou weekend
* Temps qu'il fait
* Températures ressentie et réelle
* L'humidité
* Vitesse du vent

*Entrainement uniquement*

* Nombre de vélos loués par des inscrits
* Nombre de vélos loués par des non-inscrits
* Nombre de vélos loués au total




## Introduction

Nous effectué les prédictions demandées avec différents algorithmes. Nous allons détailler les différentes méthode employées puis nous comparerons les résultats.

## Regression linéaire

Pour une première approche de prédiction on utilise un algorithme de regression linéaire.

### R

```R
train <- read.csv("~/Bureau/kaggle/train.csv")
train$date<-wday(ymd_hms(train$datetime), label=TRUE)
train$date<-as.integer(train$date)
# supprimer la date pour avoir une matrice de corrélation et essayer de voir le lien entre les 
# différentes variables !
train<-train[,-c(1)]
cor(train)
# On va essayer de faire une regression linéaire :
mylm<-lm(count~.,data=train)
stepAIC(mylm)
# On obtient :
# (Intercept)         temp        atemp     humidity    windspeed       casual   registered  
#  -4.816e-13    7.518e-15   -1.698e-14    3.528e-15   -2.835e-15    1.000e+00    1.000e+00  
# RQ : ça craint ... On va plutot faire en fonction de l'heure et regarder si on est en WE ou pas
```

### Python


