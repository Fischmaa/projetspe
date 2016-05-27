#Noms de villes et d'hôtels

Dans le forum du challenge, nous avons trouvé une personne qui avait réussi à trouver le nom des villes ainsi
que les hotels en rajoutant uniquement les données géographiques de certaines grandes villes. Nous avons donc 
trouver intéressant de détailler comment cette personne avait procédé. Cela permet de découvrir un type d'algorithme pour trouver des données à partir de statistiques et de suppositions.

##Concept de la recherche
La personne va essayer de d'identifier les différents pays, régions et villes qui sont représentées initialement par des chiffres. Pouur cela, elle va essayer de voir les destinations les plus demandées par les utilisateurs qui correspondra aux sites les plus touristiques. La démarche consistera ensuite de retrouver les villes et régions grâce aux distances fournies et les données GPS des régions. 


##Données utilisées
### Données fourni par le challenge
La personne utilise uniquement les données relatives à la position des hôtels et des utilisateurs du site. Elle utilise aussi la distance entre l'utilisateur et l'hôtel sélectionné. Les données utilisées sont :

| Données sur l'utilisateur | Données sur l'hotel | Autres données            |
|:-------------------------:|:-------------------:|:-------------------------:|
| user_location_country     |  hotel_country      | orig_destination_distance |
| user_location_region      |  hotel_market       |                           |
| user_location_city        |  srch_destination_id|                           |


###Données apportés
La personne utilise les données GPS venant d'un site [http://www.distancefromto.net/](http://www.distancefromto.net/) qui permet de connaitre la distance entre deux villes.


##Cheminement de la réflexion
1. Trouver une première localisation (Hawaii)
2. Trouver les villes et régions à partir de la première localisation (villes des Etats-Unis)
3. Trouver les pays, régions et villes à l'international



