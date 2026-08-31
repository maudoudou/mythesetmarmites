#!/usr/bin/env python3
"""Réécrit sitemap.xml à partir des pages réellement présentes : l'accueil,
les six pages de rubrique, et une entrée par article du blog (dossiers
a-table/<slug>/). À relancer après generate-article-pages.py si des articles
ont été ajoutés ou renommés.
"""
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://mythesetmarmites.fr"

# (chemin, changefreq, priority)
FIXED = [
    ("/", "weekly", "1.0"),
    ("/studio", "monthly", "0.9"),
    ("/correction", "monthly", "0.9"),
    ("/a-table", "weekly", "0.8"),
    ("/jeu", "monthly", "0.7"),
    ("/parcours", "monthly", "0.5"),
    ("/contact", "yearly", "0.6"),
]


def main():
    slugs = sorted(
        os.path.basename(os.path.dirname(p))
        for p in glob.glob(os.path.join(ROOT, "a-table", "*", "index.html"))
    )
    rows = list(FIXED) + [(f"/a-table/{s}", "yearly", "0.6") for s in slugs]

    body = "\n".join(
        f"  <url>\n    <loc>{DOMAIN}{loc}</loc>\n"
        f"    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>\n  </url>"
        for loc, cf, pr in rows
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"sitemap.xml : {len(rows)} URL ({len(slugs)} articles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
