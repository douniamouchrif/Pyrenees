PROJET : GESTION DE DONNEES MASSIVES

ABARKAN Suhaila & MOUCHRIF Dounia
CMI ISI L2

Le but de ce projet était de nous faire découvrir comment gérer des données en masse, et comment les exploiter afin de pouvoir en déduire des résultats intéressants.

Notre site est constitué d'un tableur afin de visualiser toutes les données réunies dans une seule table pyrenees, puis de 3 représentations graphiques.

Le tableur est consitué de toutes les colonnes réunies de chaque table recolte, arbre, station, et vallee, et d'un ID propre à cette table pyrenees.

La première représentation graphique est le Pie-Chart :
- le centre est constitué des deux vallées de nos données : Ossau et Luz;
- le milieu est constitué des divers stations appartenant aux vallées;
- l'extrémité est consitué des codes des arbres liés aux stations.
Ainsi, lorsque l'on sélectionne une vallée, on accède plus emplemant à ses stations, et lorsque l'on sélectionne une station, on accède donc à tous les codes des arbres appartenant à la station sélectionnée.

La deuxème représentation graphique est le Scatter-Chart : il représente la relation entre la quantité totale de glands produits (Ntot) et la surface de projection du houppier (SH), en supprimant les lignes dont le ratio de gland (rate_Germ) qui ont germé a des valeurs nulles. 
Cela explique le fait qu'il n'y pas de données visibles pour les années 2011, 2012, 2013 et 2018.
La ligne noire représente une corrélation de le relation des deux données, et chaque station est designée par une couleur différente.
De plus, la taille de chaque bulle est proportionnelle au pourcentage de ratio de glands qui ont germé en % (rate_Germ).
Enfin, on peut aussi varier la visualisation de ces données en modifiant par True ou False pour log_x et log_y.

La troisième représentation graphique est l'Animation interactive : selon la vallée, on accède à un premier graphique avec des points repésentant chaqun une station selon le volume du houppier en fonction de la hauteur de l'arbre.
Lorsque l'on se place sur un point, des données se mettent à jour sur les deux graphiques complémentaires :
- celui du haut représente l'avancée de la station pour la hauteur de ses arbres au fil des années;
- ceui du bas représente l'avancée de la station pour ses volumes des houppiers au fil des années.
L'interaction entre la souris qui se place sur les points et les deux graphiques mis à jour sont intéressants.
De plus, il est possible de zoomer sur les points du graphique pour ajouter la précision.

Nous avions fait une quatrième représentation que nous avons mis en commentaire dans le code mais qui ne fonctionne pas, nous avons mis ce code en commentaire pour que vous puissiez tout de même lire ce code.
Il s'agissait d'un box plot ou nous pouvions choisir les paramètres (H,VH,SH) et des années dans le dropdown, on affichait un box plot par station dans le graphique. 


