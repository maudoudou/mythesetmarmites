#!/usr/bin/env python3
"""Prépare pour le web les logos Studio Mille Pages fournis dans
images/charte/, sans les redessiner.

Pourquoi
--------
Les SVG de la charte écrivent « STUDIO » et « Mille Pages » avec de vrais
caractères (<text>) en Pacaembu ExtraBold et IM Fell English. Affichés par
une balise <img>, ils ne peuvent pas charger les polices du site : chez un
visiteur qui n'a pas ces polices installées, le logo s'afficherait dans une
police de remplacement. Ce script convertit chaque <text> en tracés
vectoriels, avec les polices exactes :

  - Pacaembu ExtraBold : le sous-ensemble de police incorporé dans le
    fichier .ai correspondant (les lettres S, T, U, D, I, O du logo) ;
  - IM Fell English : fonts/IMFellEnglish-Regular.ttf, la police du site.

Formes, couleurs, positions, transformations et ordre des plis restent
ceux du fichier d'origine : seule la manière de décrire les lettres change.

Fichiers écrits (les originaux de images/charte/ ne sont jamais touchés) :

  images/charte/web/smp-horizontal-couleur.svg   en-tête
  images/charte/web/smp-horizontal-lait.svg      pied de page (fond Encre)
  images/charte/web/smp-carre-couleur.svg        image de partage
  images/charte/web/favicon.svg                  favicon (rond couleur)
  images/icons/favicon-16.png, favicon-32.png    favicon PNG
  images/icons/apple-touch-icon.png              180 x 180, fond Pot au Lait
  images/icons/icon-192.png, icon-512.png        manifeste, fond Pot au Lait
  images/og-studio-mille-pages.png               1200 x 630, logo carré
                                                 sur Pot au Lait

Zone de protection : la largeur d'un pli autour des plis (favicon,
icônes) et autour du logo carré (image de partage).

Dépendances : fontTools et uharfbuzz (`pip3 install --user fonttools
uharfbuzz`), Playwright avec Chromium pour les PNG. À relancer avec
`python3 scripts/generate-logos.py` si un fichier de la charte change.
"""
import io
import os
import re
import sys
import zlib
import xml.etree.ElementTree as ET

import uharfbuzz as hb
from fontTools.cffLib import CFFFontSet
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARTE = os.path.join(ROOT, 'images', 'charte')
WEB = os.path.join(CHARTE, 'web')
ICONS = os.path.join(ROOT, 'images', 'icons')
FELL = os.path.join(ROOT, 'fonts', 'IMFellEnglish-Regular.ttf')
SVG_NS = 'http://www.w3.org/2000/svg'

POT_AU_LAIT = '#F8F5F4'

ET.register_namespace('', SVG_NS)


# ---------------------------------------------------------------- polices

def pacaembu_from_ai(ai_path):
    """Sous-ensemble Pacaembu ExtraBold (CFF) incorporé dans le .ai."""
    data = open(ai_path, 'rb').read()
    objs = {int(m.group(1)): m.group(2)
            for m in re.finditer(rb'(\d+) 0 obj(.*?)endobj', data, re.S)}
    for body in objs.values():
        ref = re.search(rb'/FontFile3\s+(\d+) 0 R', body)
        if not ref or b'Pacaembu' not in body:
            continue
        head, stream = objs[int(ref.group(1))].split(b'stream', 1)
        stream = stream.lstrip(b'\r\n')
        length = int(re.search(rb'/Length (\d+)', head).group(1))
        raw = zlib.decompress(stream[:length]) if b'FlateDecode' in head else stream[:length]
        cff = CFFFontSet()
        cff.decompile(io.BytesIO(raw), None)
        return cff[cff.fontNames[0]]
    raise SystemExit(f'Pacaembu introuvable dans {ai_path}')


class Pacaembu:
    """Une lettre à la fois : le logo pose chaque lettre de STUDIO seule."""
    upem = 1000

    def __init__(self, ai_path):
        self.font = pacaembu_from_ai(ai_path)

    def run(self, text):
        out, x = [], 0
        for ch in text:
            cs = self.font.CharStrings[ch]
            pen = SVGPathPen(None)
            cs.draw(pen)
            out.append((x, pen.getCommands()))
            x += cs.width
        return out, x


class Fell:
    """IM Fell English, composée par HarfBuzz (crénage compris)."""

    def __init__(self, path):
        blob = hb.Blob.from_file_path(path)
        self.hbfont = hb.Font(hb.Face(blob))
        self.tt = TTFont(path)
        self.upem = self.tt['head'].unitsPerEm
        self.glyphset = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()

    def run(self, text, spacing_units=0):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, {'kern': True, 'liga': True})
        out, x = [], 0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            pen = SVGPathPen(self.glyphset)
            self.glyphset[self.order[info.codepoint]].draw(pen)
            out.append((x + pos.x_offset, pen.getCommands()))
            x += pos.x_advance + spacing_units
        return out, x


# ------------------------------------------------------- texte -> tracés

def css_classes(root):
    """Propriétés des classes .stN du <style> Illustrator."""
    style = root.find(f'.//{{{SVG_NS}}}style')
    rules = {}
    if style is None:
        return rules
    for sel, body in re.findall(r'([^{}]+)\{([^}]*)\}', style.text):
        props = dict((k.strip(), v.strip()) for k, v in
                     (p.split(':', 1) for p in body.split(';') if ':' in p))
        for s in sel.split(','):
            rules.setdefault(s.strip().lstrip('.'), {}).update(props)
    return rules


def text_to_group(el, rules, fonts):
    """Remplace un <text> par un <g> de <path>, à l'identique."""
    tspan = el.find(f'{{{SVG_NS}}}tspan')
    content = (tspan.text if tspan is not None else el.text) or ''
    props = dict(rules.get(el.get('class', ''), {}))
    for k in ('font-family', 'font-size', 'letter-spacing', 'text-anchor', 'fill'):
        if el.get(k) is not None:
            props[k] = el.get(k)
    size = float(props['font-size'].replace('px', ''))
    family = props['font-family']
    font = fonts['fell'] if 'fell' in family.lower() else fonts['pacaembu']

    spacing = props.get('letter-spacing', '0').strip()
    spacing = float(spacing[:-2]) * size if spacing.endswith('em') else float(spacing or 0)
    scale = size / font.upem
    if isinstance(font, Fell):
        glyphs, advance = font.run(content, spacing / scale)
    else:
        glyphs, advance = font.run(content)

    x = float((tspan if tspan is not None else el).get('x', el.get('x', 0)))
    y = float((tspan if tspan is not None else el).get('y', el.get('y', 0)))
    if props.get('text-anchor') == 'middle':
        x -= advance * scale / 2

    g = ET.Element(f'{{{SVG_NS}}}g')
    for attr in ('class', 'transform'):
        if el.get(attr):
            g.set(attr, el.get(attr))
    if el.get('fill'):
        g.set('fill', el.get('fill'))
    g.set('aria-hidden', 'true')
    for gx, d in glyphs:
        if not d:
            continue
        p = ET.SubElement(g, f'{{{SVG_NS}}}path')
        p.set('transform', f'translate({x + gx * scale:.3f} {y:.3f}) scale({scale:.5f} {-scale:.5f})')
        p.set('d', d)
    return g


def outline(svg_name, ai_name, title):
    src = os.path.join(CHARTE, svg_name)
    tree = ET.parse(src)
    root = tree.getroot()
    fonts = {'fell': Fell(FELL), 'pacaembu': Pacaembu(os.path.join(CHARTE, ai_name))}
    rules = css_classes(root)

    for parent in root.iter():
        for i, child in enumerate(list(parent)):
            tag = child.tag.split('}')[-1]
            if tag == 'metadata':
                parent.remove(child)
            elif tag == 'text':
                parent.remove(child)
                parent.insert(i, text_to_group(child, rules, fonts))
    # Les propriétés de police du <style> ne servent plus.
    style = root.find(f'.//{{{SVG_NS}}}style')
    if style is not None:
        style.text = re.sub(r'\s*(font-[a-z-]+|letter-spacing|isolation)\s*:[^;]*;', '', style.text)
    for k in [k for k in root.attrib if k.startswith('{') or k in ('id',)]:
        del root.attrib[k]
    root.set('role', 'img')
    t = ET.Element(f'{{{SVG_NS}}}title')
    t.text = title
    root.insert(0, t)

    os.makedirs(WEB, exist_ok=True)
    out = os.path.join(WEB, svg_name)
    xml = ET.tostring(root, encoding='unicode')
    xml = re.sub(r'\sxmlns:c2pa="[^"]*"', '', xml)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(xml + '\n')
    print('écrit :', os.path.relpath(out, ROOT))
    return out


def favicon_svg():
    """Le rond couleur, plis inchangés, cadré avec une largeur de pli de
    marge tout autour (zone de protection)."""
    src = open(os.path.join(CHARTE, 'smp-rond-couleur.svg'), encoding='utf-8').read()
    polys = re.findall(r'<polygon[^>]*/>', src)
    style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
    xs, ys = [], []
    for p in polys:
        pts = [float(v) for v in re.search(r'points="([^"]+)"', p).group(1).split()]
        xs += pts[0::2]
        ys += pts[1::2]
    pli = (max(xs) - min(xs)) / 6
    w, h = max(xs) - min(xs) + 2 * pli, max(ys) - min(ys) + 2 * pli
    side = max(w, h)
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    vb = f'{cx - side / 2:.1f} {cy - side / 2:.1f} {side:.1f} {side:.1f}'
    style = re.sub(r'\s+', ' ', style).strip()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
           f'<style>{style}</style>' + ''.join(polys) + '</svg>\n')
    out = os.path.join(WEB, 'favicon.svg')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(svg)
    print('écrit :', os.path.relpath(out, ROOT))
    return out


# --------------------------------------------------------------- images

def rasterize(favicon, carre):
    from playwright.sync_api import sync_playwright

    def file_url(p):
        # Données en ligne : une page set_content() ne lit pas file://.
        import base64
        return 'data:image/svg+xml;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

    os.makedirs(ICONS, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(device_scale_factor=1)

        def shoot(size, out, bg=None):
            page.set_viewport_size({'width': size, 'height': size})
            body_bg = bg or 'transparent'
            page.set_content(
                f'<html><body style="margin:0;background:{body_bg}">'
                f'<img src="{file_url(favicon)}" style="display:block;width:{size}px;height:{size}px">'
                '</body></html>')
            page.wait_for_load_state('load')
            page.screenshot(path=out, omit_background=bg is None)
            print('écrit :', os.path.relpath(out, ROOT))

        shoot(16, os.path.join(ICONS, 'favicon-16.png'))
        shoot(32, os.path.join(ICONS, 'favicon-32.png'))
        shoot(180, os.path.join(ICONS, 'apple-touch-icon.png'), POT_AU_LAIT)
        shoot(192, os.path.join(ICONS, 'icon-192.png'), POT_AU_LAIT)
        shoot(512, os.path.join(ICONS, 'icon-512.png'), POT_AU_LAIT)

        # Image de partage : logo carré centré sur Pot au Lait. Le carré
        # mesure 1120 x 1130 ; ses plis font 170 de large (zone de
        # protection). Hauteur du logo : 430 px, soit 430/1130*170 = 65 px
        # de zone de protection, largement tenue dans 630 px.
        page.set_viewport_size({'width': 1200, 'height': 630})
        page.set_content(
            f'<html><body style="margin:0;width:1200px;height:630px;background:{POT_AU_LAIT};'
            'display:grid;place-items:center">'
            f'<img src="{file_url(carre)}" style="height:430px;width:auto;display:block">'
            '</body></html>')
        page.wait_for_load_state('load')
        out = os.path.join(ROOT, 'images', 'og-studio-mille-pages.png')
        page.screenshot(path=out)
        print('écrit :', os.path.relpath(out, ROOT))
        browser.close()


def main():
    outline('smp-horizontal-couleur.svg', 'smp-horizontal-couleur.ai', 'Studio Mille Pages')
    outline('smp-horizontal-lait.svg', 'smp-horizontal-lait.ai', 'Studio Mille Pages')
    carre = outline('smp-carre-couleur.svg', 'smp-carre-couleur.ai', 'Studio Mille Pages')
    fav = favicon_svg()
    rasterize(fav, carre)
    return 0


if __name__ == '__main__':
    sys.exit(main())
