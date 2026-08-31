#!/usr/bin/env python3
"""Ratio de contraste WCAG 2.1 pour chaque paire premier plan / fond
utilisée par la feuille de style. Sert à vérifier le niveau AA (4,5:1
pour le texte courant, 3:1 pour le grand texte et les éléments d'interface)
et à produire le tableau du rapport de refonte.

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


def mix(hex_a, hex_b, t):
    """t=0 -> a, t=1 -> b, mélange linéaire sRGB (suffisant pour des teintes pâles)."""
    a = [int(hex_a.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(hex_b.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02X%02X%02X' % tuple(round(x + (y - x) * t) for x, y in zip(a, b))


PAL = {
    'lait': '#F8F5F4', 'encre': '#534741',
    'pomme': '#EB6755', 'haricot': '#62B47E', 'reverie': '#9599EA', 'or': '#F4CC71',
    # variantes foncées, réservées au texte / aux aplats de bouton : mêmes teintes,
    # assombries pour atteindre AA (non négociable dans le brief)
    'pomme-fonce': '#B93A27', 'haricot-fonce': '#2C744A', 'reverie-fonce': '#4E53C6',
    # variantes pâles, pour les fonds de section et de carte (le corps de texte
    # reste sur un fond très clair)
    'creme': '#F8F5F4',
    'vert-pale': '#EAF3EC', 'violet-pale': '#EFEFFB',
    'pomme-pale': '#FBEBE7', 'haricot-pale': '#E6F2E9', 'reverie-pale': '#ECECFA', 'or-pale': '#FBF2DC',
}

# paires (fg, bg, usage, seuil) — seuil 4.5 texte courant, 3.0 grand texte / UI
PAIRS = [
    ('encre', 'lait', 'corps de texte sur crème', 4.5),
    ('encre', 'vert-pale', 'corps de texte sur vert pâle (section)', 4.5),
    ('encre', 'violet-pale', 'corps de texte sur violet pâle (section)', 4.5),
    ('encre', 'pomme-pale', 'texte de carte sur pêche pâle', 4.5),
    ('encre', 'haricot-pale', 'texte de carte sur vert pâle', 4.5),
    ('encre', 'reverie-pale', 'texte de carte sur violet pâle', 4.5),
    ('encre', 'or-pale', 'texte de carte sur jaune pâle', 4.5),
    ('pomme-fonce', 'lait', 'titre h2 / lien sur crème', 3.0),
    ('pomme-fonce', 'vert-pale', 'lien sur section vert pâle', 4.5),
    ('pomme-fonce', 'violet-pale', 'lien sur section violet pâle', 4.5),
    ('haricot-fonce', 'lait', 'titre h2 vert sur crème', 3.0),
    ('haricot-fonce', 'vert-pale', 'titre h2 vert sur vert pâle', 3.0),
    ('reverie-fonce', 'lait', 'titre h2 violet sur crème', 3.0),
    ('reverie-fonce', 'violet-pale', 'titre h2 violet sur violet pâle', 3.0),
    ('lait', 'pomme-fonce', 'texte de bouton plein (primaire)', 4.5),
    ('lait', 'haricot-fonce', 'texte de bouton plein (vert)', 4.5),
    ('lait', 'encre', 'texte de bouton plein (encre) / survol', 4.5),
    ('encre', 'or', 'texte sur panneau jaune plein', 4.5),
    ('lait', 'pomme', 'texte blanc sur aplat pomme vif (À ÉVITER)', 4.5),
]


def main():
    print(f"{'usage':44s} {'fg':>14s} {'bg':>12s}  ratio  seuil  état")
    print('-' * 92)
    worst = []
    for fg, bg, usage, thr in PAIRS:
        r = ratio(PAL[fg], PAL[bg])
        ok = r >= thr
        flag = 'OK ' if ok else 'ÉCHEC'
        if not ok:
            worst.append(usage)
        print(f"{usage:44s} {PAL[fg]:>14s} {PAL[bg]:>12s}  {r:4.2f}  {thr:4.1f}  {flag}")
    print()
    if worst:
        print("À revoir :", ', '.join(worst))
    else:
        print("Toutes les paires en usage passent leur seuil.")


if __name__ == '__main__':
    main()
