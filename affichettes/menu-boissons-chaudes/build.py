"""Menu « Boissons chaudes » Galzin, A4 (compagnon du menu « Boissons fraîches »).

Usage : python3 build.py  ->  galzin-menu-boissons-chaudes.svg (à ouvrir dans Illustrator,
puis Fichier > Enregistrer sous > Adobe Illustrator (.ai)).
Dessiné sur une grille 1024 x 1448 (proportions A4) puis mis à l'échelle 21 x 29,7 cm.
Chaque ligne de la carte est un groupe : nom, pointillés, prix.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, HEROICA, svg, text, image  # noqa: E402

W, H = 2100, 2970          # A4
GH = 1448                  # hauteur de la grille
K = W / 1024               # échelle grille d'origine -> 0,1 mm
CH = C["chocolat"]

BOISSONS = [  # None = espace entre deux familles
    ("Café", "1,60€"), ("Déca", "1,60€"), ("Café double", "2,50€"), ("Déca double", "2,50€"),
    ("Café crème", "2,80€"), ("Cappuccino", "2,80€"), None,
    ("Petit chocolat chaud", "2,30€"), ("Grand chocolat chaud", "2,80€"), None,
    ("Thés et infusions", "2,80€"),
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
        x0, y0, x1, y1 = m, m, 1024 - m, GH - m
        return (f'M{x0 + r} {y0}H{x1 - r}A{r} {r} 0 0 0 {x1} {y0 + r}V{y1 - r}A{r} {r} 0 0 0 {x1 - r} {y1}'
                f'H{x0 + r}A{r} {r} 0 0 0 {x0} {y1 - r}V{y0 + r}A{r} {r} 0 0 0 {x0 + r} {y0}Z')
    return (f'<g id="CADRE" fill="none" stroke="{CH}">'
            f'<path d="{contour(16, 26)}" stroke-width="2.2"/><path d="{contour(30, 22)}" stroke-width="1.4"/></g>')


def carte():
    o = []
    y, pas = 545, 66
    x_nom, x_prix, size = 420, 950, 36
    for item in BOISSONS:
        if item is None:
            y += pas * 0.6
            continue
        nom, prix = item
        fin_nom = x_nom + len(nom) * size * 0.45
        o.append(f'<g id="ligne-{nom.split()[0].lower()}">'
                 + text(x_nom, y, nom, size, CH, HEROICA, "start")
                 + f'<path d="M{fin_nom + 10:.0f} {y - 1}H{x_prix - 92}" stroke="{CH}" stroke-width="2" '
                   f'stroke-dasharray="0.1 7" stroke-linecap="round"/>'
                 + text(x_prix, y, prix, size, CH, HEROICA, "end") + '</g>')
        y += pas
    return '<g id="CARTE">' + "".join(o) + '</g>'


def menu():
    L = [f'<rect width="1024" height="{GH}" fill="#FFFFFF"/>', cadre()]
    # photo café (fournie), en colonne à gauche
    L.append('<defs><clipPath id="ClipPhoto"><rect x="40" y="300" width="330" height="1100" rx="18"/></clipPath></defs>'
             '<g id="PHOTO" clip-path="url(#ClipPhoto)">'
             + image(HERE / "images/photo-cafe.jpg", 40, 300, 330, 1100, 1400, id="photo-cafe").replace("meet", "slice")
             + '</g>')
    L.append(
        '<g id="ENTETE">'
        + image(HERE / "images/galzin-logo.png", 412, 50, 230, 230, 900, id="galzin-logo")
        + f'<g stroke="{CH}" stroke-width="1.4"><path d="M50 189H205"/><path d="M288 189H388"/>'
          f'<path d="M665 189H738"/><path d="M820 189H975"/></g>'
        + brin(247, 188, 1) + brin(778, 188, -1)
        + text(676, 400, "Boissons chaudes", 76, CH, HEROICA, italic=True, bold=True)
        + f'<path d="M590 428C625 420 665 418 690 422" fill="none" stroke="{CH}" stroke-width="3.2" '
          f'stroke-linecap="round"/>'
        + '</g>')
    L.append(carte())
    L.append('<g id="PIED">' + brin(620, 1300, 1, 1.25) + brin(756, 1300, -1, 1.25)
             + text(688, 1360, "Photos non contractuelles", 18, CH, HEROICA, italic=True) + '</g>')
    body = f'<g transform="scale({K:.6f})">' + "\n".join(L) + '</g>'
    return svg(W, H, body, "Galzin - Menu boissons chaudes")


if __name__ == "__main__":
    s = menu()
    (HERE / "galzin-menu-boissons-chaudes.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
