#!/usr/bin/env python3
"""Ratio de contraste WCAG 2.1 pour les paires premier plan / fond du site.

Charte Studio Mille Pages : fonds Pot au Lait, texte Encre ; accents vert,
jaune et violet des plis, Pomme d'Amour en accent secondaire. Aucune
couleur d'accent ne passe 3:1 sur Pot au Lait : elles servent d'aplats et
de petits éléments graphiques, jamais de couleur de texte sur fond clair.
Sur un aplat de couleur, le texte est en Encre ; sur vert et violet,
seulement en grand corps (24 px, ou 18,66 px gras).

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
    'pot-au-lait': '#F8F5F4', 'encre': '#534741', 'blanc': '#FFFFFF',
    'haricot': '#62B47E', 'haricot-2': '#55A270',
    'boucle-dor': '#F4CC71', 'boucle-dor-2': '#EBBE5C',
    'violet': '#9599EA', 'violet-2': '#A9ACEF', 'pomme': '#EB6755',
}

# (fg, bg, usage, seuil, remarque)
PAIRS = [
    ('encre', 'pot-au-lait', 'texte courant et liens', 4.5, ''),
    ('encre', 'blanc', 'texte sur carte blanche', 4.5, ''),
    ('pot-au-lait', 'encre', 'texte du pied de page, panneaux Encre', 4.5, ''),
    ('boucle-dor', 'encre', 'intitulés jaunes sur Encre', 4.5, ''),
    ('encre', 'boucle-dor', 'boutons, badges, panneaux jaunes', 4.5, ''),
    ('encre', 'boucle-dor-2', 'bouton au survol', 4.5, ''),
    ('encre', 'haricot', 'pastille d\'étape, surlignage du titre d\'accueil', 3.0, 'grand texte seulement'),
    ('encre', 'violet', 'pastille d\'étape', 3.0, 'grand texte seulement'),
    ('encre', 'violet-2', 'pastille d\'étape, appel de la page du jeu', 3.0, 'grand texte seulement (24 px minimum)'),
    ('haricot', 'pot-au-lait', 'vert sur fond clair', 3.0, 'jamais pour du texte'),
    ('violet', 'pot-au-lait', 'violet sur fond clair', 3.0, 'jamais pour du texte'),
    ('boucle-dor', 'pot-au-lait', 'jaune sur fond clair', 3.0, 'jamais pour du texte'),
    ('pomme', 'pot-au-lait', 'pomme sur fond clair', 3.0, 'jamais pour du texte'),
    ('pot-au-lait', 'boucle-dor', 'texte clair sur jaune', 3.0, 'interdit'),
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
