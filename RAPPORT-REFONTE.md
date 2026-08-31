# Rapport de refonte — mythesetmarmites.fr

Branche `refonte-2026`, 13 commits, aucun lot annulé. Le dépôt était propre au départ (pas de commit de sauvegarde nécessaire).

## Lots effectués

Tous les lots demandés ont été menés à bien. Aucun n'a été annulé : chaque lot a passé la vérification (fichiers locaux présents, routes qui répondent, CSS/JS qui se chargent) avant son commit.

- **Lot 1 — Resserrer l'offre** (commits `1133344` à `72e54cf`) : offre particuliers réduite au livre de recettes de la famille, mention « deux à trois projets par trimestre, sur devis » sur les prestations lourdes, page Correction et relecture créée, section recherche remontée avec un lien depuis l'accueil, zone d'intervention précisée.
- **Lot 2 — Accueil et portfolio** (commits `e4c25e8`, `40e47e5`) : nouveaux titres accueil/studio, gabarit documenté pour les emplacements du portfolio, `CONTRIBUTING.md` créé.
- **Lot 3 — Référencement technique** (commits `ac109e0` à `60e4a25`) : chemins absolus, sortie du routage en `#/` (solution de repli, détaillée plus bas), balises `<head>` par page, JSON-LD, sitemap/robots/favicon/manifeste, performance et accessibilité.
- **Lot 4 — Page ateliers** (commit `7a9b17e`) : page dédiée créée, avec les contenus que je n'avais pas laissés en TODO visible.

## Fichiers créés, modifiés, convertis

**Modifiés** : `index.html`, `script.js`, `style.css`, `sitemap.xml`.

**Créés — pages statiques** (une par route, générées à partir du contenu de `index.html`) : `studio/index.html`, `correction/index.html`, `ateliers/index.html`, `a-table/index.html`, `jeu/index.html`, `parcours/index.html`, `contact/index.html`.

**Créés — outillage** (dans `scripts/`, tous documentés en tête de fichier, à relancer dans cet ordre après une modification de contenu) :
1. `generate-static-pages.py` — régénère les sept pages ci-dessus à partir de `index.html`.
2. `inject-head-tags.py` — pose `<title>`, meta description, canonical, Open Graph, Twitter Card et JSON-LD sur les sept pages.
3. `generate-webp.py` — génère les `.webp` des images lourdes.
4. `generate-og-image.py` et `generate-app-icons.py` — génèrent `images/og-share.png` et les icônes du manifeste (nécessitent macOS/`qlmanage`).

**Créés — divers** : `CONTRIBUTING.md`, `.nojekyll`, `site.webmanifest`, `images/og-share.png`, `images/icon-192.png`, `images/icon-512.png`.

**Convertis (WebP, à côté des originaux, aucun fichier existant supprimé ni renommé)** : 21 images — `poules-web`, `suede-web`, `scandi-web`, `europe-web`, `manger-design-web`, `institut-couture-web`, `livre-hugo-web`, `AFC-forum-web`, `prez-institut-web`, `diplome-bachelor-web`, `master-lettres-web`, `design-web`, `marteau-jardin-web`, `recettes-web`, `cartes-web`, `pain-poule-rousse-web`, `galette-web`, `soupe-web`, `pain-epices-web`, `LOGO-LATELIERPHOTO-version2-CMJN`, `studio_sauvage_yoga_cantine-300x232`. Deux images (`panier-web.jpg`, `portrait-maud-web.jpg`) étaient déjà compressées plus efficacement que ce que WebP obtient à qualité comparable : le script l'a détecté et a laissé l'original tel quel plutôt que de générer un fichier plus lourd.

**Non touchés** : `robots.txt` (déjà correct), `CNAME`, tous les fichiers du dossier `images/` autres que les ajouts ci-dessus, toutes les adresses e-mail et liens `mailto:`.

## Décision du point 3.2 : routage

Le brief proposait deux options : passer à l'History API avec un fichier `_redirects`, ou, si la migration demandait de réécrire plus de la moitié du JS de routage, garder le `#/` et générer de vraies pages statiques.

**J'ai pris la solution de repli, mais pour une autre raison que celle prévue au départ.** Le fichier `_redirects` (`/* /index.html 200`) est une convention propre à Netlify : GitHub Pages, qui héberge ce site, ne le lit pas et n'offre aucune réécriture serveur équivalente. Avec l'History API seule, un accès direct ou un rechargement sur `/studio` aurait renvoyé une 404 — exactement le problème que ce lot devait résoudre. Ce n'est donc pas la taille de la réécriture JS qui a tranché, mais l'incompatibilité de la technique proposée avec l'hébergement réel.

La solution appliquée : `index.html` reste la coquille SPA avec son routage en `#/` (inchangé dans son principe), et sept pages statiques réelles ont été ajoutées (`/studio`, `/correction`, `/ateliers`, `/a-table`, `/jeu`, `/parcours`, `/contact`), chacune un document HTML autonome avec son propre `<head>`. La résolution `dossier/index.html` → URL sans extension est un mécanisme standard de serveur de fichiers statiques, qui fonctionne sur GitHub Pages sans configuration. Les anciens liens `#/studio` etc. redirigent côté client vers la nouvelle URL (`location.replace`, requête conservée). Voir le commit `e730dfe` pour le détail technique.

**Limite assumée** : les articles individuels du blog (`#/a-table/<slug>`) n'ont pas de page statique dédiée — seules les six routes citées par le brief, plus Ateliers, en ont une. Voir « Laissé de côté » plus bas.

## Scores Lighthouse

**Je n'ai pas pu faire tourner Lighthouse.** Cet environnement ne dispose ni de Chrome, ni de Node, ni d'aucun outil équivalent — je n'ai donc aucun score avant/après à donner, et je préfère le dire plutôt qu'en inventer. Lancez-le vous-même :

```
python3 -m http.server 8000
# puis, dans un autre terminal, sur chaque page (avant et après avoir basculé de branche) :
npx lighthouse http://localhost:8000/ --view
npx lighthouse http://localhost:8000/correction --view
```

Ou directement depuis Chrome : ouvrez la page, DevTools → onglet Lighthouse → Analyser.

À la place, voici des mesures réelles, prises sur les fichiers eux-mêmes :

| Mesure | Avant (`main`) | Après (`refonte-2026`) |
|---|---|---|
| Images transférées dès l'arrivée sur le site | 18,1 Mo (41 images, aucune en `lazy`, toutes chargées même masquées par `.hide`) | 139 Ko sur l'accueil (2 SVG décoratifs en `eager`, tout le reste en `loading="lazy"`) |
| Poids des 21 photos les plus lourdes | 18,4 Mo | 6,0 Mo (WebP) |
| Pages HTML réelles indexables | 1 (tout sous `/`) | 8 |
| `<title>` / meta description uniques | 1 jeu, dupliqué implicitement sur tout le contenu | 8 jeux uniques, dans les bornes (titre < 60 car., description 140–160 car.) |
| JSON-LD | aucun | Person, ProfessionalService, Game statiques + BlogPosting injecté par article |
| `alt=""` sur images porteuses de sens | 10 photos du carrousel Parcours sans texte alternatif | toutes décrites |

Ces chiffres pointent dans le sens attendu (Performance et SEO en hausse), mais ce ne sont pas des scores Lighthouse : ne les présentez pas comme tels.

## Prévisualiser en local

```
cd mythesetmarmites
git checkout refonte-2026
python3 -m http.server 8000
```

Puis ouvrez `http://localhost:8000/` (accueil, coquille SPA) et `http://localhost:8000/studio`, `/correction`, `/ateliers`, `/a-table`, `/jeu`, `/parcours`, `/contact` (pages statiques réelles).

Après toute modification de contenu dans `index.html`, avant de commiter, relancez dans l'ordre :
```
python3 scripts/generate-static-pages.py
python3 scripts/inject-head-tags.py
```

## Ce que j'ai repéré et volontairement laissé de côté

- **Contraste des couleurs de marque.** `--pomme` (liens, boutons), `--haricot` et `--reverie` (intitulés de rubrique « eyebrow ») ne passent pas 4,5:1 sur `--lait` : mesurés respectivement à 2,93:1, 2,32:1 et 2,41:1 (`--pomme` plafonne à 2,93:1 même à pleine opacité, donc ce n'est pas réparable par un simple réglage d'opacité). J'ai corrigé ce que je pouvais sans toucher à l'identité visuelle : le texte `.small` (`--encre-55`, 2,71:1 → 4,64:1) et l'anneau de focus clavier (désormais à double contour, visible sur fond clair comme sur fond sombre). Je n'ai pas retouché les teintes de marque elles-mêmes : c'est un choix qui vous appartient. Si vous voulez les rendre conformes tout en restant proches de la teinte actuelle : `--pomme` → `#D42F19` (4,59:1), `--haricot` → `#3C7E53` (4,50:1), `--reverie` → `#5B62DF` (4,55:1) — sensiblement plus sombres, donc à valider visuellement avant d'appliquer.
- **Articles du blog sans page statique.** Comme expliqué plus haut : les 20 articles restent uniquement accessibles via `#/a-table/<slug>`, donc invisibles pour un moteur qui n'exécute pas ce fragment précis. Le balisage BlogPosting est en place mais n'apporte, dans cette architecture, qu'un bénéfice limité. Recommandation : étendre `generate-static-pages.py` pour produire une page par article. C'est faisable sans dupliquer le contenu (j'ai vérifié qu'on peut exécuter en toute sécurité les fonctions de gabarit de `script.js` via `osascript -l JavaScript`, sans les récrire en Python), mais ça n'était pas dans le périmètre du brief pour ce lot et représente un travail comparable à celui déjà fait pour les six pages.
- **Trois images orphelines** dans `images/photos/` : `bac-web.png` (604 Ko), `design-web.HEIC` (1,3 Mo), `trames-web.jpg` (340 Ko) ne sont référencées nulle part sur le site. Je ne les ai pas touchées (aucune suppression du dossier images n'était autorisée). Si elles ne servent vraiment à rien, les supprimer allégerait le dépôt.
- **Redimensionnement des photos.** Les WebP générés gardent les dimensions d'origine ; certaines photos (`marteau-jardin-web.jpg` : 4032×3024, `panier-web.jpg` : 5443×3629) sont bien plus grandes que leur taille d'affichage réelle. Les redimensionner gagnerait encore en poids, mais c'est un recadrage qui touche au rendu : je m'en suis tenue à changer le format de compression, pas les dimensions.
- **Grille « Comment peut-on travailler ensemble » de la page Studio** liste toujours Imprimé / Scénographie / Identité, sans carte Correction — la nouvelle page y est seulement liée depuis la navigation et la liste de l'accueil. Ajouter une quatrième carte casserait la grille à trois colonnes actuelle ; à revoir si vous voulez qu'elle y apparaisse aussi.
- **`<article>` sur les emplacements du portfolio** (gabarit du lot 2.2) : j'ai ajouté cette balise sémantique aux vignettes du blog, pas aux futurs emplacements de projets, qui restent des `<div>`. Ce serait cohérent de l'ajouter aussi une fois que vous aurez rempli le gabarit avec de vrais projets.
