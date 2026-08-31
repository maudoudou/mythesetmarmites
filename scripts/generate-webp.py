#!/usr/bin/env python3
"""Génère une version WebP de chaque image lourde (jpg/png > 80 Ko)
référencée par le site, à côté du fichier original — jamais à sa
place : aucun fichier existant n'est renommé, déplacé ou supprimé.

Les dimensions ne sont pas changées, seul le format de compression
change (qualité 82, pas de perte visible à l'écran). C'est un choix
volontaire : redimensionner en plus aurait encore réduit le poids de
certaines photos, mais c'est une décision de recadrage qui touche au
rendu et qui revient à l'autrice (voir RAPPORT-REFONTE.md).

À relancer avec `python3 scripts/generate-webp.py` si une nouvelle
photo lourde est ajoutée.
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(ROOT, 'images')
THRESHOLD_BYTES = 80 * 1024
QUALITY = 82

# Uniquement les fichiers réellement utilisés par le site (voir
# index.html) : pas la peine de convertir des images orphelines.
REFERENCED = {
    'photos/poules-web.png', 'photos/marteau-jardin-web.jpg', 'photos/master-lettres-web.jpg',
    'photos/suede-web.jpg', 'photos/AFC-forum-web.jpg', 'photos/scandi-web.jpg',
    'photos/panier-web.jpg', 'photos/recettes-web.jpg', 'photos/diplome-bachelor-web.jpg',
    'photos/design-web.jpg', 'photos/manger-design-web.jpg', 'photos/pain-epices-web.jpg',
    'photos/livre-hugo-web.jpg', 'photos/soupe-web.jpg', 'photos/galette-web.jpg',
    'photos/cartes-web.jpg', 'photos/portrait-maud-web.jpg', 'photos/europe-web.jpg',
    'photos/institut-couture-web.jpg', 'photos/pain-poule-rousse-web.jpg', 'photos/prez-institut-web.jpg',
    'LOGO-LATELIERPHOTO-version2-CMJN.png', 'studio_sauvage_yoga_cantine-300x232.png',
}


def main():
    written = []
    skipped = []
    for rel in sorted(REFERENCED):
        src = os.path.join(IMAGES_DIR, rel)
        if not os.path.isfile(src):
            print(f"absent, ignoré : {rel}")
            continue
        if os.path.getsize(src) < THRESHOLD_BYTES:
            continue
        dst = os.path.splitext(src)[0] + '.webp'
        im = Image.open(src)
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if 'transparency' in im.info or im.mode == 'P' else 'RGB')
        im.save(dst, 'WEBP', quality=QUALITY, method=6)
        before = os.path.getsize(src)
        after = os.path.getsize(dst)

        # Certains JPEG sont déjà si compressés que WebP, à qualité
        # comparable, ne fait pas mieux : dans ce cas, la version WebP
        # ne sert à rien, on la retire et on garde l'original tel quel.
        if after >= before:
            os.remove(dst)
            skipped.append((rel, before, after))
            print(f"{rel:48s} WebP plus lourd ({after/1024:.0f} Ko >= {before/1024:.0f} Ko) : original conservé, pas de .webp")
            continue

        written.append((rel, before, after))
        print(f"{rel:48s} {before/1024:7.0f} Ko -> {after/1024:7.0f} Ko  ({100 - after/before*100:.0f} % de moins)")

    if written:
        tot_before = sum(b for _, b, _ in written)
        tot_after = sum(a for _, _, a in written)
        print(f"\n{len(written)} fichiers convertis, {tot_before/1024/1024:.1f} Mo -> {tot_after/1024/1024:.1f} Mo")
    if skipped:
        print(f"{len(skipped)} fichier(s) sans gain, laissé(s) en l'état : " + ', '.join(r for r, _, _ in skipped))
    return 0


if __name__ == '__main__':
    sys.exit(main())
