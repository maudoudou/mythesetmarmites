#!/usr/bin/env python3
"""Écrit les balises <head> propres à chaque page : <title> unique,
meta description unique, canonical, Open Graph complet, Twitter Card,
et les données structurées JSON-LD (Person et ProfessionalService sur
l'accueil, Game sur la page du jeu). Lit et réécrit index.html et les
six pages statiques générées par generate-static-pages.py.

Ce script est idempotent : il remplace les balises déjà posées plutôt
que de les dupliquer, donc on peut le relancer sans risque après
avoir modifié PAGES ou JSON_LD ci-dessous. Le contenu des pages
elles-mêmes (dans index.html) n'est jamais touché : seul le <head>
l'est. Les données BlogPosting (une par article du blog À table) ne
sont pas ici : elles sont injectées côté client par script.js, voir
setArticleJsonLd() — les articles n'ont pas encore de page statique
dédiée (voir RAPPORT-REFONTE.md).

À relancer avec `python3 scripts/inject-head-tags.py` après toute
modification des titres/descriptions/JSON-LD ci-dessous, ou après une
régénération des pages statiques (generate-static-pages.py écrase le
<head>, il faut donc toujours relancer ce script juste après).
"""
import json
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
    "ateliers/index.html": (
        "/ateliers",
        "Ateliers lecture et cuisine — Mythes &amp; Marmites",
        "Un atelier lecture et cuisine pour les scolaires, les médiathèques et les centres de loisirs. Publics visés, matériel fourni et zone de déplacement à Rouen.",
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

PERSON = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Maud Lenoir",
    "jobTitle": "Graphiste éditoriale et autrice, studio d'édition et de récits",
    "url": DOMAIN + "/",
    "workLocation": {
        "@type": "Place",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Rouen",
            "addressRegion": "Normandie",
            "addressCountry": "FR",
        },
    },
    "hasCredential": {
        "@type": "EducationalOccupationalCredential",
        "credentialCategory": "Master",
        "name": "Master Littérature d'enfance et de jeunesse (en cours)",
        "recognizedBy": {"@type": "CollegeOrUniversity", "name": "Université d'Artois"},
    },
}

PROFESSIONAL_SERVICE = {
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "Mythes & Marmites",
    "url": DOMAIN + "/",
    "image": OG_IMAGE,
    "founder": {"@type": "Person", "name": "Maud Lenoir"},
    "areaServed": [
        {"@type": "City", "name": "Rouen"},
        {"@type": "AdministrativeArea", "name": "Métropole Rouen Normandie"},
        {"@type": "AdministrativeArea", "name": "Normandie"},
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Prestations",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Correction et relecture de manuscrits jeunesse et scolaires"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Maquette et mise en pages de livres et albums"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Identité visuelle et charte graphique"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Livrets et panneaux d'exposition"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Ateliers lecture et cuisine en médiathèque"}},
        ],
    },
}

GAME = {
    "@context": "https://schema.org",
    "@type": "Game",
    "name": "Mythes & Marmites",
    "url": DOMAIN + "/jeu",
    "image": OG_IMAGE,
    "description": "Un jeu de récit coopératif à partir de 6 ans, pour 2 à 6 joueurs, une partie de 45 minutes.",
    "genre": "Jeu de récit coopératif",
    "numberOfPlayers": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 6},
    "typicalAgeRange": "6-",
    "duration": "PT45M",
}

# fichier -> liste des objets JSON-LD à poser sur cette page
JSON_LD = {
    "index.html": [PERSON, PROFESSIONAL_SERVICE],
    "jeu/index.html": [GAME],
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
        head = re.sub(r'\n?<script type="application/ld\+json">.*?</script>', '', head, flags=re.DOTALL)
        # nettoyage des lignes vides laissées par les retraits ci-dessus
        head = re.sub(r'\n{2,}', '\n', head).strip('\n')

        new_head_lines = build_head_block(url_path, title, desc, og_type)

        # ordre final : charset, viewport, PUIS le bloc ci-dessus, PUIS
        # ce qui restait (favicon, stylesheet...), PUIS le JSON-LD
        remaining = [l for l in head.split('\n') if l.strip()]
        charset_lines = [l for l in remaining if 'charset' in l or 'viewport' in l]
        other_lines = [l for l in remaining if l not in charset_lines]

        ld_blocks = '\n'.join(
            f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'
            for obj in JSON_LD.get(rel_path, [])
        )

        new_head = '\n'.join(charset_lines) + '\n' + new_head_lines + '\n' + '\n'.join(other_lines)
        if ld_blocks:
            new_head += '\n' + ld_blocks
        html = html[:head_start] + '\n' + new_head + '\n' + html[head_end:]

        with open(full, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"head réécrit : {rel_path}")


if __name__ == '__main__':
    sys.exit(main())
