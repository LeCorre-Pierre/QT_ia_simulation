Ce projet à pour but d'augmenter mes connaissance sur chatgpt et sur les algorithme ia evolutif.

Pour cela, je met en place une simulation

Dans l'interface principale, je trouverai une liste des 10 meilleures IA.
A partir de cette liste, je suis en mesure de réalisée plusieurs actions:

1) Lancer la recherche
En sélectionnant une ou plusieurs IA et en appuyant sur le bouton "Rechercher", une nouvelle fenetre s'ouvre qui
execute des simulations en boucles. Dans le cas ou aucune IA n'est sélectionnée, on recommence le processus de création de 0 avec une
IA avec des valeurs aléatoires pour le reseau de neurones.
Cette fenetre propose de customiser:
   - Les taux de mutations (valeurs entre 0 et 1 avec 0.5 par défaut)
   - Les taux de croisement (valeurs entre 0 et 1 avec 0.5 par défaut)
   - Le nombre d'ia par génération (Nombre entier avec 100 par défaut)
   - Le nombres de tour pour chaque simulation (Nombre entier positif avec 100 par defaut)
   - Le nombre de personnes qui jouent sur la même carte en simultané (Nombre entier avec 1 par defaut)
Une fois les valeurs choisies, un bouton "Lancer la recherche" permet d'éxécuter des simulations en boucles.
Un bouton arreter la recherche, permet d'arreter la recherche.
Au fur et à mesure de l'execution les meilleures IA sont mises dans une liste pour être réutilisée plus tard. Cette liste ne 
contient que 10 éléments.
On peut supprimer les ia de cette liste en faisant bouton droit supprimer.
On peut faire une sauvegarder vers l'interface principale en faisant bbouton droit sauvegarde
Si des ia de meilleures qualités sont trouvées, elles sont sauvegardées et remplacent directement les obsoletes.
2) Affichage infini
Sur la fenetre principale se trouve un affichage de map par default.
Cet espace est appelé "jeu infini". Il est composé sur la partie haute d'un bouton reset qui permet de remettre la carte dans son état par defaut,
d'un bouton de sélection de la carte ainsi que slider permettant de régler la vitesse de défilement du temps entre 100 ms et 1000ms par step de 200ms.
Pour finir un bouton Pause/Resume permet de mettre en pause cet fenetre et d'enlever la pause.
Dans la partie basse de cette fenetre se trouve la carte. La carte se met à jour automatiquement en continu à la vitesse indiquée par le slider.
l'utilisateur en cliquant sur la carte fait apparaitre un personnage à cet endroit. Pour se déplacer le personnage est controlé par l'ia qui est sélectionnée
dans la fenetre principale. Une fois que le personnage est épuisé (energie 0), il est retiré. L'utilisateur peut tout à fait insérer plusieurs
personnage


En sélectionnant une IA et en appuyant sur le bouton "Observer", une nouvelle fenetre s'ouvre qui permet d'observer le 
comportement de l'IA sélectionnée dans une carte.
Dans cette interface, on peut observer, a chaque tour, l'état de la carte, le score, le personnage, l'état du reseau neuronnal ainsi
que la prochaine action du personnage. Les tours peuvent être manipulés avec un slider ou les fleches gauches et droites du clavier.
Dans le log, les différentes actions sont indiquées

Précision sur les simulations
Les simulations sont basées sur le module DEAP

Pour ajouter de la diversité dans les Ias générées, la carte de base sera modifiée entre chaque simulation.
Pour une génération données, toutes les IA jouerons sur la même carte, par contre l'evaluation finale se fera sur la carte initiale.
50% des MAP_FLOWER_0 = 27 sont remplacés par des MAP_PATH = 1
20% des MAP_GRASS_START = 2 sont remplacés par des MAP_PATH = 1
