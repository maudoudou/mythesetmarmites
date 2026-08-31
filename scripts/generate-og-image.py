#!/usr/bin/env python3
"""Génère images/og-share.png (1200x630), l'image de partage utilisée
par les balises Open Graph et Twitter Card de toutes les pages.

Construite à partir du logo vectoriel (images/logo-orange.svg, rasterisé
via QuickLook — macOS uniquement) et des polices de la marque, sur le
fond crème du site. Ne modifie ni ne supprime aucun fichier du dossier
images : n'ajoute que og-share.png à côté des fichiers existants.

Nécessite macOS (qlmanage) pour rasteriser le SVG. À relancer avec
`python3 scripts/generate-og-image.py` si le logo change.
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_SVG = os.path.join(ROOT, 'images', 'logo-orange.svg')
FONT_SERIF_ITALIC = os.path.join(ROOT, 'fonts', 'IMFellEnglish-Italic.ttf')
OUT_PATH = os.path.join(ROOT, 'images', 'og-share.png')

LAIT = (248, 245, 244)      # --lait
ENCRE = (83, 71, 65)        # --encre
POMME = (235, 103, 85)      # --pomme (couleur exacte du logo-orange.svg)

W, H = 1200, 630


def rasterize_svg(svg_path, size=2400):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ['qlmanage', '-t', '-s', str(size), '-o', tmp, svg_path],
            check=True, capture_output=True,
        )
        png_name = os.path.basename(svg_path) + '.png'
        return Image.open(os.path.join(tmp, png_name)).convert('RGB')


def matte_against_white(img, fg_color):
    """Reconstruit un canal alpha pour un aplat de couleur fg_color
    détouré sur fond blanc opaque (ce que renvoie qlmanage), par
    démélange linéaire connu (observed = a*fg + (1-a)*white)."""
    rgba = img.convert('RGBA')
    px = rgba.load()
    fr, fg_, fb = fg_color
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, _ = px[x, y]
            # alpha par canal, moyenné sur les canaux où fg diffère du blanc
            alphas = []
            for c, fc in ((r, fr), (g, fg_), (b, fb)):
                if fc < 255:
                    alphas.append((255 - c) / (255 - fc))
            a = max(0.0, min(1.0, sum(alphas) / len(alphas))) if alphas else 0.0
            a255 = round(a * 255)
            if a255 == 0:
                px[x, y] = (255, 255, 255, 0)
            else:
                px[x, y] = (fr, fg_, fb, a255)
    return rgba


def autocrop(img, pad=20):
    bbox = img.getbbox()
    if not bbox:
        return img
    l, t, r, b = bbox
    l, t = max(0, l - pad), max(0, t - pad)
    r, b = min(img.width, r + pad), min(img.height, b + pad)
    return img.crop((l, t, r, b))


def main():
    if sys.platform != 'darwin':
        print("Ce script nécessite macOS (qlmanage). Abandon.")
        return 1

    raw = rasterize_svg(LOGO_SVG)
    logo = matte_against_white(raw, POMME)
    logo = autocrop(logo)

    canvas = Image.new('RGB', (W, H), LAIT)
    draw = ImageDraw.Draw(canvas)

    # Filet pointillé signature, en haut et en bas du visuel
    dot_r = 3
    for y in (70, H - 70):
        x = 60
        while x < W - 60:
            draw.ellipse([x, y - dot_r, x + dot_r * 2, y + dot_r * 2], fill=(83, 71, 65, 40))
            x += 22

    # Logo centré, redimensionné pour occuper une largeur confortable
    target_w = 620
    ratio = target_w / logo.width
    logo = logo.resize((target_w, round(logo.height * ratio)), Image.LANCZOS)
    lx = (W - logo.width) // 2
    ly = (H - logo.height) // 2 - 30
    canvas.paste(logo, (lx, ly), logo)

    # Sous-titre
    font = ImageFont.truetype(FONT_SERIF_ITALIC, 34)
    subtitle = "Studio d'édition et de récits"
    bbox = draw.textbbox((0, 0), subtitle, font=font)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) // 2
    ty = ly + logo.height + 26
    draw.text((tx, ty), subtitle, font=font, fill=ENCRE)

    canvas.save(OUT_PATH, 'PNG', optimize=True)
    print(f"Image de partage écrite : {OUT_PATH} ({canvas.width}x{canvas.height})")
    return 0


if __name__ == '__main__':
    sys.exit(main())
