## Random Forest

### Algorithme et résultats obtenus

L'algorithme du Random Forest est très utilisé pour le challenge Kaggle : il demande une grande puissance de calcul mais certifie, dans bon nombre de cas, une très bonne prédiction.

Pour illustrer l'algorithme, nous commençons par expliquer avec la figure suivante ce qu'est un arbre de décision. Dans ce cas minimaliste, on observe l'impact de l'humidité sur les résultats : à gauche les cas qui vérifient la condition "Humidity < 61", et à droite les autres. Pour chaque nœud de l'arbre, le chiffre supérieur correspond à la moyenne des locations par heure, et le pourcentage correspond à la proportion de la population vérifiant la condition de la branche.

![Arbre de décision](images/random_forest_bikesharing.png)

Le principe majeur de l'algorithme de Random Forest est la génération d' arbres de décision où les variables sont choisies aléatoirement. Une fois la forêt d'arbre générée, l'algorithme choisi les variables les plus pertinentes ainsi que l'ordre dans lequelles elles doivent être considérées. Toutefois, les paramètres de base du Random Forest s'assure d'éviter l'overfitting en ne créant pas d'arbres trop profonds qui seraient trop proches des données d'entraînement.

Son implémentation en Python nous a permis d'obtenir un score de 0,68 sur le challenge Kaggle. Il est important de préciser que nous n'avons pu utiliser que 30 arbres alors que cette technique nécessite une centaine d'arbres pour être efficace. Cette limitation est dûe à un manque de ressources de calcul.

### Travail sur les données 

Pour pouvoir appliquer l'algorithme de Random Forest dans les meilleurs conditions, une mise en forme des données a été nécessaire. Il est à noter que ce conditionnement est similaire à celui employé pour les autres techniques de prédiction. Nous le redonnons ici à titre d'information.

**Mise en forme des données :**
* Nous avons dit à notre algorithme de considérer les variable telles que `season`, `weather` comme des variables discrètes. Ceci est fait en Python grâce à l'instruction `as_type('categorie')`.
* Nous avons créé des nouvelles colonnes d'information : la colonne `date` qui contient la date de l'enregistrement au format `Datetime` et qui permet de créer la colonne `hour` contenant l'heure de la journée sous forme d'un entier.

```python
import pandas as pa
from sklearn.ensemble import RandomForestClassifier as rf
import matplotlib.pyplot as plt
from datetime import datetime
pa.options.mode.chained_assignment = None

# On lit les données fournies

tabtrain = pa.read_csv('sources/train.csv')
tabtest = pa.read_csv('sources/test.csv')

# On ajoute une colonne contenant le date au format Datetime
tabtrain['date']=0
for i in range(len(tabtrain)) :
	tabtrain['date'][i]=datetime.strptime(tabtrain['datetime'][i],'%Y-%m-%d %H:%M:%S')

tabtest['date']=0
for i in range(len(tabtest)) :
	tabtest['date'][i]=datetime.strptime(tabtest['datetime'][i],'%Y-%m-%d %H:%M:%S')

# On passe les variables en discret
tabtrain['season'] = tabtrain['season'].astype('category')
tabtrain['holiday'] = tabtrain['holiday'].astype('category')
tabtrain['workingday'] = tabtrain['workingday'].astype('category')
tabtrain['weather'] = tabtrain['weather'].astype('category')

tabtest['season'] = tabtest['season'].astype('category')
tabtest['holiday'] = tabtest['holiday'].astype('category')
tabtest['workingday'] = tabtest['workingday'].astype('category')
tabtest['weather'] = tabtest['weather'].astype('category')


# Création de la colonne contenant l'heure de la journée
tabtrain['hour']=0
for i in range(len(tabtrain)) :
	tabtrain['hour'][i] = tabtrain['date'][i].hour

tabtrain['hour']=tabtrain['hour'].astype('category')

tabtest['hour']=0
for i in range(len(tabtest)) :
	tabtest['hour'][i] = tabtest['date'][i].hour

tabtest['hour']=tabtest['hour'].astype('category')

# Tableaux d'entrainement
y_train = tabtrain['count']
x_train = tabtrain.drop(['datetime','count','casual','registered','date'],1)

# Tableau de résultats
x_test = tabtest.drop(['datetime','date'],1)

model = rf(100)

# Entrainement du modèle
model.fit(x_train, y_train)

# On détermine les prédictions
y_test = model.predict(x_test)

# On formate la sortie pour la submission
y_test = pa.DataFrame(y_test)
y_test.index = tabtest['datetime']

y_test.to_csv('csv/random_forest.csv')
```

**Remarque :** On a ici limité le traitement des données. Ce n'était en effet pas le but premier de cet exercice. Nous cherchions plutôt à prendre en main le langage et le format du challenge kaggle, plutôt qu'à optimiser au mieux les algorithmes.

### Pistes d' amélioration

Les premières étapes d'un travail plus avancé serait de déterminer de meilleurs variables définissant le système. C'est ce type d'approche qu'on essaiera de développer sur le challenge suivant. 


