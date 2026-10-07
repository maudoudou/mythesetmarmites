# Ajouter un projet au portfolio

Les projets réalisés sont décrits à un seul endroit : la page Studio, dans l'entrée qui correspond au public (`id="mediation"` pour les collectivités et lieux culturels, `id="edition"` pour les maisons d'édition). L'accueil n'en montre que la photo et la légende, dans la section « Références » (planches `figure.plate`). Tout vit dans [index.html](index.html), à l'intérieur des sections `data-page="accueil"` et `data-page="studio"`.

Pour ajouter un projet :

1. Déposez la photo dans `images/photos/` sans renommer, déplacer ni remplacer un fichier existant.
2. Générez sa version WebP : `python3 scripts/generate-webp.py` (ajoutez d'abord le nom du fichier au jeu `REFERENCED` du script).
3. Copiez un bloc `<article class="project rise">` existant dans l'entrée voulue de la page Studio, collez-le à la suite des autres, puis renseignez : le chemin de l'image et son `srcset` WebP, un texte alternatif qui décrit ce que montre la photo (pas son nom de fichier), les dimensions réelles `width`/`height`, le titre du projet, le commanditaire, la commande et ce que vous avez fait. Si vous voulez aussi le montrer sur l'accueil, ajoutez une planche `figure.plate` (photo et légende seulement, pas de description : elle reste sur le studio).
4. Répercutez le changement sur les pages statiques : `python3 scripts/generate-static-pages.py && python3 scripts/inject-head-tags.py && python3 scripts/generate-article-pages.py` (le dernier script recopie l'en-tête et le pied de page dans les articles du blog).

## Remplir les tarifs

Les trois formules de la page Studio affichent « À partir de [à définir] ». Dans [index.html](index.html), remplacez chaque `<span class="tbd">[à définir]</span>` par le prix (par exemple `350&nbsp;€`), puis relancez les scripts de l'étape 4.

Le texte alternatif décrit l'image pour les personnes qui utilisent un lecteur d'écran : « Couverture et double page intérieure d'un livret jeunesse », pas « projet-client-final.jpg » ni le titre déjà donné à côté.
