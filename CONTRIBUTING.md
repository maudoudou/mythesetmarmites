# Ajouter un projet au portfolio

Les projets réalisés apparaissent à deux endroits : la section « Projets récents » de la page d'accueil et la section « Quelques projets » de la page Studio (`id="projets"`). Les deux vivent dans [index.html](index.html), à l'intérieur des sections `data-page="accueil"` et `data-page="studio"`.

Pour ajouter un projet :

1. Déposez la photo dans `images/photos/` sans renommer, déplacer ni remplacer un fichier existant.
2. Générez sa version WebP : `python3 scripts/generate-webp.py` (ajoutez d'abord le nom du fichier au jeu `REFERENCED` du script).
3. Copiez un bloc `<article class="rise">` existant dans la section voulue, collez-le à la suite des autres, puis renseignez : le chemin de l'image et son `srcset` WebP, un texte alternatif qui décrit ce que montre la photo (pas son nom de fichier), les dimensions réelles `width`/`height`, le titre du projet, le commanditaire, la nature de la commande et les livrables.
4. Répercutez le changement sur les pages statiques : `python3 scripts/generate-static-pages.py && python3 scripts/inject-head-tags.py`.

Le texte alternatif décrit l'image pour les personnes qui utilisent un lecteur d'écran : « Couverture et double page intérieure d'un livret jeunesse », pas « projet-client-final.jpg » ni le titre déjà donné à côté.
