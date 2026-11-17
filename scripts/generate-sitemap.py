#!/usr/bin/env python3
"""Réécrit sitemap.xml à partir des pages réellement présentes : l'accueil,
et les quatre pages de rubrique. À relancer si une page est ajoutée ou
retirée.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://studiomillepages.fr"

# (chemin, changefreq, priority)
FIXED = [
    ("/", "weekly", "1.0"),
    ("/studio", "monthly", "0.9"),
    ("/jeu", "monthly", "0.5"),
    ("/parcours", "monthly", "0.7"),
    ("/contact", "yearly", "0.6"),
]


def main():
    rows = list(FIXED)

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
    print(f"sitemap.xml : {len(rows)} URL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
