#!/usr/bin/env python3
"""Génère les icônes PNG (192x192 et 512x512) utilisées par
site.webmanifest, à partir de la marque déjà utilisée en favicon
(images/favicon-orange.svg). N'ajoute que des fichiers nouveaux dans
images/ (icon-192.png, icon-512.png) : aucun fichier existant n'est
modifié, renommé ou supprimé.

Nécessite macOS (qlmanage). À relancer avec
`python3 scripts/generate-app-icons.py` si la marque change.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = os.path.join(ROOT, 'images', 'favicon-orange.svg')
POMME = (235, 103, 85)
LAIT = (248, 245, 244)


def rasterize_svg(svg_path, size):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(['qlmanage', '-t', '-s', str(size), '-o', tmp, svg_path],
                        check=True, capture_output=True)
        return Image.open(os.path.join(tmp, os.path.basename(svg_path) + '.png')).convert('RGB')


def matte_against_white(img, fg_color):
    rgba = img.convert('RGBA')
    px = rgba.load()
    fr, fg_, fb = fg_color
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, _ = px[x, y]
            alphas = [(255 - c) / (255 - fc) for c, fc in ((r, fr), (g, fg_), (b, fb)) if fc < 255]
            a = max(0.0, min(1.0, sum(alphas) / len(alphas))) if alphas else 0.0
            a255 = round(a * 255)
            px[x, y] = (255, 255, 255, 0) if a255 == 0 else (fr, fg_, fb, a255)
    return rgba


def square_icon(mark, size, pad_ratio=0.18, bg=LAIT):
    """Place le mark (RGBA) centré sur un fond carré uni de `size`px,
    avec une marge, pour une icône d'app lisible sur toutes les plateformes."""
    canvas = Image.new('RGBA', (size, size), bg + (255,))
    pad = round(size * pad_ratio)
    box = size - 2 * pad
    ratio = min(box / mark.width, box / mark.height)
    mark = mark.resize((round(mark.width * ratio), round(mark.height * ratio)), Image.LANCZOS)
    x = (size - mark.width) // 2
    y = (size - mark.height) // 2
    canvas.paste(mark, (x, y), mark)
    return canvas.convert('RGB')


def main():
    if sys.platform != 'darwin':
        print("Ce script nécessite macOS (qlmanage). Abandon.")
        return 1

    raw = rasterize_svg(SVG, 1600)
    mark = matte_against_white(raw, POMME)
    bbox = mark.getbbox()
    if bbox:
        mark = mark.crop(bbox)

    for size in (192, 512):
        icon = square_icon(mark, size)
        out = os.path.join(ROOT, 'images', f'icon-{size}.png')
        icon.save(out, 'PNG', optimize=True)
        print(f"écrit : images/icon-{size}.png")
    return 0


if __name__ == '__main__':
    sys.exit(main())
