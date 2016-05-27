# Interprétation des données

Interprétation réalisée sur la base d'échantillons aléatoires sur l'ensemble des données. 

## Interprétation individuelle de chaque donnée :

### Channel :

TODO

### Cnt :

TODO

### Date - Month :

D'une année sur l'autre, on remarque quelques patterns récurrents :
* En fin Décembre - début Janvier, les utilisateurs utilisent moins le site Expédia
* En Mars, Juillet et Octobre, on remarque une augmentation d'activité. Notre hypothèse quand à ce phénomène est que ces mois correspondent à des vacances, notamment scolaire.

Si on fait la comparaison des résultats sur l'année, on constate que le nombre de clics par an a doublé entre 2013 et 2015. Quelques recherches nous ont amené à constater qu'en 2013 Expédia a été élu site de [voyage de l'année](http://espace.expedia.fr/presse/expediafr-est-nomme-meilleur-site-de-l-annee-2013-dans-la-categorie-loisirs-voyages-313), ce qui pourrait expliquer cette affluence.

### Day - 1 à 31 :

Même si en moyenne les booking correpondent à ~50% des clics sur l'ensemble du mois, on constate 2 périodes bien distinctes sur ce graphique :
* Jour 6 à 19 : les jours les plus favorables au booking sont situés dans cette période,
* Jour 19 à 31 et 1 à 5 : au contraire, les jours les moins favorables au booking sont dans cette période

Notre hypothèse pour ces pics au cours du mois sont les dates de jour de paie; il faudrait vérifier qu'en moyenne les paies sont délivrées en majorité à la fin de la 1ère semaine du mois mais nous n'avons pas réussi à collecter d'informations à ce sujet.

### DayOfWeek - Lundi à Dimanche :

On constate une baisse d'activité sur le site d' Expéria au fil de la semaine avec une remontée le Dimanche. Néanmoins on constate que les utilisateurs ont plus tendance à faire des réservations en semaine qu'en week-end. Notre hypothèse quand à ce comportement concerne le moral des personnes qui profitent du week-end pour faire leur recherche et discuter ensemble des destinations.

### HotelCluster :

Ce graphique dégage une tendance des utilisateurs : les clusters les plus reservés (ex : 91, 48) sont ceux les plus souvent consultés. Néanmoins, la réciproque n'est pas forcement vrai et un hôtel très consulté peu très bien avoir un très faible taux de réservation (ex: 66, 87).

Si on arrivait à géolocaliser les clusters, il serait possible de savoir si les hôtels très consultés mais peu reservés sont, par exemple, des destinations de rêves plutôt onéreuses (ex: Hawai).

### Hotel_Continent :

Cet histogramme nous a apprend que les utilisateurs ont largement tendance à consulter des offres du continent 2, et que concernant ce dernier ils ont plutôt tendance à réserver (~ 54%) qu'à simplement regarder (~ 46%). De plus, on apprend que les continents 0, 1 et 5 sont très peu présents (~ 7% du total) et qu'ils pourraient donc faire une bonne variable caractéristiques.

### Hotel_country :

Sur ce graphique, on constate des comportements similaires au précédent; on pourrait par exemple se servir de ces données en émettant l'hypothèse que l'hôtel 51 est situé sur le continent 2 pour explorer un peu plus les données, ce qui est fait dans la partie [Data Leak](leak.md).

### Hotel_market :

On constate que certains groupes d'hôtels sont privilégiés par les utilisateurs (ex : 365, 625, 675). On remarque que certains hotels ont une grande proportion de booking (395, 405, 665, 645) et inversement (1505, 1465, 1705, 115). La variable semble donc caractérisante et probablement correlée aux deux précédentes.

### Is_mobile :

Au vu du graphique, les gens ont plutôt tendance à utiliser leur ordinateur (90% utilisateurs PC vs. 10% mobile) :
 * sur ordinateur la tendance est à la réservation,
 * sur mobile, la tendance est à la simple navigation

On pourrait estimer que cette variable est moins significative dans le cas de notre problème puisque dans les deux cas les clusters à proposer restent les mêmes, il s'agirait plutôt de stratégie commerciale/marketing. Néanmoins, rejeter cette variable sans étude plus précise ce serait rejeter de l'information arbitrairement.

### Is_package :

Ce graphique semble nous apporter une information majeure et caractéristante :
* dans un package, les offres sont réservées à hauteur d'environ 33%
* hors package, les offres sont réservées à hauteur d'environ 50%

### Orig_destination_distance :

D'après ce graphique, les utilisateurs consultent et réservent beaucoup plus vers des destinations à moins de 500km. De plus, jusqu'à 1000km le ratio de booking est supérieur à 50%, et la tendance s'inverse au-delà.

### Posa_continent :

Cet histogramme nous apprend que la plus grande affluence d'utilisateurs d'Expédia provient du continent 3; notre hypothèse sur ce dernier est donc assez partagée entre l'Asie et les Etats-Unis même si au vu des diagrammes précédent on aurait plutôt tendance à associer les Etats-Unis au continent 2. Si on réussisait à géolocaliser les données, on pourrait mettre en parallèle ce diagramme avec les données du point précédent pour dégager des tendances de reservations.

### Year : 

Comme remarqué dans l'analyse de l'histogramme suivant la date, il y a eu une forte augmentation de l'activité entre l'année 2013 et 2014 sur le site Expedia.

Pour l'année 2013, il y a plus de réservations que de consultations. Ce rapport s'inverse pour l'année 2014. Toutefois, la différence de ratio booking/consultation reste faible.

Si l'augmentation de l'activité sur le site Expedia est encore vraie, on pourrait imaginer que de plus en plus de visiteurs consulteront le site sans pour autant faire une réservation.

### User_location_region :

Aucune différence significative observée entre booking et consultation.
Il y a quelques régions où il y a une légère différence, cependant la différence ne se fait pas plus en faveur de booking ou de consultation.

### User_location_country : 

De même que pour user_location_region, il n'y a aucune différence perceptible (ce qui paraît logique).
Tout de même, on peut remarquer que seule quelques user_location_country sont représentées, en particulier 67 et 205 qui sont extrêmements élévées par rapport aux autres. 

### User_location_city : 

Comme précédemment, il n'y a aucune différence remarquable entre booking et consultation.

On peut observer néanmoins observer que certaines villes ressortent d'avantage : 
* très utilisatrices d' Expedia : 2250, 4750, 14750, 24250, 25250, 26250, 36250, 47750, 48750, 49250
* très peu utilisatrices d' Expedia : 4250, 6250, 14250, 19750, 20250, 26750, 32000->33000, 35750, 37250, 43750, 52750, 55250

### User_id : 

On voit que tous les utilisateurs ne fonctionnent pas de la même façon. Ainsi, certains consultent plus souvent Expedia qu'ils ne font de réservation, d'autres font exactement l'inverse (ils réservent dès qu'ils consultent) et enfin certains ont un ratio proche de 50% (il y a très peu d'utilisateurs dans ce cas).

Globalement :
* les utilisateurs qui se rendent le plus souvent sur Expedia réservent plus qu'ils ne consultent
* les utilisateurs qui se rendent le moins souvent sur Expedia ont tendances à consulter d'avantage qu'ils ne réservent

Notre hypothèse quant à ces données est que les utilisateurs réguliers ont tendance à faire confiance à Expédia tandis que les autres préfèrent s'assurer de leur choix en prenant le temps d'explorer le site auparavant.

### Srch_rm_cnt :

La grande majorité des recherches est constituée par des demandes de chambre unique, puis de deux chambres :
* pour une chambre unique, il y a un peu plus (~+4%) de consultations que de réservations.
* pour deux chambres, il y a plus de réservations (~+22%) que de consultations.

### Srch_destination_type_id :

On constate tout d'abord que tous les types ne sont pas représentés; en effet, le type 2 est absent.

Seul le type 1 comprend plus de consultations que de réservations; c'est également le type le plus demandé, avec plus de 2 fois par rapport au second (type 6). C'est donc le type le plus populaire.
Les autre types comportent systématiquement plus de réservations que de consultations avec un ratio presque équilibré pour le type 4.

### Srch_destination_id : 

On remarque que comme pour srch_destination_type_id il y a très peu de destinations qui sont plus consultées que réservées. On pourrait donc envisager une combinaison des variables srch_destination_id et srch_destination_type_id de façon à identifier le type d'une destination avec son id.

Il y a des destinations plus populaires que d'autres et, une fois encore, elles générent d'avantage de consultations que de réservations, et inversement pour les moins populaires.

### Srch_co (à vérifier) : 

Etrangement l'histogramme ne superpose pas les données, il faudrait déterminer pourquoi cela : erreur dans la génération du graphe ? bizarrerie des données ? explication rationnelle ?

On remarque qu'entre l'année 2013, 2014, 2015 la forme des données a évoluée : 
* en nombre total, il y a une nette augmentation pour 2014 par rapport à 2013 et en 2015 très : l'interprétation semble compliqué. L'augmentation en 2014 pourrait être expliqué par la hausse d'affluence sur le site (hypothèse déjà émise dans d'autre analyse d'histogramme). Concernant la baisse en 2015, peut-il s'agir d'un problème dans l'échantillon retenu ? (à vérifier ...)
* répartition Booking/Consultation : en 2013, mise à part une date en Décembre, systématiquement le nombre de booking est plus important que de consultation. Alors qu'en 2014, la tendance semble s'être inversée. Peut-être qu'il s'agit d'une amélioration d'expedia qui permet en 2014 de mieux prévoir son voayge ?

Autrement, on remarque que le début d'année n'est pas propice aux checkout et c'est plutôt à partir du mois d'Avril que les données augmentent en nombre, et on peut noter un légère baisse en Septembre. Il y a un pic particulièrement important au mois de Décembre où, toute année confondu il y a plus de consultation que de booking : il pourraît s'agir de tentatives de départ pour les fêtes, il faudrait vérifier si la distance des voyages est plus courte en Décembre ce qui conforterait cette idée.

### Srch_ci : 

L'histogramme ressemble énormément à celui de srch_co. On pouvait s'attendre à ce que les dates soient largement translatées mais ce n'est pas le cas. L'hypothèse qui en découle, et qui est validée grâce à la variable trip_duration, est que la durée des voyages est très courte, ce qui explique que les graphes puissent presquent se superposer.

### Srch_children_cnt : 

On constate un comportement différent en fonction du nombre d'enfant :
* 0 (donnée majoritaire, 8x plus qu'avec 1 enfant) : ~ 53% de réservations contre ~ 47% de consultations,
* 1 : le ratio est d'environ 50% pour les réservations et consultations,
* 2/+ : il y a plus de consultations que de réservations (~ +37%)

L'hypothèse qui résulte de ces données est qu'il doit être plus compliqué de partir avec des enfants.

### Srch_adults_cnt : 

La majorité des voyages se fait avec 2 adultes (~2 fois plus qu'avec 1 adulte). Dans ces voyages, il y a plus de consultations que de réservations (~+20%).
Pour les voyages avec 1 adulte, la tendance s'inverse et il y a presque deux fois plus de réservations que de consultations.
Les voyages comportant 3 ou 4 adultes sont plus rares et il y a à chaque fois un peu plus (~+10%) de consultations que de réservations.
Les voyages comportants un autre nombre d'adulte sont quasi-inexistants.

### Site_name : 

Il y un nom de domaine qui est très majoritairement utilisé (domaine 0) concentrant ~75% des activités. Le nombre de booking est un tout petit peu plus élevé sur ce domaine mais rien de significatif (<+1%).
Il y a 5 autres domaines (8, 11, 13, 23, 34) où il y a de l'activité, en particulier les domaines 11 et 34. De même la différence entre booking et consultation n'est pas significative, toutefois le ratio est inversé pour certains domaines.

## Interaction entre les variables données :

TODO
Matrices de corrélations, etc.

## Ajout de variables et interprétation :

TODO
