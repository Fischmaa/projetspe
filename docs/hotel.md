[Retour au sommaire d'expedia](expedia_sommaire.md)

#Noms de villes et d'hôtels

Dans le forum du challenge, nous avons trouvé une personne qui avait réussi à trouver le nom des villes ainsi
que les hôtels en ajoutant uniquement les données géographiques de certaines grandes villes. Nous avons donc 
trouvé intéressant de détailler comment cette personne avait procédé. Cela permet de découvrir un type d'algorithme pour trouver des données à partir de statistiques et de suppositions.

##Concept de la recherche
La personne va essayer d'identifier les différents pays, régions et villes qui sont représentées initialement par des chiffres. Pour cela, elle va trouver les destinations les plus demandées par les utilisateurs qui correspondra aux sites les plus touristiques. La démarche consistera ensuite à retrouver les villes et régions grâce aux distances fournies et les données GPS des régions. 


##Données utilisées
### Données fournies par le challenge
La personne utilise uniquement les données relatives à la position des hôtels et des utilisateurs du site. Elle utilise aussi la distance entre l'utilisateur et l'hôtel sélectionné. Les données utilisées sont :

| Données sur l'utilisateur | Données sur l'hotel | Autres données            |
|:-------------------------:|:-------------------:|:-------------------------:|
| user_location_country     |  hotel_country      | orig_destination_distance |
| user_location_region      |  hotel_market       |                           |
| user_location_city        |  srch_destination_id|                           |


###Données apportées
La personne utilise les données GPS venant d'un site [http://www.distancefromto.net/](http://www.distancefromto.net/) qui permet de connaitre la distance entre deux villes.


##Cheminement de la réflexion
1. [Trouver une première localisation](#trouver-une-première-localisation)
2. [Trouver les villes et régions à partir de la première localisation (villes des Etats-Unis)](#trouver-les-villes-et-régions-à-partir-de-la-première-localisation)
3. [Trouver les pays, régions et villes à l'international](#trouver-les-pays-régions-et-villes-à-linternational)


### Trouver une première localisation

La démarche commence par récupérer un million de lignes de la base de test et on les regroupe en fonction des user_location_country et des hotel_country. Puis on calcule le minimum, le maximum, la moyenne et le nombre de fois ou chaque couple (user_location_country, hotel_country) a été trouvé. Nous obtenons un tableau:

|                      |               |  min | mean     | max        | count  |
|:--------------------:|:-------------:|:----:|:--------:|:----------:|:------:|
|user_location_country | hotel_country |      |          |            |        |
|66                    |50 	           |0.0056|860.307373|5156.8218   |323353  |
|205 	                 |198 	         |0.0056|484.961579|3113.8813 	|20790   |
|46 	                 |144 	         |0.0060|197.404405|500.7198 	  |2178    |
|1 	                   |105 	         |0.0766|222.188807|730.5410 	  |3754    |
|205 	                 |50 	           |2.9126|1360.29673|5812.7800 	|30217   |


On peut voir que beaucoup de le tuple (66, 50) revient très souvent. On suppose, à ce moment-là, que *hotel_country n°50 et user_location_country n°66 représente les USA*.

Pour vérifier cette hypothèse, on essaye de savoir combien de région se trouve dans ce pays. On trouve 51 régions différentes donc cela confirme notre supposition.

On sait que Hawaii est une grosse attraction. Du coup, on essaye de savoir quel hotel_country est la plus recherché par les américains. On recherche alors tous les hôtels qui se trouvent aux Etats-Unis, et on regarde ceux dont la distance avec les utilisateurs est d'environ 5000 km (distance moyenne entre le continent nord Américain et Hawaii). On trouve que le hotel_mark n°212 semble le plus prometteur. On trouve rapidment que la région pour les utilisateurs d'Hawaii (user_location_region) doit être le n°246. 


#### Trouver les villes et régions à partir de la première localisation

La suite de la démarche consiste à utiliser la distance de Hawaii avec les différents utilisateurs pour essayer de trouver les villes et régions des Etats-Unis. Le tableau suivant regroupe les distances depuis la région de Hawaii : 

|                      |                    |  min      | mean      | max        | count  |
|:--------------------:|:------------------:|:---------:|:---------:|:----------:|:------:|
|user_location_region  | user_location_city |           |           |            |        |
|174 	                 |24103 	            |2553.6476  |2558.920339|2572.9294   |225     |
|174                   |26232 	            |2388.9474  |2398.424736|2410.4776 	 |205     |
|348 	                 |48862 	            |4955.8994 	|4965.165163|4977.7217 	 |130     |

A partir du site [http://www.distancefromto.net/](http://www.distancefromto.net/), on peut trouver les distances entre des villes. On peut avoir les distances de Honolulu (capitale de l'état de Hawaii) avec les villes suivantes:
* San Francisco : 2397.40 miles (la seconde ligne)
* Los Angeles : 2562.87 miles (la première ligne)
* New York : 4965.20 miles (la troisième ligne)

On peut alors en déduire, par exemple, que la région n°348 est la région de New York.

A partir de ce point, on peut retrouver toutes les grandes villes des Etats-Unis.


### Trouver les pays, régions et villes à l'international

La méthode est la même que pour la deuxième partie de la démarche sauf que l'on utilise New York comme point de repère.
On regarde les personnes qui regarde pour partir à New York mais qui ne sont pas nord-américains. On peut alors à partir des distances moyenne, retrouver les différents pays. Par exemple, on trouve que user_location_country n°1 est l'Italie car plusieurs distances correspondent aux distances entre New York et des villes italiennes (Rome et Milan).

Ensuite on regarde les personnes qui partent de New York vers des pays étrangers. On peut alors trouver la localisation d'autres grandes ville comme Paris(hotel_country n°207). Pour trouver les autres villes des pays, on réitère les deux dernières étapes de la démarche.


## Conclusion

Cette démarche permet de montrer que l'on peut retrouver des données, qui sont pourtant cachées, à partir de la base de données fournie. Cela pourrait permettre d'utiliser de nouvelles informations pour pouvoir affiner les algortihmes utilisés comme le poids historiques de certaines villes ou si la ville à des attractions touristiques importantes.

Cependant, il est nécessaire de noter que l'ajout de la distance entre les villes grâce au site internet [http://www.distancefromto.net/](http://www.distancefromto.net/) est contraire aux règles de Kaggle. Cela permet juste de montrer que beaucoup de données peuvent être retrouvées facilement à partir d'une base assez importante.

Pour avoir toute la démarche, avec le code utilisé, il faut se rendre à l'adresse du [site kaggle](https://www.kaggle.com/dvasyukova/expedia-hotel-recommendations/the-locations-puzzle)
