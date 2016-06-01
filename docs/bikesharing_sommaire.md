# 1er problème : Bikesharing problem

**Objectif :** Soumission d'une solution au problème kaggle : Bike Sharing Demand

[Lien vers le challenge](https://www.kaggle.com/c/bike-sharing-demand)

**Résumé du problème :** On possède les données de circulation des vélos du type des *velib* parisiens entre différentes stations ainsi que les données météo associées. On cherche à prédire dans quelles quantitée sont loués les vélos, dans le système de location de vélo de la ville de Washigton.

**Données disponibles :** Données sur deux ans. Les 19 premiers jours de chaque mois constituent les `training set`, il s'agit des données permettant de calibrer le classificateur. Le reste du mois correspond aux données pour tester le classificateur.

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


## Sommaire

1. [Regression linéaire](bikesharing_1_linear_regression.md)
2. [Random forest](bikesharing_2_random_forest.md)

## Conclusion

Après avoir exploré le forum du sujet [Bike Sharing](https://www.kaggle.com/c/bike-sharing-demand/scripts) et lu l'article de Trevor Stephens sur le sujet Kaggle concernant les victimes du [Titanic](http://trevorstephens.com/post/73770963794/titanic-getting-started-with-r-part-5-random), nous avons voulu voir les résultats atteignables avec la méthode de Random Forest. Nous avons donc utilisé le code de [Ben Hamner](https://www.kaggle.com/benhamner/bike-sharing-demand/random-forest-benchmark) et obtenu sur Kaggle une erreur de 0.66, soit presque 50% moins bien que notre régression de Poisson fine, qui donne un résultat de 0.44051. Malgré la complexité du modèle Random Forest, nous avons donc découvert qu'avec une regression de Poisson il était possible de faire un score bien meilleur. Ainsi, l'expérience nous a démontré l'importance de bien traiter les données (feature engineering) et de chercher à leur donner le plus de sens possible avant de se lancer dans des processus complexes.

![évolution du score](https://raw.githubusercontent.com/matthiasbe/projetspe/master/docs/images/scoreBikeSharing.png)
