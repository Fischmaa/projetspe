# Interprétation des données

Interprétation réalisée sur la base d'échantillons aléatoires sur l'ensemble des données. 

## Notes en vrac :

### Date :

2013-2014:

Moins de booking et consultations en janvier.
Pic en mars, juillet, octobre -> semble correspondre aux vacances (scolaires) 

2015 :

Nombre de réservations/consultations qui a plus que doublé de 2013 à 2015 -> popularisation d' Expédia, plus d'affluence sur le site (?).
Question posée : est-ce le comportement des utilisateurs qui explique les sessions sur Expédia en fonction de la date ou simplement la plus grande affluence sur leur site ?

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
Variable très important !

