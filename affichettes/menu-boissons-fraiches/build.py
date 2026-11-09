"""Menu « Boissons fraîches » Galzin (reprise du visuel fourni), 40 x 60 cm.

Usage : python3 build.py  ->  galzin-menu-boissons-fraiches.svg (à ouvrir dans Illustrator,
puis Fichier > Enregistrer sous > Adobe Illustrator (.ai)).
Dessiné sur la grille du visuel d'origine (1024 x 1536) puis mis à l'échelle 40 x 60 cm.
Chaque ligne de la carte est un groupe : nom, pointillés, prix.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, HEROICA, svg, text, image  # noqa: E402

W, H = 4000, 6000          # 40 x 60 cm
K = W / 1024               # échelle grille d'origine -> 0,1 mm
CH = C["chocolat"]

BOISSONS = [
    ("Fuzetea 33 cl", "2.20€"), ("Fuzetea 40 cl", "2.80€"), ("Coca Cola 33 cl", "2.20€"),
    ("Coca Cola 50 cl", "2.80€"), ("Coca Zéro 33 cl", "2.20€"), ("Coca Zéro 50 cl", "2.80€"),
    ("Coca Cherry 33 cl", "2.20€"), ("Coca Cherry 50 cl", "2.80€"), ("Coca Cola 1.25 l", "4.10€"),
    ("Fanta 33 cl", "2.20€"), ("Fanta dragon 33 cl", "2.20€"), ("Fanta 50 cl", "2.80€"),
    ("Tropico mini", "1.70€"), ("Tropico 33cl", "2.20€"), ("Tropico 40cl", "2.80€"),
    ("Sprite 33 cl", "2.20€"), ("Sprite 50 cl", "2.80€"), ("Monster mangue 50 cl", "3.20€"),
    ("Redbull 25 cl", "3.20€"), ("Maid orange 33 cl", "2.20€"), ("Maid pomme 33 cl", "2.20€"),
    ("Heineken 33 cl", "2.80€"), ("Desperados 33 cl", "3.80€"), ("Bière artisanale", "3.80€"),
    ("Volvic fraise ou citron 50 cl", "2.80€"), ("San Pellegrino / Perrier 50 cl", "2.50€"),
    ("Eau 50 cl", "1.50€"), ("Eau 1.5 l", "2.50€"), ("Limonade 27,5 cl", "2.80€"),
]


def brin(cx, cy, sens=1, s=1.0):
    """Petit brin de laurier vectoriel (tige + 3 paires de feuilles)."""
    out = f'<g transform="translate({cx} {cy}) scale({sens * s} {s})" fill="{CH}">'
    out += f'<path d="M-34 4C-10 2 10 -2 34 -6" fill="none" stroke="{CH}" stroke-width="2.4"/>'
    for i, x in enumerate((-20, -2, 16)):
        out += (f'<ellipse cx="{x}" cy="{-8 + i}" rx="8" ry="3.4" transform="rotate(-38 {x} {-8 + i})"/>'
                f'<ellipse cx="{x + 2}" cy="{8 - i * 2}" rx="8" ry="3.4" transform="rotate(38 {x + 2} {8 - i * 2})"/>')
    return out + f'<ellipse cx="38" cy="-7" rx="7" ry="3" transform="rotate(-10 38 -7)"/></g>'


def cadre():
    """Double cadre aux coins rentrants, comme l'original."""
    def contour(m, r):
        x0, y0, x1, y1 = m, m, 1024 - m, 1536 - m
        return (f'M{x0 + r} {y0}H{x1 - r}A{r} {r} 0 0 0 {x1} {y0 + r}V{y1 - r}A{r} {r} 0 0 0 {x1 - r} {y1}'
                f'H{x0 + r}A{r} {r} 0 0 0 {x0} {y1 - r}V{y0 + r}A{r} {r} 0 0 0 {x0 + r} {y0}Z')
    return (f'<g id="CADRE" fill="none" stroke="{CH}">'
            f'<path d="{contour(16, 26)}" stroke-width="2.2"/><path d="{contour(30, 22)}" stroke-width="1.4"/></g>')


def carte():
    o = []
    y, pas = 445, 34.3
    x_nom, x_prix, size = 386, 940, 23
    for nom, prix in BOISSONS:
        fin_nom = x_nom + len(nom) * size * 0.42
        o.append(f'<g id="ligne-{nom.split()[0].lower()}">'
                 + text(x_nom, y, nom, size, CH, HEROICA, "start")
                 + f'<path d="M{fin_nom + 8:.0f} {y - 1}H{x_prix - 66}" stroke="{CH}" stroke-width="1.6" '
                   f'stroke-dasharray="0.1 5" stroke-linecap="round"/>'
                 + text(x_prix, y, prix, size, CH, HEROICA, "end") + '</g>')
        y += pas
    return '<g id="CARTE">' + "".join(o) + '</g>'


def menu():
    L = [f'<rect width="1024" height="1536" fill="#FFFFFF"/>', cadre()]
    L.append('<g id="PHOTO">' + image(HERE / "images/photo-coca.png", 34, 270, 351, 1140, 1400, id="photo-coca") + '</g>')
    L.append(
        '<g id="ENTETE">'
        + image(HERE / "images/galzin-logo.png", 412, 50, 230, 230, 900, id="galzin-logo")
        + f'<g stroke="{CH}" stroke-width="1.4"><path d="M50 189H205"/><path d="M288 189H388"/>'
          f'<path d="M665 189H738"/><path d="M820 189H975"/></g>'
        + brin(247, 188, 1) + brin(778, 188, -1)
        + text(662, 382, "Boissons fraîches", 86, CH, HEROICA, italic=True, bold=True)
        + f'<path d="M580 410C615 402 655 400 680 404" fill="none" stroke="{CH}" stroke-width="3.2" '
          f'stroke-linecap="round"/>'
        + '</g>')
    L.append(carte())
    L.append('<g id="PIED">' + brin(420, 1438, 1, 1.25) + brin(556, 1438, -1, 1.25)
             + text(488, 1494, "Dans la limite des stocks disponibles", 17, CH, HEROICA) + '</g>')
    body = f'<g transform="scale({K:.6f})">' + "\n".join(L) + '</g>'
    return svg(W, H, body, "Galzin - Menu boissons fraîches")


if __name__ == "__main__":
    s = menu()
    (HERE / "galzin-menu-boissons-fraiches.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
