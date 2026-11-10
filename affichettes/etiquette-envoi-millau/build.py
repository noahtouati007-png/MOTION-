"""Étiquette d'envoi interne A5 paysage, version simple (texte brut, très lisible, sans DA).

Usage : python3 build.py  ->  galzin-etiquette-envoi-millau-A5.svg (1 unité = 0,1 mm, 210 x 148 mm).
"""
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
W, H = 2100, 1480
LIGNES = [  # (texte, taille, gras)
    ("POUR : MALICIA", 210, True),
    ("MILLAU", 210, True),
    ("CLÉ USB NOAH", 170, False),
    ("DE : FABRÈGUES", 150, False),
]


def etiquette():
    y, out = 300, []
    for txt, size, gras in LIGNES:
        w = ' font-weight="bold"' if gras else ""
        out.append(f'<text x="{W/2}" y="{y}" text-anchor="middle" font-family="Arial" font-size="{size}"'
                   f'{w} fill="#000000">{escape(txt)}</text>')
        y += size + 110
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="148mm" viewBox="0 0 {W} {H}">\n'
            f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>\n' + "\n".join(out) + '\n</svg>\n')


if __name__ == "__main__":
    (HERE / "galzin-etiquette-envoi-millau-A5.svg").write_text(etiquette(), encoding="utf-8")
