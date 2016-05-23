## Random Forest

L'algorithme du Random Forest est très utilisé pour le challenge kaggle. Cet algorithme demandant une grande puissance de calcul mais certifie une très bonne prédiction dans bon nombre de cas.

Pour illustrer l'algorithme, nous avons représenté ci-dessous un arbre de décision minimaliste. Dans ce cas, on observe l'impact de l'humidité sur les résultats. Pour chaque neud de l'arbre, le chiffre supérieur correspond à la moyen des locations par heure et le pourcentage correspond à la proportion de la population considérée.

![Arbre de décision](images/random_forest_bikesharing.png)

Ainsi le random forest correspond à la génération d'arbres de décision dont les variables utilisées sont aléatoires. On fait ensuite une commité de vote entre les différents arbres.

Nous implémenté cet algorithme en Python. Cela nous a permit d'obtenir un score de 0,68 sur le challenge kaggle. Il est important de préciser que nous avons uniquement pu utiliser 30 arbres alors que cette technique nécessite une centaine d'arbres pour être efficace. Cette limitation est dûe à un manque de ressources de calcul.

Pour pouvoir appliquer l'algorithme du random forest dans les meilleurs conditions, une mise en forme des données a été nécessaire. Il est à noter que ce conditionnement est similaire à celui employé pour les autres techniques de prédiction. Nous le redonnons ici à titre d'information.

**Mise en forme des données :**
* Nous avons indiquer à notre algorithme de considérer les variable telles que `season`, `weather` comme des variables discrètes. Ceci est fait en Python grâce à l'instruction `as_type('categorie')`.
* Nous avons créé des nouvelles colonne d'information : la colonne `date` qui contient la date de l'enregistrement au format `Datetime` et qui permet de créer la colonne `hour` qui contient l'heure de la journée sous forme d'un entier.

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

**Remarque :** On a ici limité le traitement des données. Ce n'était en effet pas le but premier de cet exercice. Nous cherchions ici plutôt à prendre en main le langage et le forme de challenge kaggle plutôt qu'à optimiser au mieux les algorithme.

Les premières étapes d'un travail plus poussé serait de déterminer de meilleurs variables définissant le systèmes. C'est ce type d'approche que l'on essaiera de développer sur le challenge suivant. 


