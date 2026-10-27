"""Affiche A3 « Pizza de la semaine » (charte Galzin, voir ../_kit-galzin/CHARTE.md).

Usage : python3 build.py  ->  galzin-pizza-semaine-A3.svg (à ouvrir dans Illustrator).
On ne dit pas quelle pizza : elle change chaque semaine et s'affiche en magasin.
Unités : 1 unité = 0,1 mm (A3 = 2970 x 4200).
"""
import base64
import io
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


def affiche():
    L = [f'<g id="FOND"><rect width="{W}" height="{H}" fill="{C["creme"]}"/></g>']
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{C["chocolat"]}" d="M0 0H{W}V520C2300 720 1500 440 800 600C450 680 200 690 0 650Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="14" d="M0 700C200 740 450 730 800 650'
        f'C1500 490 2300 770 {W} 570"/>'
        f'<path fill="{C["chocolat"]}" d="M0 3380C800 3150 1700 3520 {W} 3150V{H}H0Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="14" d="M0 3320C800 3090 1700 3460 {W} 3090"/>'
        '</g>')
    L.append(
        '<g id="PHOTOS">'
        + image("pizza-chevre", -380, 1520, 1500, 900)
        + image("pizza-poulet", 1850, 1480, 1500, 900)
        + image("pizza-thon", 285, 1850, 2400, 1420)
        + '</g>')
    L.append(
        '<g id="TEXTES">'
        + text(W / 2, 330, "CHAQUE SEMAINE, UNE NOUVELLE", 175, C["creme"])
        + text(W / 2, 1180, "Pizza", 600, C["chocolat"], HEROICA, bold=True)
        + f'<g transform="rotate(-3 {W/2} 1390)"><rect x="{W/2 - 780}" y="1235" width="1560" height="310" '
          f'rx="70" fill="{C["turquoise"]}"/></g>'
        + text(W / 2, 1465, "de la semaine", 230, C["creme"], HEROICA, italic=True, bold=True, rot=-3)
        # pastille mystère
        + f'<g id="MYSTERE" transform="rotate(10 2480 1750)"><circle cx="2480" cy="1750" r="300" '
          f'fill="{C["chocolat"]}" stroke="{C["creme"]}" stroke-width="22"/>'
        + text(2480, 1930, "?", 520, C["creme"])
        + '</g>'
        + f'<g transform="rotate(-6 640 1660)"><rect x="40" y="1560" width="1200" height="210" rx="60" '
          f'fill="{C["chocolat"]}"/></g>'
        + text(640, 1700, "Laquelle cette semaine ?", 112, C["creme"], HEROICA, italic=True, bold=True, rot=-6)
        + text(W / 2, 3640, "À DÉCOUVRIR EN MAGASIN !", 235, C["creme"])
        + text(W / 2, 3780, "Son nom est affiché en boutique, chaque semaine une surprise", 92, C["creme"],
               HEROICA, italic=True, bold=True)
        + '</g>')
    L.append(
        '<g id="PRIX">'
        + f'<g transform="rotate(-5 2230 2830)"><rect x="1880" y="2735" width="700" height="190" rx="50" '
          f'fill="{C["chocolat"]}"/></g>'
        + text(2230, 2870, "seulement", 130, C["creme"], HEROICA, italic=True, bold=True, rot=-5)
        + ovale_prix(2230, 3170, 560, 290, "8,90€", "rouge", rot=-5)
        + '</g>')
    L.append(
        '<g id="LOGO_MENTIONS">'
        f'<image id="galzin-logo" x="120" y="3830" width="330" height="330" xlink:href="{href("galzin-logo", 700)}"/>'
        + badge_fidelite(520, 3880, 700)
        + text(W - 60, H - 50, "Photos non contractuelles", 50, C["creme"], HEROICA, "end", italic=True)
        + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - Pizza de la semaine A3")


if __name__ == "__main__":
    s = affiche()
    (HERE / "galzin-pizza-semaine-A3.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
