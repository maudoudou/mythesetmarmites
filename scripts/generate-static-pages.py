#!/usr/bin/env python3
"""Génère de vraies pages HTML statiques pour les six routes principales
du site (studio, a-table, jeu, parcours, contact).

Pourquoi ce script existe
--------------------------
Le site est une page unique (index.html) qui affiche ses « pages » en
JavaScript selon le fragment d'URL (#/studio, #/jeu, etc.). Les moteurs
de recherche n'indexent pas les fragments comme des URL distinctes :
tout le site finissait indexé sous une seule adresse. Ce script prend
le contenu déjà écrit dans index.html (l'en-tête, le pied de page, et
chaque section <section data-page="...">) et en fait une page HTML
autonome par route, à sa propre URL réelle (/studio/, /parcours/,
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
dossiers /studio/, /a-table/, /jeu/, /parcours/, /contact/.

Pipeline complet, à relancer dans cet ordre après toute modification de
contenu (index.html ou script.js) :

    python3 scripts/generate-static-pages.py    # /studio, /parcours, ...
    python3 scripts/inject-head-tags.py         # <head> des 7 pages
    python3 scripts/generate-article-pages.py   # /a-table/<slug>/ (macOS)
    python3 scripts/generate-sitemap.py         # sitemap.xml
    python3 scripts/generate-web-images.py      # .webp redimensionnés (si
                                                # nouvelle photo)

scripts/check-contrast.py vérifie les paires de couleurs de la charte.
"""
import re
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Posé tôt dans le <head> : marque que le JS tourne (-> .js .rise animées).
# Sans JS, ou si script.js échoue, le contenu reste visible (voir style.css)
# et ce repli au chargement révèle toute .rise restée masquée.
JS_MARK = (
    "<script>document.documentElement.classList.add('js');"
    "addEventListener('load',function(){setTimeout(function(){"
    "var r=document.querySelectorAll('.rise:not(.in)');"
    "for(var i=0;i<r.length;i++)r[i].classList.add('in')},500)})</script>"
)

# Version de la feuille de style : à incrémenter quand style.css change,
# pour que les navigateurs ne gardent pas l'ancienne en cache.
CSS_VERSION = '9'

# Titres provisoires : inject-head-tags.py pose ensuite les titres définitifs.
ROUTES = {
    'studio':   'Le studio · Studio Mille Pages',
    'a-table':  'À table · Mythes & Marmites',
    'jeu':      'Le jeu · Mythes & Marmites',
    'parcours': 'Parcours · Studio Mille Pages',
    'contact':  'Contact · Studio Mille Pages',
}


def extract_block(html, open_tag, close_tag, start=0):
    """Renvoie (contenu_complet, fin_du_bloc) en cherchant open_tag puis
    la première occurrence de close_tag qui suit (pas de tags imbriqués
    de même nom dans ce document, donc une recherche simple suffit)."""
    i = html.index(open_tag, start)
    j = html.index(close_tag, i) + len(close_tag)
    return html[i:j], j


def extract_section(html, page_id):
    """Renvoie la <section data-page="..."> complète. Les pages contiennent
    elles-mêmes des <section> (une par titre courant) : on compte donc
    l'imbrication pour trouver le </section> qui ferme la page."""
    marker = f'data-page="{page_id}"'
    tag_start = html.rindex('<section', 0, html.index(marker))
    depth, pos = 0, tag_start
    for m in re.finditer(r'<section\b|</section>', html[tag_start:]):
        depth += -1 if m.group(0) == '</section>' else 1
        if depth == 0:
            pos = tag_start + m.end()
            break
    return html[tag_start:pos]


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

        # Sur la page autonome, le contenu est une composition complète et
        # unique : <section> devient <article> (balise sémantique du brief).
        # a-table reste une <section> : c'est une liste, et ses vignettes
        # sont déjà des <article> (voir cardHTML dans script.js).
        if route != 'a-table':
            section = '<article' + section[len('<section'):]
            section = section[:-len('</section>')] + '</article>'

        # Dans la coquille SPA, le titre de chaque section secondaire est un
        # <h2 class="page-title"> : ça garde un seul <h1> sur la page d'accueil.
        # Sur la page autonome, ce titre redevient le <h1> (classe conservée).
        section = section.replace('<h2 class="page-title"', '<h1 class="page-title"', 1)
        section = re.sub(r'(<h1 class="page-title"[^>]*>[^<]*)</h2>', r'\1</h1>', section, count=1)

        # Marque le lien de nav correspondant comme actif (le JS de route()
        # ne s'exécute pas sur ces pages, voir IS_SPA_SHELL dans script.js).
        nav_link = f'<a class="navlink" href="/{route}" data-route="{route}">'
        nav_link_active = f'<a class="navlink is-on" href="/{route}" data-route="{route}" aria-current="page">'
        page_header = header.replace(nav_link, nav_link_active, 1)
        # « Contact » est un bouton dans le menu : même marquage de page courante.
        contact_btn = '<a class="btn btn--sm" href="/contact" data-route="contact">'
        if route == 'contact':
            page_header = page_header.replace(
                contact_btn, contact_btn[:-1] + ' aria-current="page">', 1)

        doc = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{JS_MARK}
<title>{title}</title>
<link rel="icon" href="/images/charte/web/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/images/icons/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/images/icons/favicon-16.png" sizes="16x16" type="image/png">
<link rel="apple-touch-icon" href="/images/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="canonical" href="https://mythesetmarmites.fr/{route}">
<link rel="stylesheet" href="/style.css?v={CSS_VERSION}">
</head>
<body>

{page_header}

<main id="main" tabindex="-1">

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
