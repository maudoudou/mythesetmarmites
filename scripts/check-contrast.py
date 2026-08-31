#!/usr/bin/env python3
"""Ratio de contraste WCAG 2.1 pour les paires premier plan / fond du site.

Le site est fidèle à la charte : les teintes vives (--pomme, --haricot,
--reverie) servent d'accent et d'aplat de bloc. Comme sur beaucoup de
chartes colorées, certaines ne passent pas 4,5:1 en petit texte sur crème
(2,3 à 2,9:1) — c'est un choix d'identité assumé. Les blocs qui portent un
paragraphe long utilisent soit --or (texte foncé, lisible), soit --encre
(texte clair), soit un encart crème (.card__inset).

`python3 scripts/check-contrast.py`
"""


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_):
    h = hex_.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


PAL = {
    'lait': '#F8F5F4', 'encre': '#534741',
    'pomme': '#EB6755', 'haricot': '#62B47E', 'reverie': '#9599EA', 'or': '#F4CC71',
}

# (fg, bg, usage, seuil, remarque)
PAIRS = [
    ('encre', 'lait', 'corps de texte sur crème', 4.5, ''),
    ('lait', 'encre', 'texte sur bloc --encre (brun)', 4.5, ''),
    ('encre', 'or', 'texte sur bloc --or (doré)', 4.5, ''),
    ('lait', 'pomme', 'titre / texte court blanc sur bloc --pomme', 3.0,
     'grand texte seulement ; paragraphe long -> encart crème'),
    ('lait', 'haricot', 'titre court blanc sur bloc --haricot', 3.0,
     'titre + icône seulement ; le paragraphe va dans .card__inset'),
    ('lait', 'reverie', 'titre court blanc sur bloc --reverie', 3.0,
     'titre + icône seulement ; le paragraphe va dans .card__inset'),
    ('pomme', 'lait', 'lien / titre de section corail sur crème', 3.0,
     'accent de charte, sous 4,5:1 en petit texte — assumé'),
    ('haricot', 'lait', 'accent vert sur crème', 3.0, 'accent de charte — assumé'),
    ('reverie', 'lait', 'accent violet sur crème', 3.0, 'accent de charte — assumé'),
    ('lait', 'pomme', 'texte de bouton .btn (blanc sur corail)', 3.0,
     'texte court et gras ; comme le site d\'origine'),
]


def main():
    print(f"{'usage':52s} {'ratio':>6s}  {'seuil':>5s}  état")
    print('-' * 100)
    for fg, bg, usage, thr, note in PAIRS:
        r = ratio(PAL[fg], PAL[bg])
        state = 'OK' if r >= thr else 'sous seuil'
        line = f"{usage:52s} {r:5.2f}  {thr:5.1f}  {state}"
        if note:
            line += f"   — {note}"
        print(line)


if __name__ == '__main__':
    main()
