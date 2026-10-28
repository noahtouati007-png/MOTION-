"""Stop-trottoir recto/verso Galzin, version produits Galzin et typo élégante.

Usage : python3 build.py  ->  galzin-stop-trottoir-recto-verso.svg (à ouvrir dans Illustrator).
Format d'une face : 54 x 125 cm (5400 x 12500, 1 unité = 0,1 mm), fenêtre en arche. Les deux faces
sont côte à côte (groupes RECTO / VERSO). Ovales de prix livrés vides.
Typo : titres produits en Heroica, petites accroches en Impact espacé entre tirets.
"""
import base64
import io
import sys
from html import escape
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "_kit-galzin"))
from build import C, IMPACT, HEROICA, ovale_prix, svg  # noqa: E402

SW, SH = 5400, 12500
AX0, AX1, ATOP, ABOT = 620, 4780, 340, 11330
AR = (AX1 - AX0) / 2
MID = SW / 2


def href(name, max_px=1000):
    im = Image.open(HERE / "images" / f"{name}.png")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def image(name, x, y, w, h, max_px=1000, rot=0):
    tr = f' transform="rotate({rot} {x + w/2:.0f} {y + h/2:.0f})"' if rot else ""
    return (f'<image id="{name}" x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'preserveAspectRatio="xMidYMid meet"{tr} xlink:href="{href(name, max_px)}"/>')


def text(x, y, txt, size, fill, font=IMPACT, anchor="middle", italic=False, bold=False, spacing=0):
    st = ' font-style="italic"' if italic else ""
    wt = ' font-weight="bold"' if bold else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size:.0f}" fill="{fill}"{st}{wt}{ls}>{escape(txt, quote=False)}</text>')


def accroche(cx, y, txt, color, size=180):
    """Petite accroche Impact espacée, encadrée de tirets (style « du matin »)."""
    half = len(txt) * size * 0.32 + 120
    t = (f'<g fill="none" stroke="{color}" stroke-width="16" stroke-linecap="round">'
         f'<path d="M{cx - half} {y - size*0.33:.0f}h-220"/><path d="M{cx + half} {y - size*0.33:.0f}h220"/></g>')
    return t + text(cx, y, txt, size, color, spacing=size * 0.18)


def arche():
    return f'M{AX0} {ATOP + AR}A{AR} {AR} 0 0 1 {AX1} {ATOP + AR}V{ABOT}H{AX0}Z'


def folliet(cx, y, w):
    h = w * 468 / 1812
    return image("folliet-logo-blanc", cx - w / 2, y, w, h, 1812)


def face(contenu, prefix):
    L = [f'<g id="FOND"><rect width="{SW}" height="{SH}" fill="{C["chocolat"]}"/>'
         f'<path d="{arche()}" fill="{C["creme"]}"/></g>', contenu,
         '<g id="LOGO_MENTIONS">'
         f'<image id="galzin-logo" x="{MID - 1000:.0f}" y="600" width="2000" height="2000" '
         f'xlink:href="{href("galzin-logo", 1743)}"/>'
         + folliet(MID, ABOT + 280, 2300)
         + text(AX1, ABOT + 160, "Photos non contractuelles", 90, C["creme"], HEROICA, "end", italic=True)
         + '</g>']
    return "\n".join(L).replace('id="', f'id="{prefix}_')


def recto():
    v = (f'<g id="VAGUES" clip-path="url(#Arche)">'
         f'<path fill="{C["chocolat"]}" d="M0 5550C1400 5150 2800 5850 {SW} 5350V8450C3800 8900 2200 8200 0 8700Z"/>'
         f'<path fill="none" stroke="{C["caramel"]}" stroke-width="30" d="M0 5470C1400 5070 2800 5770 {SW} 5270"/>'
         f'<path fill="none" stroke="{C["caramel"]}" stroke-width="30" d="M0 8790C2200 8290 3800 8990 {SW} 8540"/></g>')
    t = ('<g id="TEXTES_PHOTOS">'
         # 1. café + croissant
         + accroche(MID, 2950, "LE DUO", C["caramel"])
         + text(MID, 3480, "Café + Croissant", 440, C["chocolat"], HEROICA, bold=True)
         + image("croissant-galzin", 700, 3750, 2600, 1750, 1000)
         + image("gobelet", 2300, 3650, 1300, 1640, 800)
         # 2. 3 viennoiseries
         + accroche(MID, 6120, "AU CHOIX", C["cuivre_clair"])
         + text(MID, 6650, "3 Viennoiseries", 470, C["creme"], HEROICA, bold=True)
         + image("croissant-galzin", 650, 6950, 1800, 1210, 1000)
         + image("chocolatine", 1720, 7250, 1500, 1060, 1000, rot=4)
         + image("feuillete-pomme", 3150, 6950, 1550, 900, 1000, rot=10)
         # 3. sandwich / salade + boisson
         + accroche(MID, 9330, "LE MIDI", C["caramel"])
         + text(1680, 9850, "Sandwich", 330, C["chocolat"], HEROICA, bold=True)
         + text(3720, 9850, "Salade", 330, C["chocolat"], HEROICA, bold=True)
         + text(1680, 10080, "+ boisson", 190, C["caramel"], HEROICA, italic=True, bold=True)
         + text(3720, 10080, "+ boisson", 190, C["caramel"], HEROICA, italic=True, bold=True)
         + f'<path d="M{MID} 9600V11150" stroke="{C["caramel"]}" stroke-width="14"/>'
         + image("sandwich-seul", 700, 10180, 1650, 890, 1000, rot=-6)
         + image("canette", 2150, 10150, 420, 800, 600, rot=8)
         + image("salade", 2950, 10170, 1300, 970, 1000)
         + image("canette", 4170, 10300, 380, 720, 600, rot=-8)
         + '</g>')
    p = ('<g id="PRIX">'
         + ovale_prix(4150, 4950, 460, 250, "", "cuivre", rot=-6)
         + ovale_prix(1350, 8150, 560, 300, "", "cuivre", rot=5)
         + ovale_prix(1680, 11120, 400, 210, "", "cuivre", rot=-4)
         + ovale_prix(3720, 11120, 400, 210, "", "cuivre", rot=-4)
         + '</g>')
    return face(v + t + p, "RECTO")


def verso():
    v = (f'<g id="VAGUES" clip-path="url(#Arche)">'
         f'<path fill="{C["chocolat"]}" d="M0 6950C1500 6500 3200 7300 {SW} 6700V{SH}H0Z"/>'
         f'<path fill="none" stroke="{C["caramel"]}" stroke-width="30" d="M0 6870C1500 6420 3200 7220 {SW} 6620"/>'
         f'<path fill="{C["caramel"]}" d="M0 9300C1500 9000 3200 9600 {SW} 9200V10700C3200 11000 1500 10500 0 10850Z"/>'
         '</g>')
    t = ('<g id="TEXTES_PHOTOS">'
         + accroche(MID, 3050, "FORMULE", C["caramel"])
         + text(MID, 3700, "Espresso", 620, C["chocolat"], HEROICA, bold=True)
         + image("croissant-galzin", 650, 4150, 2600, 1750, 1000)
         + image("espresso", 2000, 4550, 2200, 1780, 1000)
         + accroche(MID, 7700, "FORMULE", C["cuivre_clair"])
         + text(MID, 8300, "Petit-déjeuner", 520, C["creme"], HEROICA, bold=True)
         # même composition qu'avant (tasse Folliet + jus), avec le croissant Galzin
         + image("formule-petit-dej", 950, 8550, 3500, 2740, 1000)
         + '</g>')
    p = ('<g id="PRIX">'
         + ovale_prix(3950, 4250, 560, 300, "", "cuivre", rot=-6)
         + ovale_prix(1350, 8900, 520, 280, "", "cuivre", rot=5)
         + '</g>')
    return face(v + t + p, "VERSO")


def stop_trottoir():
    gap = 600
    body = (f'<defs><clipPath id="Arche"><path d="{arche()}"/></clipPath></defs>'
            f'<g id="RECTO">{recto()}</g>'
            f'<g id="VERSO" transform="translate({SW + gap} 0)">{verso()}</g>')
    return svg(SW * 2 + gap, SH, body, "Galzin - Stop-trottoir recto et verso")


if __name__ == "__main__":
    s = stop_trottoir()
    (HERE / "galzin-stop-trottoir-recto-verso.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
