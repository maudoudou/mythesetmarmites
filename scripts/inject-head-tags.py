#!/usr/bin/env python3
"""Écrit les balises <head> propres à chaque page : <title> unique,
meta description unique, canonical, Open Graph complet et Twitter
Card. Lit et réécrit index.html et les six pages statiques générées
par generate-static-pages.py.

Ce script est idempotent : il remplace les balises déjà posées plutôt
que de les dupliquer, donc on peut le relancer sans risque après
avoir modifié PAGES ci-dessous. Le contenu des pages elles-mêmes
(dans index.html) n'est jamais touché : seul le <head> l'est.

À relancer avec `python3 scripts/inject-head-tags.py` après toute
modification des titres/descriptions ci-dessous, ou après une
régénération des pages statiques (generate-static-pages.py écrase le
<head>, il faut donc toujours relancer ce script juste après).
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://mythesetmarmites.fr"
OG_IMAGE = f"{DOMAIN}/images/og-share.png"

# path relatif du fichier -> (URL absolue, title, description, og:type)
PAGES = {
    "index.html": (
        "/",
        "Mythes &amp; Marmites — studio d'édition jeunesse, Rouen",
        "Studio d'édition à Rouen : maquette pour l'édition jeunesse, correction de manuscrits, ateliers lecture et cuisine en médiathèque, et un jeu coopératif.",
        "website",
    ),
    "studio/index.html": (
        "/studio",
        "Le studio, maquette d'édition jeunesse — Mythes &amp; Marmites",
        "Maquette et mise en pages pour l'édition jeunesse, identité visuelle, livrets et panneaux d'exposition. Studio basé à Rouen, pour la Normandie.",
        "website",
    ),
    "correction/index.html": (
        "/correction",
        "Correction et relecture jeunesse — Mythes &amp; Marmites",
        "Préparation de copie, correction orthotypographique et relecture sur épreuves, pour l'édition jeunesse et scolaire. Test de correction sur demande.",
        "website",
    ),
    "a-table/index.html": (
        "/a-table",
        "À table : contes, mythes et recettes — Mythes &amp; Marmites",
        "Un blog qui associe une recette et le conte, le mythe ou l'album qui va avec, plus des notes de lecture sur la nourriture dans les livres pour enfants.",
        "website",
    ),
    "jeu/index.html": (
        "/jeu",
        "Le jeu Mythes &amp; Marmites — récit coopératif",
        "Un jeu de récit coopératif à partir de 6 ans, pour 2 à 6 joueurs, une partie de 45 minutes. Prototype en test, cherche un éditeur et des tables pour le jouer.",
        "website",
    ),
    "parcours/index.html": (
        "/parcours",
        "Mon parcours — Mythes &amp; Marmites",
        "Diplômes, formations et expériences de Maud Lenoir, entre design d'édition, communication et littérature d'enfance et de jeunesse, en master à Artois.",
        "website",
    ),
    "contact/index.html": (
        "/contact",
        "Parler d'un projet — Mythes &amp; Marmites",
        "Un manuscrit à corriger, un livre à mettre en pages, un atelier à monter en médiathèque ou à l'école : écrivez-moi, avec une réponse sous deux jours ouvrés.",
        "website",
    ),
}


def build_head_block(url_path, title, desc, og_type):
    url = DOMAIN + url_path
    title_plain = re.sub(r"&amp;", "&", title)
    return (
        f'<title>{title}</title>\n'
        f'<meta name="description" content="{desc}">\n'
        f'<link rel="canonical" href="{url}">\n'
        f'<meta property="og:title" content="{title_plain}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        f'<meta property="og:image" content="{OG_IMAGE}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:locale" content="fr_FR">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{title_plain}">\n'
        f'<meta name="twitter:description" content="{desc}">\n'
        f'<meta name="twitter:image" content="{OG_IMAGE}">'
    )


def main():
    for rel_path, (url_path, title, desc, og_type) in PAGES.items():
        full = os.path.join(ROOT, rel_path)
        with open(full, encoding="utf-8") as f:
            html = f.read()

        head_start = html.index("<head>") + len("<head>")
        head_end = html.index("</head>")
        head = html[head_start:head_end]

        # on retire tout ce que ce script a pu poser lors d'un passage
        # précédent, pour rester idempotent
        head = re.sub(r'\n?<title>.*?</title>', '', head, flags=re.DOTALL)
        head = re.sub(r'\n?<meta name="description"[^>]*>', '', head)
        head = re.sub(r'\n?<link rel="canonical"[^>]*>', '', head)
        head = re.sub(r'\n?<meta property="og:[^>]*>', '', head)
        head = re.sub(r'\n?<meta name="twitter:[^>]*>', '', head)
        # nettoyage des lignes vides laissées par les retraits ci-dessus
        head = re.sub(r'\n{2,}', '\n', head).strip('\n')

        new_head_lines = build_head_block(url_path, title, desc, og_type)

        # ordre final : charset, viewport, PUIS le bloc ci-dessus, PUIS
        # ce qui restait (favicon, stylesheet...)
        remaining = [l for l in head.split('\n') if l.strip()]
        charset_lines = [l for l in remaining if 'charset' in l or 'viewport' in l]
        other_lines = [l for l in remaining if l not in charset_lines]

        new_head = '\n'.join(charset_lines) + '\n' + new_head_lines + '\n' + '\n'.join(other_lines)
        html = html[:head_start] + '\n' + new_head + '\n' + html[head_end:]

        with open(full, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"head réécrit : {rel_path}")


if __name__ == '__main__':
    sys.exit(main())
