
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
![Gradient Boosting Tunning](http://www.analyticsvidhya.com/blog/2016/02/complete-guide-parameter-tuning-gradient-boosting-gbm-python/)

Il y a trois types de paramètres sur lesquels on peut agir en faisant du gradient boosting : 
* paramètres spécifiques aux arbres de décision
* paramètres de boosting 
* autres paramètres

Attention : les noms de paramètres sont ceux de la librairie scikit-learn mais les concepts restent les mêmes.
### Paramètres spécifiques aux arbres de décision

![Abre de décision](http://www.analyticsvidhya.com/wp-content/uploads/2016/02/tree-infographic.png)

#### min_samples_split
Correspond au nombre minimum d'observations requises dans un noeud pour le spliter.
Ce paramètre permet de controler l'over-fitting en augmentant ce nombre minimum, toutefois si ce nombre est trop élévé il y a un risque d' under-fitting.
#### min_samples_leaf
Définit le nombre minimum d'observations requises dans une feuille.
Permet aussi de contrôler l'over-fitting (comme min_samples_split)
Généralement de petites valeurs seront utilisées dans le cas où les classes à prédire ne sont pas équilibrés.
#### max_depth
Profondeur maximale des arbres de décision.
Permet de gérer l'over-fitting : le risque d'over-fitting augment avec la profondeur des arbres.
#### max_leaf_nodes
Nombre maximum de feuilles dans un arbre.
Puisque les arbres décisions sont des arbres binaires, ce paramètre est incompatible avec max_depth
#### max_features 
Nombre maximum de variables à considérer pour la recherche (aléatoirement) du meilleur split.
Règle bateau : la racine carré du nombre total de variables est un bon départ et on peut aller jusqu'à 30%-40% du nombre total de variables.
Un valeur plus grande peut potentiellement conduire à de l'over-fitting mais cela dépend des cas.

### Paramètres de boosting

#### learning_rate
Détermine l'impact de chaque arbre sur le résultat final, ce paramètre contrôle les variations des poids associés aux arbres.
Les faibles valeurs sont généralement préférés puisqu'elle rende le modèle robuste aux caractéristiques spécifiques de chaque arbre ce qui permet de mieux généraliser.
Des faibles valeurs nécessitent un plus grand nombre d'abres ce qui peut être couteux.
#### n_estimators
Nombre d'arbres utilisés.
Un trop grand nombre peut conduire à de l'over-fitting même si le gradient boosting traîte bien un grand nombre d'arbres.
#### subsample
Fraction des observations à séléctionner (aléatoirement) pour chaque arbre.
Valeur typique de ~0.8 marche bien mais peut être amélioré.

### Autres paramètres

#### loss
Correspond à la fonction à minimiser à chaque split.
La valeur par défaut devrait marcher correctement mais il est possible de la modifier intélligemment.

#### random_state 
Graine du générateur de nombre aléatoire.
C'est un paramètre important pour comparer différents modèles : il faut utiliser la même graine.



