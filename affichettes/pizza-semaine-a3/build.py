"""Affiche A3 « Pizza de la semaine » (charte Galzin, voir ../_kit-galzin/CHARTE.md).

Usage : python3 build.py  ->  galzin-pizza-semaine-A3.svg (à ouvrir dans Illustrator).
On ne dit pas quelle pizza : elle change chaque semaine et s'affiche en magasin.
Unités : 1 unité = 0,1 mm (A3 = 2970 x 4200).
"""
import base64
import io
import math
import sys
from html import escape
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "_kit-galzin"))
from build import C, IMPACT, HEROICA, ovale_prix, badge_fidelite, svg  # noqa: E402

W, H = 2970, 4200


def href(name, max_px=1000):
    im = Image.open(HERE / "images" / f"{name}.png")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def image(name, x, y, w, h, max_px=1000):
    return (f'<image id="{name}" x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'preserveAspectRatio="xMidYMid meet" xlink:href="{href(name, max_px)}"/>')


def text(x, y, txt, size, fill, font=IMPACT, anchor="middle", italic=False, bold=False, rot=0):
    st = ' font-style="italic"' if italic else ""
    wt = ' font-weight="bold"' if bold else ""
    tr = f' transform="rotate({rot} {x:.0f} {y:.0f})"' if rot else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size:.0f}" fill="{fill}"{st}{wt}{tr}>{escape(txt, quote=False)}</text>')


def eclat(cx, cy, R, r, n=18):
    """Éclat (starburst) comme sur l'affiche OFFRE+."""
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rad = R if i % 2 == 0 else r
        pts.append(f"{cx + rad * math.cos(a):.0f} {cy + rad * math.sin(a):.0f}")
    return f'<path fill="url(#OrangeRouge)" d="M{"L".join(pts)}Z"/>'


def affiche():
    L = [f'<g id="FOND"><rect width="{W}" height="{H}" fill="{C["creme"]}"/></g>']
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{C["chocolat"]}" d="M0 0H{W}V480C2300 680 1500 400 800 560C450 640 200 650 0 610Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="14" d="M0 660C200 700 450 690 800 610'
        f'C1500 450 2300 730 {W} 530"/>'
        f'<path fill="{C["chocolat"]}" d="M0 3520C900 3320 1900 3680 {W} 3370V{H}H0Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="14" d="M0 3460C900 3260 1900 3620 {W} 3310"/>'
        '</g>')

    def etiquette(x, y, txt, fill=C["chocolat"], w=620):
        return (f'<g transform="rotate(-5 {x + w/2} {y})"><rect x="{x}" y="{y - 85}" width="{w}" height="170" '
                f'rx="45" fill="{fill}"/></g>' + text(x + w / 2, y + 45, txt, 120, C["creme"], rot=-5))

    # frise : 3 semaines passées, chacune sa pizza
    cases = [(90, "pizza-poulet", "SEMAINE 1"), (1045, "pizza-chevre", "SEMAINE 2"), (2000, "pizza-thon", "SEMAINE 3")]
    ph = ''.join(image(img, x, 1830, 880, 520, 900) for x, img, _ in cases)
    tags = ''.join(etiquette(x + 130, 1800, lab, w=560) for x, _, lab in cases)
    fl = (f'<g id="FLECHES" fill="none" stroke="{C["chocolat"]}" stroke-width="24" stroke-linecap="round" '
          f'stroke-linejoin="round">'
          f'<path d="M940 2120H1030M985 2075L1035 2120L985 2165"/>'
          f'<path d="M1895 2120H1985M1940 2075L1990 2120L1940 2165"/>'
          f'<path d="M2440 2410C2000 2440 1700 2520 1500 2720"/><path d="M1520 2610L1495 2725L1610 2715"/></g>')
    # la semaine en cours : mystère
    myst = (f'<g id="CETTE_SEMAINE"><circle cx="1000" cy="3000" r="430" fill="url(#OrangeRouge)" '
            f'stroke="{C["creme"]}" stroke-width="24"/>'
            + text(1000, 3225, "?", 680, C["creme"])
            + etiquette(600, 2560, "CETTE SEMAINE", C["chocolat"], 800) + '</g>')
    L.append('<g id="PHOTOS">' + ph + '</g>')
    L.append(
        '<g id="TEXTES">'
        + text(W / 2, 320, "UNE NOUVELLE RECETTE CHAQUE SEMAINE", 160, C["creme"])
        + text(W / 2, 1180, "LA PIZZA", 600, C["chocolat"])
        + f'<g transform="rotate(-3 {W/2} 1430)"><rect x="{W/2 - 900}" y="1270" width="1800" height="330" '
          f'rx="80" fill="{C["chocolat"]}"/></g>'
        + text(W / 2, 1515, "de la semaine", 250, C["cuivre_clair"], HEROICA, italic=True, bold=True, rot=-3)
        + tags + fl + myst
        + text(W / 2, 3800, "À DÉCOUVRIR EN MAGASIN !", 240, C["creme"])
        + text(W / 2, 3920, "Sa recette change chaque semaine et s'affiche en boutique", 88,
               C["cuivre_clair"], HEROICA, italic=True, bold=True)
        + '</g>')
    L.append(
        '<g id="PRIX">'
        + f'<g transform="rotate(-6 2250 2740)"><rect x="1910" y="2650" width="680" height="180" rx="50" '
          f'fill="{C["chocolat"]}"/></g>'
        + text(2250, 2780, "seulement", 125, C["creme"], HEROICA, italic=True, bold=True, rot=-6)
        + ovale_prix(2250, 3090, 520, 280, "8,90€", "cuivre", rot=-6)
        + '</g>')
    L.append(
        '<g id="LOGO_MENTIONS">'
        f'<image id="galzin-logo" x="110" y="3950" width="230" height="230" xlink:href="{href("galzin-logo", 700)}"/>'
        + badge_fidelite(400, 3985, 540)
        + text(W - 60, H - 50, "Photos non contractuelles", 50, C["creme"], HEROICA, "end", italic=True)
        + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - Pizza de la semaine A3")


if __name__ == "__main__":
    s = affiche()
    (HERE / "galzin-pizza-semaine-A3.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
