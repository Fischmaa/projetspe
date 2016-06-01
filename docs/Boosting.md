
[Retour au sommaire d'Expedia](expedia_sommaire.md)

Sommaire : 
* [Boosting Algorithms](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#boosting-algorithms) 
* [Gradient Boosting](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#gradient-boosting)
  * [Arbres de décision](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#param%C3%A8tres-sp%C3%A9cifiques-aux-arbres-de-d%C3%A9cision)
  * [Boosting](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#param%C3%A8tres-de-boosting)
  * [Autres](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#autres-param%C3%A8tres)
* [XGBoost](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#xgboost)
  * [Avantages](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#avantage)
  * [Paramètres](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#param%C3%A8tres-de-xgboost)
    * [Généraux](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#param%C3%A8tres-g%C3%A9n%C3%A9raux)
    * [Boosting](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#param%C3%A8tres-de-boosting--pour-les-arbres-de-d%C3%A9cisions)
    * [Apprentissage](https://github.com/matthiasbe/projetspe/blob/master/docs/Boosting.md#param%C3%A8tres-dapprentissage)


# Boosting Algorithms
![Introduction to Boosting Algorithms](http://www.analyticsvidhya.com/blog/2015/11/quick-introduction-boosting-algorithms-machine-learning/)

*Boosting* : famille d'algorithmes d'optimisation de variables. L'idée est de transformer des weak learner en strong learner.

*Weak learner* : variables qui ne permettent pas de classifier correctement.
*Strong learner* : combinaison de weak learner pour améliorer la classification.

Les algorithmes de boosting sont itératifs et à chaque étape un weak learner est utilisé pour assigner des poids sur les différentes observations classées dans une mauvaise catégorie, de façon à ce qu'à la prochaine itération le weak learner suivant classe en priorité ces observations avec un poids plus important.
Finalement, on combine tous les résultats pour créer un strong learner à partir de toutes les itérations.

Il y a différents algorithmes de boosting : 
* AdaBoost (Adaptive Boosting)
* Gradient Tree Boosting 
* XGBoost (Extreme Gradient Boost)

# Gradient Boosting
![Gradient Boosting Tunning](http://www.analyticsvidhya.com/blog/2016/02/complete-guide-parameter-tuning-gradient-boosting-gbm-python/)

Il y a trois types de paramètres sur lesquels on peut agir en faisant du gradient boosting : 
* paramètres spécifiques aux arbres de décision
* paramètres de boosting 
* autres paramètres

Attention : les noms de paramètres sont ceux de la librairie scikit-learn mais les concepts restent les mêmes.
### Paramètres spécifiques aux arbres de décision

![Abre de décision](http://www.analyticsvidhya.com/wp-content/uploads/2016/02/tree-infographic.png)

* **min_samples_split** :
Correspond au nombre minimum d'observations requises dans un noeud pour le spliter.
Ce paramètre permet de controler l'over-fitting en augmentant ce nombre minimum, toutefois si ce nombre est trop élévé il y a un risque d' under-fitting.

* **min_samples_leaf** :
Définit le nombre minimum d'observations requises dans une feuille.
Permet aussi de contrôler l'over-fitting (comme min_samples_split)
Généralement de petites valeurs seront utilisées dans le cas où les classes à prédire ne sont pas équilibrés.

* **max_depth** :
Profondeur maximale des arbres de décision.
Permet de gérer l'over-fitting : le risque d'over-fitting augment avec la profondeur des arbres.

* **max_leaf_nodes** :
Nombre maximum de feuilles dans un arbre.
Puisque les arbres décisions sont des arbres binaires, ce paramètre est incompatible avec max_depth

* **max_features**  :
Nombre maximum de variables (colonnes) à considérer pour la recherche (aléatoirement) du meilleur split.
Règle bateau : la racine carré du nombre total de variables est un bon départ et on peut aller jusqu'à 30%-40% du nombre total de variables.
Un valeur plus grande peut potentiellement conduire à de l'over-fitting mais cela dépend des cas.

### Paramètres de boosting

* **learning_rate** :
Détermine l'impact de chaque arbre sur le résultat final, ce paramètre contrôle les variations des poids associés aux arbres.
Les faibles valeurs sont généralement préférés puisqu'elle rende le modèle robuste aux caractéristiques spécifiques de chaque arbre ce qui permet de mieux généraliser.
Des faibles valeurs nécessitent un plus grand nombre d'abres ce qui peut être couteux.

* **n_estimators** :
Nombre d'arbres utilisés.
Un trop grand nombre peut conduire à de l'over-fitting même si le gradient boosting traîte bien un grand nombre d'arbres.

* **subsample** :
Fraction des observations à séléctionner (aléatoirement) pour chaque arbre.
Valeur typique de ~0.8 marche bien mais peut être amélioré.

### Autres paramètres

* **loss** :
Correspond à la fonction erreur à minimiser à chaque split.
La valeur par défaut devrait marcher correctement mais il est possible de la modifier intélligemment.

* **random_state** :
Graine du générateur de nombre aléatoire.
C'est un paramètre important pour comparer différents modèles : il faut utiliser la même graine.

# XGBoost

## Avantage 

* **Regularisation** : 
Inexistant dans le Gradient Boosting, on peut ajouter un terme de régularisation qui permet de lutter contre l'over-fitting.
[Plus d'explication](http://www.analyticsvidhya.com/blog/2015/02/avoid-over-fitting-regularization/)

* **Parralélisation** :
Accélère considérablement les calculs par rapport au Gradient Boosting.

* **Flexibilité** :
Permet de gérer les critères d'évaluations et les fonctions objectives du modèle.

* **Données manquantes** :
XGBoost peut gérer les données manquantes.

* **Elagage des arbres de décision** :
Contrairement au Gradient Boosting qui est un algorithme glouton, XGBoost fait des recherches intélligentes dans le parcours des arbres pour supprimer des noeuds inutiles par exemples.

* **Cross-Validation** :
Permet de faire une cross-validation à chaque itération et permet donc de booster les paramètres en une seule fois (contrairement au Gradient Boosting).

* **Reprendre un modèle déjà existant** : 

Permet de reprendre un modèle XGBoost depuis ca dernière itération.

[Plus d'informations](http://xgboost.readthedocs.io/en/latest/model.html)

## Paramètres de XGBoost 

Il y a trois types de paramètres sur lesquels on peut agir en utilisant XGBoost : 
* paramètres généraux
* paramètres de boosting 
* paramètres d'apprentissage

### Paramètres généraux 

* **booster[default=gbtree]** : Permet de choisir le modèle à utiliser.
  * gbtree : modèle d'abre de décision
  * gblinear : modèle linéaire
 
* **nthread[default to maximum number of threads availabe if not set]** 

### Paramètres de boosting ( pour les arbres de décisions)
Certaines analogies sont faites avec l'étude des [paramètres pour le Gradient Boosting.](https://github.com/matthiasbe/projetspe/blob/master/docs/XGBoostTunning.md#param%C3%A8tres-de-boosting)

* **eta[default=0.3]** : 
Analogue au learning rate pour le Gradient Boosting.
Valeur finale courante : 0.01 à 0.2.

* **min_child_weight[default=1]** :
Définit le minimum pour la somme des poids des observations pour un noeud enfant.
Presque similaire au mind_child_leaf poiur le Gradient Boosting mais prend en compte la somme des poids plutôt que le nombre d'observations.

* **max_depth[default=6]** : 
Profondeur maximum pour un arbre, comme pour le Gradient Boosting : permet de controler l'over-fitting.
Les valeurs courantes sont : 3 à 10.

* **max_leaf_nodes** : 
Nombre maximum de feuilles dans un arbre, comme pour le Gradient Boosting.
Incompatible avec max_depth.

* **gamme[default=0]** : 
Un noeud est diviser (split) seulement quand le résultat de la division améliore le résultat de la fonction erreur (loss) à minimiser.
gamme indique le minimum d'amélioration requis pour faire la division d'un noeud.

* **subsample[default=1]** : 
Comme le subsample du Gradient Boosting.
Valeur courante : 0.5 à 1.

* **colsample_bytree[default=1]** : 
Analogue au max_features du Gradient Boosting.
Valeur courante : 0.5 à 1.

* **lambda[default=1]** : 
Terme de régulation de classe L2, des poids.
Pas très utilisé mais devrait aider à réduire l'over-fitting.

* **alpha[default=0]** : 
Terme de régulation de classe L1, des poids.
A utiliser dans le cas de très grandes dimension pour améliorer la vitesse d'execution.

* **scale_pos_weight[defaut=1]** : 
Un valeur plus grande que 0 devrait, dans le cas de classes non équilibrées, améliorer la vitesse de convergence.

### Paramètres d'apprentissage

Ces paramètres permettent de définir la fonction objectif et la métrique pour évaluer les performances.

* **objective[default=reg:linear]** : Définit la fonction erreur (loss) à minimiser.
 * **binary:logistic** : regression logistique pour la classification binaire, retourne les probabilités prédites (pas les classes).
 * **multi:softmax** : classification pour des classes multiples en utilisant comme fonction objectif : [softmax](https://en.wikipedia.org/wiki/Softmax_function)
  * **num_class** : il faut alors définir le nombre de classes.
 * **multi:softprob** : comme softmax, mais retourne les probabilités prédites pour chaque donnée de chaque classe.
 
* **eval_metric[default according to objective]** : 
Correspond à la métrique utilisée pour la validation de performances. Les valeurs par défaut sont *rmse* pour les regressions et *error* pour la classification.
Les valeurs courantes sont : 
   * **rmse** : root mean square error
   * **mae** : mean absolute error
   * **logloss** : negative log-likelihood
   * **error** : valeur d'erreur pour classification binaire (seuil à 0.5)
   * **merror** : valeur d'erreur pour la classification multi classes.
   * **mlogloss** : multiclass logloss
   * **auc** : area under the curve

* **seed[default=0]** : 
Graine du générateur de nombre aléatoire, analogue au random_state du Gradient Boosting.

[Tuto pour le tunning avec XGBoost](http://www.analyticsvidhya.com/blog/2016/03/complete-guide-parameter-tuning-xgboost-with-codes-python/)


