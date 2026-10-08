# Ajouter un projet au portfolio

Les projets réalisés sont décrits à un seul endroit : la page Studio, dans l'entrée qui correspond (`id="mediation"` pour les supports pédagogiques, `id="papeterie"` pour la papeterie personnalisée, `id="jeux"` pour les jeux de société, `id="livres"` pour les livres et ouvrages). Tout vit dans [index.html](index.html), à l'intérieur de la section `data-page="studio"`.

Pour ajouter un projet :

1. Déposez la photo dans `images/photos/` sans renommer, déplacer ni remplacer un fichier existant.
2. Générez sa version WebP : `python3 scripts/generate-webp.py` (ajoutez d'abord le nom du fichier au jeu `REFERENCED` du script).
3. Copiez un bloc `<article class="project rise">` existant dans l'entrée voulue de la page Studio, collez-le à la suite des autres, puis renseignez : le chemin de l'image et son `srcset` WebP, un texte alternatif qui décrit ce que montre la photo (pas son nom de fichier), les dimensions réelles `width`/`height`, le titre du projet, le commanditaire, la commande et ce que vous avez fait. 
4. Répercutez le changement sur les pages statiques : `python3 scripts/generate-static-pages.py && python3 scripts/inject-head-tags.py && python3 scripts/generate-article-pages.py` (le dernier script recopie l'en-tête et le pied de page dans les articles du blog).

## Remplir les tarifs et les visuels

Chaque entrée de la page Studio affiche « À partir de [à définir] ». Dans [index.html](index.html), remplacez chaque `<span class="tbd">[à définir]</span>` par le prix (par exemple `350&nbsp;€`).

Les références « Livre de généalogie familiale » et « Série de cartes postales » attendent leur visuel : remplacez `<div class="todo">[visuel à venir]</div>` par un bloc `<picture>` comme celui du guide des poules (photo dans `images/photos/`, version WebP, texte alternatif, dimensions réelles).

Relancez ensuite les scripts de l'étape 4.
