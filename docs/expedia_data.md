[Retour au sommaire Expedia](expedia_sommaire.md)

## Explication des données

Pour le problème Expedia, on possède beaucoup de données, on va donc ici détailler les différentes données et leur signification.
Sur la age du challenge, on nous popose de télécharger quatre fichiers:

* **train.csv :** Regroupe les données d'entrainement. Ce fichier fait 38 millions de lignes. Il s'agit d'un échantillon pris parmi les données d'Expedia des années 2013 et 2014. Ces données correspondent aux recherches d'hôtels et aux réservations faites par les utilisateurs.
* **test.csv :** Regroupe les données de test. Fichier de 2,5 millions de lignes. Ce fichier regroupe les données de 2015 concernant uniquement les réservations faites par les utilisateurs.
* **sample_submission.csv :** Un exemple de fichier à soumettre.
* **destinations.csv :** Des informations sur les hôtels traduis en `float` (avis sur les hôtels, données de recherche ...)

### train.csv et test.csv

Nous détaillons ici les différentes attributs. Pour train.csv, un ligne correspond à une recherche (un clic) ou à une réservation. Pour test.csv, une ligne correspond à une recherche ou une reservation.

#### Champs communs à train.csv et test.csv

nom du champ | description
:-----------:|------------
`date_time`
site_name
posa_continent
user_location_country
user_location_region
user_location_city
orig_destination_distanceuser_id 	is_mobile 	... 	srch_children_cnt 	srch_rm_cnt 	srch_destination_id 	srch_destination_type_id 	is_booking 	cnt 	hotel_continent 	hotel_country 	hotel_market 	hotel_cluster

#### Champs propres à train.csv

