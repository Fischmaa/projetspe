# Algorithmes retenus

[Retour au sommaire d'Expedia](expedia_sommaire.md)

## Introduction

- TODO

## Plan

1. [Gradient Boosting](#gradient-boosting)
2. [Naive Bayes](#naive-bayes)

## Gradient Boosting

Les explications données dans cette partie sont directement issus de la [documentation anglaise de XGBoost](https://xgboost.readthedocs.io/en/latest/model.html).

En utilisant la notation "θ" pour représenter les paramètres de notre modèle prédictif, le Gradient Boosting se résume à une optimisation des choix réalisés dans les arbres de décision. Pour celà, on introduit une fonction objectif :

![](http://nsa37.casimages.com/img/2016/05/30/160530121135280376.png)

* L : l' erreur d'apprentissage, généralement décroissante avec la complexité du modèle
* Ω : le terme de régularition, croissant avec la complexité du modèle, qui permet d'éviter l'overfitting causé par la diminution de l'erreur d'apprentissage

Dans le cas de XGBoost, la fonction Ω est arbitrairement définie pour chaque problème par une fonction de cette forme où T est le nombre de feuilles de l'arbre, γ et λ des constantes :

![](http://nsa37.casimages.com/img/2016/05/30/160530122016216810.png)

## Naive Bayes

- TODO
