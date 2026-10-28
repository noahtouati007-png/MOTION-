"""Affiche A3 « La formule du matin » (charte Galzin, voir ../_kit-galzin/CHARTE.md).

Usage : python3 build.py  ->  galzin-formule-matin-A3.svg (à ouvrir dans Illustrator).
Formule 3,80€ : boisson chaude + pain + beurre + confiture. +1€ : croissant ou pain au chocolat (4,80€).
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
from build import C, IMPACT, HEROICA, ovale_prix, badge_fidelite, plus, svg  # noqa: E402

W, H = 2970, 4200


def href(name, max_px=900):
    im = Image.open(HERE / "images" / f"{name}.png")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def image(name, x, y, w, h, max_px=900, rot=0):
    tr = f' transform="rotate({rot} {x + w/2:.0f} {y + h/2:.0f})"' if rot else ""
    return (f'<image id="{name}" x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'preserveAspectRatio="xMidYMid meet"{tr} xlink:href="{href(name, max_px)}"/>')


def text(x, y, txt, size, fill, font=IMPACT, anchor="middle", italic=False, bold=False, rot=0):
    st = ' font-style="italic"' if italic else ""
    wt = ' font-weight="bold"' if bold else ""
    tr = f' transform="rotate({rot} {x:.0f} {y:.0f})"' if rot else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size:.0f}" fill="{fill}"{st}{wt}{tr}>{escape(txt, quote=False)}</text>')


def pastille(cx, cy, w, h, fill, txt, size, color, rot=-4, font=IMPACT, **kw):
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx - w/2:.0f}" y="{cy - h/2:.0f}" '
            f'width="{w}" height="{h}" rx="{h*0.3:.0f}" fill="{fill}"/></g>'
            + text(cx, cy + size * 0.36, txt, size, color, font, rot=rot, **kw))


def affiche():
    L = [f'<g id="FOND"><rect width="{W}" height="{H}" fill="{C["creme"]}"/></g>']
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{C["chocolat"]}" d="M0 0H{W}V720C2300 900 1500 650 800 810C450 890 200 890 0 860Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="14" d="M0 920C200 950 450 950 800 870'
        f'C1500 710 2300 960 {W} 780"/>'
        f'<path fill="{C["chocolat"]}" d="M0 3380C900 3200 1900 3480 {W} 3220V{H}H0Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="14" d="M0 3320C900 3140 1900 3420 {W} 3160"/>'
        '</g>')

    # Plateau : boisson chaude + pain + beurre + confiture
    assiette = '<g id="PLATEAU">' + image("plateau", 80, 1110, 2450, 1094, 1200) + '</g>'
    boissons = (
        '<g id="BOISSONS">'
        + image("espresso", 300, 2620, 620, 470)
        + image("cafe-allonge", 1175, 2600, 620, 490)
        + image("chocolat-chaud", 2060, 2560, 620, 540)
        + '</g>')
    vienno = ('<g id="VIENNOISERIES">'
              + image("croissant", 1800, 3260, 620, 480, 900, rot=-6)
              + image("chocolatine", 2300, 3350, 580, 420, 900, rot=6)
              + '</g>')
    L.append('<g id="PHOTOS">' + assiette + boissons + vienno + '</g>')

    def ligne_compo(items, y, size, gap=170):
        """Éléments Impact séparés par des « + », centrés (largeur Impact ~0,45 em/lettre)."""
        ws = [len(t) * size * 0.45 for t in items]
        x = (W - sum(ws) - gap * (len(items) - 1)) / 2
        out = ""
        for i, (t, w) in enumerate(zip(ws and items, ws)):
            out += text(x + w / 2, y, t, size, C["chocolat"])
            x += w
            if i < len(items) - 1:
                out += plus(x + gap / 2, y - size * 0.36, size * 0.8)
                x += gap
        return out

    compo = [("1 BOISSON CHAUDE", 480), ("PAIN", 1260), ("BEURRE", 1850), ("CONFITURE", 2470)]
    L.append(
        '<g id="TEXTES">'
        f'<image id="galzin-logo" x="110" y="90" width="600" height="600" xlink:href="{href("galzin-logo", 900)}"/>'
        + text(1850, 410, "LA FORMULE", 360, C["creme"])
        + text(1850, 660, "du matin", 250, C["cuivre_clair"], HEROICA, italic=True, bold=True, rot=-3)
        # composition de la formule
        + ligne_compo([t for t, _ in compo], 2330, 120)
        + text(W / 2, 2530, "Votre boisson chaude au choix", 150, C["chocolat"], HEROICA, italic=True, bold=True)
        + text(610, 3200, "EXPRESSO", 115, C["chocolat"])
        + text(1485, 3200, "CAFÉ ALLONGÉ", 115, C["chocolat"])
        + text(2370, 3200, "CHOCOLAT CHAUD", 115, C["chocolat"])
        # +1€ viennoiserie
        + f'<g id="PLUS_1"><circle cx="330" cy="3640" r="230" fill="url(#OrangeRouge)" stroke="{C["creme"]}" '
          f'stroke-width="16"/>' + text(330, 3720, "+1€", 210, C["creme"]) + '</g>'
        + text(620, 3600, "Avec un croissant", 125, C["creme"], HEROICA, "start", italic=True, bold=True)
        + text(620, 3740, "ou un pain au chocolat", 125, C["creme"], HEROICA, "start", italic=True, bold=True)
        + text(620, 3860, "+ LE BEURRE ET LA CONFITURE", 85, C["cuivre_clair"], anchor="start")
        + '</g>')
    L.append(
        '<g id="PRIX">'
        + ovale_prix(2470, 1030, 420, 240, "3,80€", "cuivre", rot=-6)
        + pastille(2350, 3820, 860, 150, C["caramel"], "FORMULE AVEC VIENNOISERIE", 80, C["chocolat_fonce"])
        + ovale_prix(2350, 4010, 360, 140, "4,80€", "cuivre", size=170, rot=-4)
        + '</g>')
    L.append(
        '<g id="LOGO_MENTIONS">'
        + badge_fidelite(110, 3960, 560)
        + text(1500, H - 30, "Photos non contractuelles", 45, C["creme"], HEROICA, italic=True)
        + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - La formule du matin A3")


if __name__ == "__main__":
    s = affiche()
    (HERE / "galzin-formule-matin-A3.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
