[Retour au sommaire d'Expedia](expedia_sommaire.md)

## Introduction :

[Source](http://www.analyticsvidhya.com/blog/2015/09/naive-bayes-explained/)

L' algorithme de Naïve Bayes fait partie de la famille des algorithmes de classification. Il s'appuye sur les probabilités a priori des évènements pour déterminer la probabilité avec laquelle l'un d'entre eux va se réaliser; pour cela, il utilise le [théorème de Bayes](#théorème-de-bayes-) et une hypothèse d'indépendance entre les variables.

## Avantages de cet algorithme :

* simplicité : les hypothèses probabilistes sont simples à vérifier et l'algorithme se comprend assez facilement
* convergence : peu de données en entrée sont nécessaires pour fournir un modèle satisfaisant
* performance : malgré sa simplicité, il est réputé pour être plus efficace que certaines algorithmes de classification plus complexes

## Théorème de Bayes :

<img src="http://www.analyticsvidhya.com/wp-content/uploads/2015/09/Bayes_rule-300x172.png" width="300" height="180" />

### Ce qu'on observe :
* P(c) : la probabilité d'avoir la classe c
* P(x) : la probabilité d'avoir les attributs x
* P(x|c) : la probabilité d'observer l'attribut x, sachant qu'on a un objet de classe c

### Ce qu'on souhaite déterminer :
* P(c|x) : la probabilité d'avoir la classe c, étant donné les attributs x


## Comment ça marche :

L'algorithme se décompose en plusieurs étapes :

1. Convertir les données en une table de fréquence
2. Faire la table de probabilité correspondante 
3. Se servir de la formule de Bayes pour trouver P(c|x) à partir des observations de P(c), P(x) et P(x|c)

Par exemple avec :


<img src="http://www.analyticsvidhya.com/wp-content/uploads/2015/08/Bayes_41.png" width="600" height="250" />


* P(Yes|Sunny) = P(Sunny|Yes) * P(Yes) / P (Sunny)
* P(Sunny|Yes) = 3/9 = 0.33,
* P(Sunny) = 5/14 = 0.36,
* P(Yes)= 9/14 = 0.64

D'où : 

P (Yes|Sunny) = 0.33 * 0.64 / 0.36 = 0.60

On privilégiera donc la réponse Yes (plutôt que No) quand on a Sunny car :

P(No|Sunny) = 1 - P(Yes|Sunny) = 0.40 < 0.60
