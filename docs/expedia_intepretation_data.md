# Interprétation des données

Interprétation réalisée sur la base d'échantillons aléatoires sur l'ensemble des données. 

## Notes en vrac :

### Date (ie. Année) et month :

Moins de booking et consultations en janvier.
Pic en mars, juillet, octobre -> semble correspondre aux vacances (scolaires) 

Nombre de réservations/consultations qui a plus que doublé de 2013 à 2015 -> popularisation d' Expédia, plus d'affluence sur le site (?). Est-ce le comportement des utilisateurs qui explique les sessions sur Expédia en fonction de la date, ou simplement la plus grande affluence sur leur site ?

### Day (1-31):

Moins de booking en fin de mois, plus de consultations sans booking.
Au contraire, pics de booking au milieu du mois (jour de paie ?)
Conclusion sur la variable :
Variation visible des consultations/réservation (comportement utilisateur différent) selon le jour du mois -> donne envie de garder cette variable.

### DayOfWeek (Lundi, ..., Dimanche) :

Chute le W-E des deux bases de données (avec plus de consultations que de réservations, contrairement à la semaine).
En semaine, plus consultations/réservations en début de semaine, décroit avec les jours (dû à la "remontée de moral" du W-E -> les gens veulent pas s'embeter le WE)

Conclusion sur la variable : semble plutôt significative pour la congestion du site, intéressant pour la destination ?

### HotelCluster :

Tendance qui se dégage -> les clusters les plus bookés sont souvent consultés, mais l'inverse n'est pas forcement vrai.
Variable très importante !

### Hotel_Continent :

Mise en évidence du continent 2 -> utilisateur ont plus tendance à book ce continent qu'à simplement consulter; pour les autres continents c'est l'inverse.
Absence du continent 1.

### Hotel_country :

Même similarité que le continent 2 pour les pays 51 et 199, on remarque plus de booking que de simples consultations.

### Hotel_market :

Groupes d'hotels privilégiés par les utilisateurs (345-750); certains hotels avec une grande proportion de booking vis-à-vis des consultations (395, 405, 665, 645) et inversement (1505, 1465, 1705, 115). La variable semble donc caractérisante.

### is_mobile :

Au vu du graphique, les gens ont plus tendance à utiliser leur ordinateurs (90% utilisateurs PC vs. 10% mobile) :
 * sur ordinateur la tendance est plus à la réservation qu'à la consultation,
 * sur mobile, c'est l'inverse

Variable moins significative dans le cas de notre problème, les clusters à proposer restent les mêmes; il s'agit plus de stratégie commerciale/marketing.

### is_package :

Les offres qui sont dans un package ne sont bookés avec un ratio que de 1 pour 3 par rapport aux consultations, tandis que le ratio est de 54 pour 100 pour les offres hors packages. Cette variable est donc clairement significative dans notre cas.

### orig_destination_distance :

Les utilisateurs consultent et réservent beaucoup plus vers des destinations à moins de 5km. De plus, jusqu'à 1000km le ratio de booking pour consultation est supérieur à 1/2 alors qu'il devient inférieur après. La variable est donc très significative de notre problème.

### posa_continent :

Cette donnée pondère les distances de recherches par l'origine des utilisateurs. En soit cette variable semble ne pas être porteuse d'information majeure, mais sans elle les résultats retournées par l'algorithme de recommandation ne tiendront pas compte de l'importance de l'origine des données récoltées.
Cette variable semble donc être assez significative.
