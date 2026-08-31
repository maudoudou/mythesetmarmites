# Rapport de refonte vitrine — mythesetmarmites.fr

Branche `refonte-vitrine`, partie de `refonte-2026` (`2de3645`). Sept commits.
Le dépôt était propre au départ : aucun commit de sauvegarde nécessaire.

Prévisualiser en local :

```
git checkout refonte-vitrine
python3 -m http.server 8000
```

Puis `http://localhost:8000/`, `/studio`, `/correction`, `/a-table`, `/jeu`,
`/parcours`, `/contact`, et un article : `/a-table/pain-poule-rousse`.

Après toute modification de contenu (`index.html` ou `script.js`), relancer
dans cet ordre :

```
python3 scripts/generate-static-pages.py
python3 scripts/inject-head-tags.py
python3 scripts/generate-article-pages.py   # nécessite macOS
python3 scripts/generate-sitemap.py
python3 scripts/generate-web-images.py      # seulement si nouvelle photo
```

---

## Lots effectués, lots annulés

Les quatre lots ont été menés à bien. **Aucun lot n'a été annulé** : chacun a
passé la vérification (fichiers locaux présents, routes qui répondent, CSS et
JS qui se chargent, HTML équilibré) avant son commit.

- **Lot 1 — Contenu** (`fbdc3d6`). Accueil ramené à six blocs. Studio
  réorganisé (« Ce que je fais, en détail », « Compétences », « Comment ça se
  passe », « Qui suis-je » raccourci, « Recherche » remontée). Page
  Correction et relecture réécrite mot pour mot selon le brief. Ateliers
  retirés partout (section, page, menus en-tête et pied, option du
  formulaire, offre du JSON-LD, sitemap, routage). Parcours : intro,
  « Compétences » développé, galerie ramenée de dix à six photos. À table,
  Le jeu, Contact, pied de page mis à jour. Un seul `<h1>` par page.
- **Lot 2 — Design** (`a7a3637`). Bandes de section qui font alterner crème,
  vert très pâle et violet très pâle ; titres de section colorés selon la
  bande ; illustrations agrandies posées en ancrage de section ; cartes à
  fond de palette pâle ; boutons pleins colorés à survol franc. Contraste
  AA vérifié sur chaque paire (tableau plus bas).
- **Lot 3 — Référencement technique** (`81e8bc8`, `61d9cf2`, `556d157`).
  3.1 déjà satisfait (voir plus bas). 3.2 : sortie du `#/` par vraies pages
  statiques + `_redirects` (décision détaillée plus bas). 3.3 : `<head>`
  complet et unique par page. 3.4 : Person, ProfessionalService, Game,
  BlogPosting. 3.5 : sitemap, robots, favicon, manifeste. 3.6 : WebP
  redimensionnés, `loading`, `alt`, balises sémantiques, focus.
- **Finitions** (`83239fe`). Ponctuation (tirets cadratins retirés du texte
  rédigé pour la refonte), couleur du message d'erreur du formulaire.

---

## Fichiers créés, modifiés, convertis

**Créés — pages** : `_redirects` ; `a-table/<slug>/index.html` pour les
16 articles du blog.

**Créés — outillage** (dans `scripts/`) :

- `generate-article-pages.py` — une vraie page HTML par article, en
  réutilisant `articleHTML()` de `script.js` tel quel (exécuté via
  JavaScriptCore, `osascript -l JavaScript` ; nécessite macOS).
- `generate-sitemap.py` — réécrit `sitemap.xml` d'après les pages présentes.
- `generate-web-images.py` — (re)génère les `.webp` d'affichage
  redimensionnés. Ne touche aucun fichier d'origine.
- `check-contrast.py` — ratio de contraste WCAG de chaque paire de la charte.

**Modifiés** : `index.html`, `script.js`, `style.css`, `sitemap.xml`,
`site.webmanifest`, `robots.txt` (inchangé au fond), `CONTRIBUTING.md`,
les six pages statiques de rubrique, `scripts/generate-static-pages.py`,
`scripts/inject-head-tags.py`.

**Supprimé** : `ateliers/index.html` (prestation retirée).

**Images — `.webp` uniquement, à côté des originaux, aucun original touché,
aucun fichier supprimé, renommé ou déplacé** :

- Redimensionnés + recompressés : 21 fichiers. `poules-web.webp`
  1 333 Ko → 161 Ko, `suede-web.webp` 213 → 84, `AFC-forum-web.webp`
  211 → 85, `cropped-logo-vectoriel-mdj.webp` 166 → 34, etc.
- Créés (n'avaient pas de `.webp`) : `jetons-web.webp`, `panier-web.webp`,
  `photos-photos-web.webp`, `portrait-maud-web.webp`.

**Non touchés** : toutes les adresses e-mail et liens `mailto:` (l'écart
entre l'adresse affichée `bonjour@mythesetmarmites.fr` et le lien
`lnrmaud@gmail.com` est laissé tel quel) ; les polices ; `CNAME` ;
`.nojekyll` ; tous les fichiers `.jpg`, `.png`, `.avif`, `.svg` du dossier
`images/`.

### Point 3.1 — chemins relatifs

Rien à convertir : tous les chemins d'images, de CSS et de JS étaient déjà
absolus (`/images/…`, `/style.css`, `/script.js`), hérités du commit
`ac109e0`. Vérifié sur `index.html`, `script.js`, `style.css` et les
23 pages : aucune référence relative, aucun `url()` relatif dans le CSS.
Aucun commit séparé, faute de changement.

---

## Décision du point 3.2 — sortie du routing en `#/`

**Solution retenue : la solution de repli du brief — de vraies pages HTML
statiques — pas l'History API.**

Le brief autorisait ce repli « si la migration demande de réécrire plus de
la moitié du JS de routage ». C'est le cas, et pour une raison de fond :

- `index.html` est la **coquille** : elle contient toutes les sections du
  site (c'est la source de `generate-static-pages.py`). Passer à l'History
  API demanderait soit de la vider et de réinjecter chaque section en
  JavaScript selon `location.pathname`, soit de laisser toutes les sections
  dans le document — auquel cas chaque URL (`/studio`, `/jeu`…) servirait
  le contenu de **toutes** les pages, un problème de contenu dupliqué pour
  l'indexation. Les deux options dépassent largement la moitié du JS de
  routage actuel.
- Six pages statiques réelles existaient déjà (commit `e730dfe`). Les
  compléter et les étendre au blog était le chemin le plus court **et** le
  meilleur résultat pour le référencement : une vraie page HTML par URL,
  avec son propre `<head>`, indexable sans exécuter de JavaScript.

Ce qui a été fait :

- **16 pages d'article** générées à `/a-table/<slug>/`, chacune avec son
  `<title>`, sa meta description, son canonical, son Open Graph et son
  JSON-LD BlogPosting. Le gabarit `articleHTML()` de `script.js` n'a pas
  été réécrit : `generate-article-pages.py` l'exécute tel quel.
- **`_redirects`** (lu par Netlify) :
  - `/ateliers` et `/ateliers/*` → `/studio` en 301 ;
  - `/*` → `/index.html` en 200, repli pour toute URL sans fichier.
- **Redirections des anciennes URL en `#/`** : le serveur ne voit jamais le
  fragment, la redirection est donc côté client. `script.js` :
  `redirectLegacyHash()` renvoie `#/studio` → `/studio`,
  `#/a-table/<slug>` → `/a-table/<slug>` (requête `?cat=` conservée),
  `#/ateliers` → `/studio`. Tous les liens internes du site pointent
  désormais vers les vraies URL ; il ne reste plus aucun `/#/` dans le code.
- La coquille servie par le repli `_redirects` à une URL autre que `/`
  renvoie à l'accueil.

**Limite assumée** : le repli `/* /index.html 200` renvoie un statut 200
pour une URL inexistante (l'accueil s'affiche après un court renvoi JS)
plutôt qu'un vrai 404. C'est la règle demandée par le brief ; toutes les
vraies URL ayant un fichier, seules les URL réellement fautives sont
concernées.

---

## Combinaisons de couleurs créées, avec leur ratio de contraste

La charte n'avait pas de teinte capable de porter du texte au niveau AA :
`--pomme` plafonne à 2,93:1 sur crème, `--haricot` à 2,31:1, `--reverie`
à 2,45:1. Le brief demande la palette existante **et** le contraste AA
« non négociable » : trois variantes foncées des mêmes teintes ont été
ajoutées pour le texte et les aplats de bouton. Les teintes vives restent
pour le décor (filets pointillés, illustrations, grandes formes).

Teintes ajoutées : `--pomme-fonce #B93A27`, `--haricot-fonce #2C744A`,
`--reverie-fonce #4E53C6` ; aplats pâles `--vert-pale #EAF3EC`,
`--violet-pale #EFEFFB`, `--pomme-pale #FBEBE7`, `--haricot-pale #E6F2E9`,
`--reverie-pale #ECECFA`, `--or-pale #FBF2DC`.

| Usage | Premier plan | Fond | Ratio | Seuil | État |
|---|---|---|---|---|---|
| Corps de texte sur crème | `#534741` | `#F8F5F4` | 8,25 | 4,5 | OK |
| Corps de texte sur vert pâle | `#534741` | `#EAF3EC` | 7,90 | 4,5 | OK |
| Corps de texte sur violet pâle | `#534741` | `#EFEFFB` | 7,85 | 4,5 | OK |
| Texte de carte sur pêche pâle | `#534741` | `#FBEBE7` | 7,73 | 4,5 | OK |
| Texte de carte sur vert pâle | `#534741` | `#E6F2E9` | 7,78 | 4,5 | OK |
| Texte de carte sur violet pâle | `#534741` | `#ECECFA` | 7,65 | 4,5 | OK |
| Texte de carte sur jaune pâle | `#534741` | `#FBF2DC` | 8,03 | 4,5 | OK |
| Titre h2 / lien sur crème | `#B93A27` | `#F8F5F4` | 5,24 | 3,0 (h2), 4,5 (lien) | OK |
| Lien sur bande vert pâle | `#B93A27` | `#EAF3EC` | 5,01 | 4,5 | OK |
| Lien sur bande violet pâle | `#B93A27` | `#EFEFFB` | 4,98 | 4,5 | OK |
| Titre h2 vert sur crème | `#2C744A` | `#F8F5F4` | 5,23 | 3,0 | OK |
| Titre h2 vert sur vert pâle | `#2C744A` | `#EAF3EC` | 5,00 | 3,0 | OK |
| Titre h2 violet sur crème | `#4E53C6` | `#F8F5F4` | 5,73 | 3,0 | OK |
| Titre h2 violet sur violet pâle | `#4E53C6` | `#EFEFFB` | 5,45 | 3,0 | OK |
| Texte de bouton plein (primaire) | `#F8F5F4` | `#B93A27` | 5,24 | 4,5 | OK |
| Texte de bouton plein (vert) | `#F8F5F4` | `#2C744A` | 5,23 | 4,5 | OK |
| Texte de bouton plein / survol (encre) | `#F8F5F4` | `#534741` | 8,25 | 4,5 | OK |
| Texte sur panneau jaune plein | `#534741` | `#F4CC71` | 5,85 | 4,5 | OK |

`scripts/check-contrast.py` reproduit ce tableau. La seule paire en échec
qu'il signale (`#F8F5F4` sur `#EB6755` vif, 2,93:1) est une ligne
d'avertissement : cette combinaison **n'est utilisée nulle part**.

---

## Scores Lighthouse

**Je n'ai pas pu faire tourner Lighthouse.** Cet environnement n'a ni
Chrome, ni Node, ni `npx`, et l'accès réseau (y compris `localhost`) y est
bloqué. Je préfère le dire plutôt que d'inventer des scores.

À lancer vous-même — vous avez Brave, qui embarque Lighthouse :

```
python3 -m http.server 8000
```

puis, dans Brave : ouvrez `http://localhost:8000/`, `F12` →
onglet **Lighthouse** → **Analyser**. Faites-le sur `/` et sur
`/a-table/pain-poule-rousse`, sur `main` puis sur `refonte-vitrine`.

À la place, voici des mesures prises sur les fichiers eux-mêmes :

| Mesure | Avant (`main`) | Après (`refonte-vitrine`) |
|---|---|---|
| Pages HTML réelles indexables | 8 | 22 (+ la coquille) |
| Poids cumulé des images référencées (meilleure variante WebP) | 11,4 Mo | 3,3 Mo |
| Image référencée la plus lourde | 1 726 Ko | 161 Ko |
| `poules-web` (accueil + studio) | 1 333 Ko (WebP) | 161 Ko |
| Images chargées d'emblée sur l'accueil (`eager`) | logo seul | logo seul (15 Ko) |
| `<title>` / meta description uniques | 8 | 23, toutes uniques, titres < 60 car. |
| JSON-LD | Person, ProfessionalService, Game + BlogPosting injecté en JS | idem, mais BlogPosting **dans le `<head>`** des 16 pages d'article |
| Contraste des teintes de marque (texte) | `--pomme` 2,93:1, `--haricot` 2,31:1, `--reverie` 2,45:1 (échec AA) | variantes foncées, toutes ≥ 4,5:1 |
| `<h1>` par page | 1 visible mais 7 dans le DOM de la coquille | 1 partout |
| Balises sémantiques | header/nav/main/footer | + `<article>` sur les pages de contenu |

`script.js` fait 45 Ko brut (16 Ko gzip), `style.css` 28 Ko (8 Ko gzip).
Netlify sert les deux compressés.

---

## Repéré et volontairement laissé de côté

- **`script.js` embarque les 16 articles complets** (recettes, récits) et
  est chargé sur toutes les pages, où ces données ne servent pas (hors
  `/a-table`). 16 Ko gzip transportés pour rien sur la plupart des pages.
  *Recommandation :* scinder en `articles.js` (chargé seulement par
  `/a-table/`) et le reste.
- **`poules-web.png` (6 Mo) reste le repli du `<picture>`.** Le `.webp`
  redimensionné (161 Ko) est servi à ~97 % des navigateurs ; les autres
  téléchargent le PNG de 6 Mo. L'original n'a pas été touché (règle du
  brief). *Recommandation :* remplacer l'original par un JPEG ~1 500 px.
- **Deux projets seulement au portfolio.** L'accueil et le studio montrent
  le guide des poules et la collection « Scandinavan » : c'est tout le
  matériel disponible avec des photos. *Recommandation :* ajouter des
  projets via `CONTRIBUTING.md`.
- **Photos retirées de la galerie Parcours** (`marteau-jardin-web`,
  `institut-couture-web`, `livre-hugo-web`, `master-lettres-web`) : leurs
  fichiers restent dans `images/` mais ne sont plus référencés.
  `marteau-jardin-web.webp` fait 1,7 Mo. *Recommandation :* si elles ne
  resservent pas, les retirer (dossier `images/` protégé, à vous de jouer).
- **Trois images orphelines** signalées dans le rapport précédent
  (`bac-web.png`, `design-web.HEIC`, `trames-web.jpg`) : toujours
  inutilisées, pas touchées.
- **`diplome-bachelor-web.webp` (142 Ko)** garde une compression douce
  volontairement : c'est une attestation avec du texte fin à garder
  lisible. `portrait-maud-web.webp` (160 Ko) est à 1 300 px pour une carte
  qui l'affiche assez grand.
- **Illustrations d'ancrage masquées sous 1080 px.** Sur tablette et mobile
  elles ne s'affichent pas, pour ne pas gêner la lecture. Le brief demandait
  la lisibilité mobile ; le compromis a été de garder les illustrations
  marquées sur grand écran seulement.
- **`/a-table` (la liste) est une `<section>`, pas un `<article>`** : c'est
  un index, et ses vignettes sont déjà des `<article>` (générés par
  `cardHTML`). Les cinq autres pages de rubrique sont bien des `<article>`.
- **Le tableau de bord Netlify** n'a pas été vérifié (pas d'accès). Le
  fichier `_redirects` est à la racine du dossier publié, Netlify le lira
  au prochain déploiement.

---

## Ce qui reste à fournir par l'autrice

1. **Des projets pour le portfolio** : photo(s), commanditaire, nature de
   la commande, livrables. Procédure dans `CONTRIBUTING.md`.
2. **Un original allégé pour `poules-web`** (JPEG ~1 500 px), à déposer à
   côté du PNG.
3. **Le score Lighthouse** avant/après, à mesurer dans Brave (voir plus
   haut) — je n'ai pas pu le faire.
4. **Décision sur les images de galerie retirées** et les orphelines :
   les garder ou les supprimer du dépôt.
5. **Vérifier le rendu visuel** des bandes de couleur et des illustrations
   d'ancrage sur un vrai écran, en particulier à 375 px et autour de
   1000-1100 px de large (bascule de l'affichage des illustrations).
6. **Le libellé exact du parcours vidéo / scénographie / web** dans le
   bloc Compétences de la page Parcours : je l'ai rédigé au plus près de
   vos expériences listées, à relire.
