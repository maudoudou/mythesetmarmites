#!/usr/bin/env python3
"""Génère de vraies pages HTML statiques pour les six routes principales
du site (studio, correction, a-table, jeu, parcours, contact).

Pourquoi ce script existe
--------------------------
Le site est une page unique (index.html) qui affiche ses « pages » en
JavaScript selon le fragment d'URL (#/studio, #/jeu, etc.). Les moteurs
de recherche n'indexent pas les fragments comme des URL distinctes :
tout le site finissait indexé sous une seule adresse. Ce script prend
le contenu déjà écrit dans index.html (l'en-tête, le pied de page, et
chaque section <section data-page="...">) et en fait une page HTML
autonome par route, à sa propre URL réelle (/studio/, /correction/,
etc.), tout en laissant le routage en #/ fonctionner comme avant sur
la page d'accueil (pour les liens existants et les articles du blog,
qui n'ont pas de page statique dédiée).

Quand le relancer
-----------------
À chaque modification du contenu d'une des six pages dans index.html
(texte, liens, structure), relancez `python3 scripts/generate-static-pages.py`
depuis la racine du dépôt pour répercuter le changement dans les pages
statiques correspondantes. Le script ne touche jamais index.html,
script.js, ni style.css : il ne fait que lire index.html et écrire les
dossiers /studio/, /correction/, /a-table/, /jeu/, /parcours/, /contact/.

Les balises <head> (titre, meta description, canonical, Open Graph,
JSON-LD...) de chaque page statique sont injectées séparément par
scripts/inject-head-tags.py, à relancer aussi après une régénération.
"""
import re
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROUTES = {
    'studio':     'Le studio — Mythes & Marmites',
    'correction': 'Correction et relecture — Mythes & Marmites',
    'a-table':    'À table — Mythes & Marmites',
    'jeu':        'Le jeu — Mythes & Marmites',
    'parcours':   'Mon parcours — Mythes & Marmites',
    'contact':    "Parler d'un projet — Mythes & Marmites",
}


def extract_block(html, open_tag, close_tag, start=0):
    """Renvoie (contenu_complet, fin_du_bloc) en cherchant open_tag puis
    la première occurrence de close_tag qui suit (pas de tags imbriqués
    de même nom dans ce document, donc une recherche simple suffit)."""
    i = html.index(open_tag, start)
    j = html.index(close_tag, i) + len(close_tag)
    return html[i:j], j


def extract_section(html, page_id):
    marker = f'data-page="{page_id}"'
    tag_start = html.rindex('<section', 0, html.index(marker))
    tag_open_end = html.index('>', tag_start) + 1
    close = html.index('</section>', tag_open_end) + len('</section>')
    return html[tag_start:close]


def main():
    with open(os.path.join(ROOT, 'index.html'), encoding='utf-8') as f:
        html = f.read()

    header, _ = extract_block(html, '<header class="nav">', '</header>')
    footer, _ = extract_block(html, '<footer class="foot">', '</footer>')

    generated = []
    for route, title in ROUTES.items():
        section = extract_section(html, route)
        # Les sections sont écrites avec class="page hide" dans index.html
        # (masquées par défaut, affichées en JS selon le fragment d'URL).
        # Sur une page statique dédiée, le contenu doit être visible d'emblée.
        section = section.replace('class="page hide"', 'class="page"', 1)

        # Marque le lien de nav correspondant comme actif (le JS de route()
        # ne s'exécute pas sur ces pages, voir IS_SPA_SHELL dans script.js).
        nav_link = f'<a class="navlink" href="/{route}" data-route="{route}">'
        nav_link_active = f'<a class="navlink is-on" href="/{route}" data-route="{route}" aria-current="page">'
        page_header = header.replace(nav_link, nav_link_active, 1)

        doc = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="icon" href="/images/favicon-orange.svg">
<link rel="apple-touch-icon" href="/images/icon-192.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="canonical" href="https://mythesetmarmites.fr/{route}">
<link rel="stylesheet" href="/style.css?v=3">
</head>
<body>

{page_header}

<main id="main">

{section}

</main>

{footer}

<script src="/script.js"></script>
</body>
</html>
'''
        out_dir = os.path.join(ROOT, route)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(doc)
        generated.append(f'/{route}/index.html')

    print(f"{len(generated)} pages générées :")
    for g in generated:
        print("  -", g)


if __name__ == '__main__':
    sys.exit(main())
