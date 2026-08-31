#!/usr/bin/env python3
"""Génère une vraie page HTML statique pour chaque article du blog À table,
à /a-table/<slug>/index.html, avec ses propres balises <head> (title, meta
description, canonical, Open Graph, Twitter Card, JSON-LD BlogPosting).

Pourquoi
--------
Les articles vivaient uniquement dans la coquille SPA, à l'URL fragment
#/a-table/<slug> : invisibles pour un moteur qui n'exécute pas ce fragment
précis. Ce script réutilise le gabarit articleHTML() déjà écrit dans
script.js (aucune réécriture : il est exécuté tel quel via JavaScriptCore,
osascript -l JavaScript) et l'enveloppe dans un document complet, en-tête
et pied compris, repris de index.html.

Dépendances : macOS (osascript). À relancer avec
`python3 scripts/generate-article-pages.py` après toute modification des
ARTICLES ou du gabarit articleHTML dans script.js, puis régénérer le
sitemap si des slugs ont changé.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://mythesetmarmites.fr"
OG_FALLBACK = f"{DOMAIN}/images/og-share.png"


def slice_between(src, start_marker, end_marker, inclusive_end=True):
    i = src.index(start_marker)
    j = src.index(end_marker, i)
    return src[i:j + (len(end_marker) if inclusive_end else 0)]


def extract_pure_js():
    """Récupère dans script.js les seules déclarations nécessaires au rendu
    d'un article : pas de code qui touche au DOM."""
    js = open(os.path.join(ROOT, "script.js"), encoding="utf-8").read()
    cats = slice_between(js, "const CATS = [", "\n];")
    articles = slice_between(js, "const ARTICLES = [", "\n];")
    ill_dims = slice_between(js, "const ILL_DIMS = {", "\n};")
    ill_attrs = slice_between(js, "function illAttrs(name) {", "\n}")
    mois = slice_between(js, "const MOIS_FR = {", "};")
    date_iso = slice_between(js, "function dateFrancaiseVersISO(str) {", "\n}")
    article_html = slice_between(js, "function articleHTML(a) {", "\n}\n")
    return "\n".join([cats, articles, ill_dims, ill_attrs, mois, date_iso, article_html])


def run_jxa(pure_js):
    driver = pure_js + r"""
var out = ARTICLES.map(function (a) {
  return {
    slug: a.slug, cat: a.cat, title: a.title, chapeau: a.chapeau,
    img: a.img || null, date: a.date, dateISO: dateFrancaiseVersISO(a.date),
    photo: a.photo || null, html: articleHTML(a)
  };
});
JSON.stringify(out);
"""
    res = subprocess.run(
        ["osascript", "-l", "JavaScript", "-e", driver],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        sys.stderr.write(res.stderr)
        raise SystemExit("échec du rendu JavaScriptCore (osascript)")
    return json.loads(res.stdout)


def header_footer():
    html = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    header = slice_between(html, '<header class="nav">', "</header>")
    footer = slice_between(html, '<footer class="foot">', "</footer>")
    # marque « À table » comme rubrique active
    header = header.replace(
        '<a class="navlink" href="/a-table" data-route="a-table">',
        '<a class="navlink is-on" href="/a-table" data-route="a-table" aria-current="page">',
        1,
    )
    return header, footer


CAT_LABEL = {
    "contes": "Contes", "mythes": "Mythes et fables",
    "albums": "Albums et romans", "notes": "Notes de lecture",
}


def build_page(art, header, footer):
    slug, title, chapeau = art["slug"], art["title"], art["chapeau"]
    url = f"{DOMAIN}/a-table/{slug}"
    full_title = f"{title} — Mythes &amp; Marmites"
    if len(re.sub("&amp;", "&", full_title)) > 60:
        full_title = title  # titre d'article long : on garde < 60 sans le suffixe
    title_plain = re.sub("&amp;", "&", full_title).replace('"', "&quot;")

    # meta description : le chapeau de l'article, complété si trop court
    # pour rester dans une plage utile (140-160 caractères).
    desc_text = chapeau.rstrip()
    if len(desc_text) < 125:
        suffix = (" Une recette et le conte, le mythe ou l'album qui l'accompagne, sur le blog À table."
                  if art["cat"] != "notes"
                  else " Notes de lecture sur la nourriture dans les livres pour enfants, blog À table.")
        desc_text = (desc_text + suffix)[:158].rstrip()
    desc = desc_text.replace('"', "&quot;")
    img = f"{DOMAIN}{art['img']}" if art["img"] else OG_FALLBACK

    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": chapeau,
        "image": img,
        "author": {"@type": "Person", "name": "Maud Lenoir"},
        "publisher": {
            "@type": "Organization", "name": "Mythes & Marmites",
            "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/images/logo-orange.svg"},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "url": url,
        "articleSection": CAT_LABEL.get(art["cat"], ""),
    }
    if art["dateISO"]:
        ld["datePublished"] = art["dateISO"]

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title_plain}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{img}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="article">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title_plain}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="/images/favicon-orange.svg">
<link rel="apple-touch-icon" href="/images/icon-192.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/style.css?v=3">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>

{header}

<main id="main">
<div class="band"><div class="wrap" style="padding-top:52px;padding-bottom:72px">
{art['html']}
</div></div>
</main>

{footer}

<script src="/script.js"></script>
</body>
</html>
"""


def main():
    if sys.platform != "darwin":
        print("Ce script nécessite macOS (osascript -l JavaScript). Abandon.")
        return 1

    pages = run_jxa(extract_pure_js())
    header, footer = header_footer()

    written = []
    for art in pages:
        doc = build_page(art, header, footer)
        out_dir = os.path.join(ROOT, "a-table", art["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(doc)
        written.append(f"/a-table/{art['slug']}/")

    print(f"{len(written)} pages d'article générées :")
    for w in written:
        print("  -", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
