## Etude de la fonction de notation

[Retour au sommaire d'Expedia](expedia_sommaire.md)

### Introduction

Comme pour chaque challenge hébergé par kaggle, l'organisateur du challenge donne une fonction de notation prenant en paramètre les données soumises par le participant et les données réellement enregistrées. Cette fonction permet de produire le classement des participants. Il est donc utile d'étudier cette méthode de notation pour une meilleur approche du problème.

La page kaggle du challenge nous fournit une [première explication](https://www.kaggle.com/c/expedia-hotel-recommendations/details/evaluation) de cette fonction. Nous nous attelons ici la tâche de comprendre plus en profondeur cette fonction de notation.

### Données à soumettre

Pour se classer dans le challenge Expedia, on nous demande de soumettre un fichier au format `csv` associant les identifiants des utilisateurs (colonne `id`) à une liste de au plus cinq clusters d'hôtels (colonne `hotel_cluster`). Voir [l'explication des données](expedia_data.md#informations-sur-lhôtel) pour une explication de la donnée `hotel_cluster`.
