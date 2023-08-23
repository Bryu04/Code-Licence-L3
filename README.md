# Détails sur les programmes python

Le programme python dict_species2.py parcours tous les fichiers des sous-dossiers du dossier central (nom_global) et crée pour chaque sous-dossier des dictionnaires reprenant toutes les données concernant l’abondance en fonction du temps pour chaque fichier dans le sous-dossier en les classant en fonction des espèces. 

Le programme nautilus_code_supreme.py  crée des processeurs qui lancent le code Nautilus sur plusieurs fichiers simultanément, ce qui permet de gagner du temps. Le code Nautilus est un code astrochimie créé pour calculer les abondances des espèces en fonction du temps.  

Le programme plot.py reprend les dictionnaires créés avant afin de pouvoir tracer des courbes comme  l’abondance de 4 espèces choisies en fonction du temps, l’évolution temporelle de la distance de désaccord ou encore la température en fonction du temps. 

Le programme select_part.py parcours tous les fichiers et reprend ceux dans lesquels il y a une Abondance supérieure ou égale à l’abondance maximale définit dans le programme, les réarrange dans un bon format ,et les met dans un nouveau dossier. Cela est faite pour prendre des mesures que dans les zones qui sont proches d’un bras spiral d’une galaxie. 
