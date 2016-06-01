
[Retour au sommaire d'Expedia](expedia_sommaire.md)

## Boosting Algorithms
![Introduction to Boosting Algorithms](http://www.analyticsvidhya.com/blog/2015/11/quick-introduction-boosting-algorithms-machine-learning/)

Boosting : famille d'algorithmes d'optimisation de variables. L'idée est de transformer des weak learner en strong learner.

Weak learner : variables qui ne permettent pas de classifier correctement.
Strong learner : combinaison de weak learner pour améliorer la classification.

Les algorithmes de boosting sont itératifs et à chaque étape un weak learner est utilisé pour assigner des poids sur les différentes observations classées dans une mauvaise catégorie, de façon à ce qu'à la prochaine itération le weak learner suivant classe en priorité ces observations avec un poids plus important.
Finalement, on combine tous les résultats pour créer un strong learner à partir de toutes les itérations.

Il y a différents algorithmes de boosting : 
* AdaBoost (Adaptive Boosting)
* Gradient Tree Boosting 
* XGBoost (Extreme Gradient Boost)

## Gradient Boosting

Il y a trois types de paramètres sur lesquels on peut agir en faisant du gradient boosting : 
* paramètres spécifiques aux arbres de décision
* paramètres de boosting 
* autres paramètres

### Paramètres spécifiques aux arbres de décision

![Abre de décision](http://www.analyticsvidhya.com/wp-content/uploads/2016/02/tree-infographic.png)

