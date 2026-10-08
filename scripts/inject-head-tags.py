#!/usr/bin/env python3
"""Écrit les balises <head> propres à chaque page : <title> unique,
meta description unique, canonical, Open Graph complet, Twitter Card,
et les données structurées JSON-LD (Person et ProfessionalService sur
l'accueil, Game sur la page du jeu). Lit et réécrit index.html et les
cinq pages statiques générées par generate-static-pages.py.

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
DOMAIN = "https://studiomillepages.fr"
# Image de partage du studio (logo carré sur Pot au Lait). Le jeu et le
# blog À table, projets Mythes & Marmites, gardent l'image d'origine.
OG_IMAGE = f"{DOMAIN}/images/og-studio-mille-pages.png"
OG_IMAGE_MM = f"{DOMAIN}/images/og-share.png"
OG_BY_PAGE = {"a-table/index.html": OG_IMAGE_MM, "jeu/index.html": OG_IMAGE_MM}

# path relatif du fichier -> (URL absolue, title, description, og:type)
PAGES = {
    "index.html": (
        "/",
        "Studio Mille Pages · designer éditoriale à Rouen",
        "Maud Lenoir, designer éditoriale et maquettiste : livrets pédagogiques, livres et faire-part, pour les collectivités, les lieux culturels, les associations et les familles.",
        "website",
    ),
    "studio/index.html": (
        "/studio",
        "Le studio · supports pédagogiques, livres, papeterie",
        "Supports pédagogiques et médiation, papeterie personnalisée, jeux de société, livres et ouvrages : mise en pages à partir de votre charte ou d'une direction typographique.",
        "website",
    ),
    "a-table/index.html": (
        "/a-table",
        "À table · une recette et le récit qui va avec",
        "Deux fois par mois, une recette et le conte, le mythe ou l'album qui l'accompagne, plus des notes de lecture sur la nourriture dans les livres pour enfants.",
        "website",
    ),
    "jeu/index.html": (
        "/jeu",
        "Mythes &amp; Marmites · le jeu de récit coopératif",
        "Un jeu de récit coopératif à partir de 6 ans, pour 2 à 6 joueurs, une partie de 45 minutes. Prototype en test, cherche un éditeur et des tables pour jouer.",
        "website",
    ),
    "parcours/index.html": (
        "/parcours",
        "Parcours · Maud Lenoir, designer éditoriale",
        "Deux fois majore de promotion en design et en communication, un an chargée de communication en collectivité, master de littérature jeunesse en cours.",
        "website",
    ),
    "contact/index.html": (
        "/contact",
        "Contact · Studio Mille Pages",
        "Un livret, un livre, un faire-part : écrivez-moi quelques lignes. Réponse sous deux jours ouvrés. Basée à Rouen, disponible partout en France.",
        "website",
    ),
}

PERSON = {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Maud Lenoir",
    "jobTitle": "Designer éditoriale et maquettiste",
    "description": "Designer éditoriale et maquettiste : supports pédagogiques et de médiation, livres et ouvrages, papeterie personnalisée.",
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
    "areaServed": ["Rouen", "Métropole Rouen Normandie", "Normandie"],
    "knowsAbout": [
        "Maquette et mise en pages",
        "Design éditorial",
        "Direction typographique",
        "Supports pédagogiques et de médiation",
        "Papeterie personnalisée",
    ],
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
    "name": "Studio Mille Pages",
    "url": DOMAIN + "/",
    "image": OG_IMAGE,
    "description": "Studio de design éditorial : mise en pages de supports pédagogiques et de médiation, de livres et ouvrages, et de papeterie personnalisée.",
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
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Livrets pédagogiques, guides pour les familles, fiches d'activité, livrets de visite et panneaux d'exposition"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Papeterie personnalisée : faire-part de naissance et de mariage, cartes"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Conception et mise en pages de jeux de société et de jeux pédagogiques : cartes à jouer, livrets de règles, boîtes et emballages, éléments de jeu"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Mise en pages de livres et d'ouvrages : livres de famille, ouvrages d'associations, catalogues, recueils"}},
        ],
    },
}

GAME = {
    "@context": "https://schema.org",
    "@type": "Game",
    "name": "Mythes & Marmites",
    "url": DOMAIN + "/jeu",
    "image": OG_IMAGE_MM,
    "description": "Un jeu de récit coopératif à partir de 6 ans, pour 2 à 6 joueurs, une partie d'environ 45 minutes.",
    "genre": "Jeu de récit coopératif",
    "numberOfPlayers": {"@type": "QuantitativeValue", "minValue": 2, "maxValue": 6},
    "typicalAgeRange": "6-",
    "author": {"@type": "Person", "name": "Maud Lenoir"},
    "additionalProperty": [
        {"@type": "PropertyValue", "name": "Durée d'une partie", "value": "45 minutes"},
        {"@type": "PropertyValue", "name": "Statut", "value": "Prototype en test, à la recherche d'un éditeur"},
    ],
}

# fichier -> liste des objets JSON-LD à poser sur cette page
JSON_LD = {
    "index.html": [PERSON, PROFESSIONAL_SERVICE],
    "jeu/index.html": [GAME],
}


def build_head_block(url_path, title, desc, og_type, og_image=OG_IMAGE):
    url = DOMAIN + url_path
    title_plain = re.sub(r"&amp;", "&", title)
    return (
        f'<title>{title}</title>\n'
        f'<meta name="description" content="{desc}">\n'
        f'<link rel="canonical" href="{url}">\n'
        f'<meta property="og:title" content="{title_plain}">\n'
        f'<meta property="og:description" content="{desc}">\n'
        f'<meta property="og:image" content="{og_image}">\n'
        f'<meta property="og:url" content="{url}">\n'
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:locale" content="fr_FR">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{title_plain}">\n'
        f'<meta name="twitter:description" content="{desc}">\n'
        f'<meta name="twitter:image" content="{og_image}">'
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

        new_head_lines = build_head_block(url_path, title, desc, og_type,
                                          OG_BY_PAGE.get(rel_path, OG_IMAGE))

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
