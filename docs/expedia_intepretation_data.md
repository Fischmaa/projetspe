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

### Year : 

Comme remarqué dans l'analyse de l'histogramme suivant la data : entre l'année 2013 et 2014 il y a eu une forte augmentation de l'activité ( booking ou consulation ) sur le site expedia.

Pour l'année 2013, il y a plus de booking que de consultations. Ce rapport s'inverse pour l'année 2014. Toutefois, la différence de ratio booking/consultation reste faible.

Si l'augmentation de l'activité sur le site expedia est vrai, on pourrait imaginer que de plus en plus de visiteurs consulteraient le site sans pour autant booker une reservation.

### User_location_region :

Aucune différence significative observée entre booking et consultation.
Il y a quelques régions où il y a une légère différence, cependant la différence ne se fait pas plus en faveur de booking ou de consultation.

### user_location_country : 

De même que pour user_location_region, il n'y a aucune différence perceptible ( ce qui paraît logique ).
Tout de même, on peut remarquer que seule quelques user_location_country sont représentés et deux en particulier (67 et 205) qui sont extrêmements élévées par rapport aux autres. 

### user_location_city : 

De même, il n'y a aucune différence remarquable entre booking/consultation.
On peut observer, que certaines villes ressortent d'avantage : 
* très utilisatrice de expedia : 2250, 4750, 14750, 24250, 25250, 26250, 36250, 47750, 48750, 49250
* très peu utilisatrice de expedia : 4250, 6250, 14250, 19750, 20250, 26750, 32000->33000, 35750, 37250, 43750, 52750, 55250

### user_id : 

On voit que tous les utilisateurs ne fonctionnent pas de la même façon : ainsi certains consultent plus souvent expedia qu'ils ne book quelque chose et d'autre l'inverse ( ils book dès qu'ils consultent) et certains ratio quasi égal (très peu d'utilisateurs dans ce cas).

Globalement, parmi les utilisateurs qui se rendent le plus souvent sur expedia, ils book plus qu'ils ne consultent ( ils ont tendances à faire confiance aux site et à être sur de leur choix) et de même, parmi ceux qui se rendent le moins souvent sur expedia, ils ont tendances à consulter d'avantage qu'ils ne book.

### srch_rm_cnt :

Tout d'abord, la grande majorité est constitué par des demandes d'une chambre unique puis de deux chambre.
On remarque que pour la demande de chambre unique il y a un peu plus (~+4%) de demande pour les consultations que pour les booking.
Tandis que pour deux chambres, c'est l'inverse il y a plus de booking (~+22%) que de consultations.

### srch_destination_type_id :

Tout d'abord toues les types ne sont pas représentés : le type 2 est complétement absent. Les seuls types présents sont : 1, 3, 4, 5, 6.

Seul le type 1 comprend plus de consultations que de booking et c'est le type le plus demandé (et de loin : plus de 2 fois par rapport au second ( type 6)). C'est donc le type le plus populaire.
Les autre types comportent systématiquement plus de booking que de consultations (presque égale pour le type 4) : ces destinations moins prisé génèrent plus de réservations que de consultations.

### srch_destination_id : 

On remarque que comme pour srch_destination_type_id il y a très peu de destinations qui sont plus consultés que bookées. On pourrait donc envisager une corrélation entre srch_destination_id et srch_destination_type_id de façon à identifier le type d'une destination avec son id.

De plus, il y a clairement des destinations plus populaires que d'autres et une fois encore les plus populaires générent d'avantage de consultation que de booking. Inversement pour les destinations moins populaires.

### srch_co : 

Etrangement l'histogramme ne superpose pas les données, il faudrait déterminer pourquoi cela : erreur dans la génération du graphe ? bizarrerie des données ? explication rationnelle ?
On remarque qu'entre l'année 2013, 2014, 2015 la forme des données a évoluée : 
* en nombre total, il y a une nette augmentation pour 2014 par rapport à 2013 et en 2015 très : l'interprétation semble compliqué. L'augmentation en 2014 pourrait être expliqué par la hausse d'affluence sur le site (hypothèse déjà émise dans d'autre analyse d'histogramme). Concernant la baisse en 2015, peut-il s'agir d'un problème dans l'échantillon retenu ? (à vérifier ...)
*répartition Booking/Consultation : en 2013, mise à part une date en Décembre, systématiquement le nombre de booking est plus important que de consultation. Alors qu'en 2014, la tendance semble s'être inversée. Peut-être qu'il s'agit d'une amélioration d'expedia qui permet en 2014 de mieux prévoir son voayge ?

Autrement, on remarque que le début d'année n'est pas propice aux checkout et c'est plutôt à partir du mois d'Avril que les données augmentent en nombre, et on peut noter un légère baisse en Septembre. Il y a un pic particulièrement important au mois de Décembre où, toute année confondu il y a plus de consultation que de booking : il pourraît s'agir de tentatives de départ pour les fêtes, il faudrait vérifier si la distance des voyages est plus courte en Décembre ce qui conforterait cette idée.

### srch_ci : 

L'histogramme ressemble énormément à celui de srch_co, ce qui est en soi très étrange car une forte demande de départ devrait conduire à une forte demande d'arrivée mais à des dates différentes... Ou alors c'est que la durée des voyages est très courtes et que donc les périodes se recoupent : à vérifier avec une nouvelle variable trip_duration.

### srch_children_cnt : 

Clairement, il y a majoritairement 0 enfant (~8 fois plus qu'avec 1 enfant) lors des voyages avec un peu plus (~+3%) de booking que de consultation.
Pour les voyages avec 1 enfant, il y a presque égalité parfaite entre booking et consultation.
Toutefois, pour les voyages avec 2 enfants il y a plus de consultations que de booking (~+37%) : surement plus compliqué de partir avec avec des enfants ...

### srch_adults_cnt : 

La majorité des voyages se fait avec 2 adultes (~2 fois plus qu'avec 1 adulte). Dans ces voyages, il y a plus de consultations que de booking (~+20%).
Pour les voyages avec 1 adulte, la tendance s'inverse et il y a presque deux fois plus de booking que de consultations.
Les voyages comportant 3 ou 4 adultes sont plus rares et il y a à chaque fois un peu plus (~+10%) de consultations que de booking.
Les voayges comportants un autre nombre d'adulte sont quasi inexistants.

### site_name : 

Il y un nom de domaine qui est très majoritairement utilisé (domaine 0) concentrant ~75% des activités. Le nombre de booking est un tout petit peu plus élevé sur ce domaine mais rien de significatif (<+1%)
Il y a 5 autres domaines (8, 11, 13, 23, 34) où il y a de l'activité en particulier les domaines 11 et 34. De même la différence entre booking et consultation n'est pas significative, toutefois le ratio est inversé pour certains domaines.
