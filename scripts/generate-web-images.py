#!/usr/bin/env python3
"""(Re)génère les WebP d'affichage : redimensionnés à une largeur maximale
raisonnable pour le web et compressés en WebP. Les fichiers d'origine
(.jpg / .png) ne sont jamais touchés — seuls les .webp dérivés, à côté,
sont écrits ou réécrits.

Différence avec generate-webp.py : celui-ci ne changeait que le format, pas
les dimensions ; certaines photos faisaient 5000-6000 px de large pour un
affichage de 350-1000 px. Ici on plafonne la largeur.

`python3 scripts/generate-web-images.py`
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "images")
QUALITY = 78

# relpath (sous images/) -> largeur max en px pour l'affichage web
TARGETS = {
    # pleines largeurs / héros
    "photos/poules-web.png": 1500,
    "photos/suede-web.jpg": 1500,
    "photos/pain-poule-rousse-web.jpg": 1400,
    "photos/panier-web.jpg": 1400,
    "photos/portrait-maud-web.jpg": 1300,
    # recettes (héros d'article, 1080x400 déjà raisonnable mais on recompresse)
    "photos/galette-web.jpg": 1200,
    "photos/soupe-web.jpg": 1200,
    "photos/pain-epices-web.jpg": 1200,
    # rail du jeu / studio (~340-520 px d'affichage)
    "photos/recettes-web.jpg": 1100,
    "photos/jetons-web.jpg": 1100,
    "photos/cartes-web.jpg": 1100,
    "photos/scandi-web.jpg": 1100,
    "photos/europe-web.jpg": 1000,
    # galerie parcours (~340 px d'affichage)
    "photos/design-web.jpg": 1000,
    "photos/manger-design-web.jpg": 1000,
    "photos/prez-institut-web.jpg": 1000,
    "photos/AFC-forum-web.jpg": 1000,
    "photos/photos-photos-web.jpg": 1000,
    "photos/diplome-bachelor-web.jpg": 1000,
    # logos bitmap d'établissements
    "LOGO-LATELIERPHOTO-version2-CMJN.png": 1000,
    "studio_sauvage_yoga_cantine-300x232.png": 600,
}


def main():
    total_before = total_after = 0
    for rel, maxw in sorted(TARGETS.items()):
        src = os.path.join(IMAGES, rel)
        if not os.path.isfile(src):
            print(f"absent, ignoré : {rel}")
            continue
        dst = os.path.splitext(src)[0] + ".webp"
        im = Image.open(src)
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if ("transparency" in im.info or im.mode == "P") else "RGB")
        if im.width > maxw:
            h = round(im.height * maxw / im.width)
            im = im.resize((maxw, h), Image.LANCZOS)
        im.save(dst, "WEBP", quality=QUALITY, method=6)
        before = os.path.getsize(src)
        after = os.path.getsize(dst)
        total_before += before
        total_after += after
        print(f"{rel:46s} {before/1024:7.0f} Ko -> {after/1024:6.0f} Ko  ({im.width}px)")
    print(f"\noriginaux {total_before/1024/1024:.1f} Mo -> webp {total_after/1024/1024:.1f} Mo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
