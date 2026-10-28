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


def tirets(cx, cy, cote, color):
    """Petits traits décoratifs de part et d'autre d'une accroche (comme sur la maquette)."""
    sg = -1 if cote == "g" else 1
    return (f'<g fill="none" stroke="{color}" stroke-width="16" stroke-linecap="round">'
            f'<path d="M{cx} {cy - 40}l{sg * 90} -40"/><path d="M{cx} {cy}l{sg * 120} 0"/>'
            f'<path d="M{cx} {cy + 40}l{sg * 90} 40"/></g>')


def ligne_compo(items, y, size, color, gap=None):
    """Éléments Impact séparés par des « + », centrés (largeur Impact ~0,45 em/lettre)."""
    gap = gap or size * 1.6
    ws = [len(t) * size * 0.45 for t in items]
    x = (W - sum(ws) - gap * (len(items) - 1)) / 2
    out = ""
    for i, (t, w) in enumerate(zip(items, ws)):
        out += text(x + w / 2, y, t, size, color)
        x += w
        if i < len(items) - 1:
            out += plus(x + gap / 2, y - size * 0.36, size * 0.8, C["cuivre_clair"])
            x += gap
    return out


def affiche():
    L = [f'<g id="FOND"><rect width="{W}" height="{H}" fill="{C["chocolat"]}"/></g>']
    # vague caramel = la table sous le plateau
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{C["caramel"]}" d="M0 1640C900 1440 2000 1720 {W} 1460V2420C2000 2580 1000 2360 0 2520Z"/>'
        f'<path fill="none" stroke="{C["cuivre_clair"]}" stroke-width="14" '
        f'd="M0 1590C900 1390 2000 1670 {W} 1410"/>'
        '</g>')

    L.append(
        '<g id="PHOTOS">'
        + image("plateau", 110, 1290, 2750, 1228, 1200)
        + image("espresso", 260, 2780, 600, 400)
        + image("cafe-allonge", 1185, 2760, 600, 420)
        + image("chocolat-chaud", 2110, 2730, 600, 450)
        + '</g>')

    L.append(
        '<g id="TEXTES">'
        f'<image id="galzin-logo" x="1185" y="50" width="600" height="600" xlink:href="{href("galzin-logo", 900)}"/>'
        + text(1350, 960, "LA FORMULE", 320, C["creme"])
        + text(1350, 1250, "du matin", 300, C["cuivre_clair"], HEROICA, italic=True, bold=True, rot=-3)
        + tirets(700, 1150, "g", C["cuivre_clair"]) + tirets(2000, 1130, "d", C["cuivre_clair"])
        # boissons au choix
        + text(W / 2, 2720, "Avec votre boisson chaude", 150, C["creme"], HEROICA, italic=True, bold=True)
        + tirets(560, 2670, "g", C["cuivre_clair"]) + tirets(2410, 2670, "d", C["cuivre_clair"])
        + f'<g stroke="{C["cuivre_clair"]}" stroke-width="6"><path d="M1020 2800V3290"/><path d="M1950 2800V3290"/></g>'
        + text(560, 3280, "EXPRESSO", 105, C["creme"])
        + text(1485, 3280, "CAFÉ ALLONGÉ", 105, C["creme"])
        + text(2410, 3280, "CHOCOLAT CHAUD", 105, C["creme"])
        # encadré viennoiserie
        + f'<rect x="80" y="3350" width="{W - 160}" height="650" rx="40" fill="{C["chocolat_fonce"]}" '
          f'stroke="{C["cuivre_clair"]}" stroke-width="8"/>'
        + '<g id="VIENNOISERIES">' + image("croissant", 1720, 3380, 560, 430, 900, rot=-8)
        + image("chocolatine", 1930, 3560, 450, 320, 900, rot=6) + '</g>'
        + f'<g id="PLUS_1"><circle cx="320" cy="3600" r="190" fill="url(#OrangeRouge)" stroke="{C["creme"]}" '
          f'stroke-width="14"/>' + text(320, 3670, "+1€", 175, C["creme"]) + '</g>'
        + text(560, 3540, "Avec un croissant", 118, C["creme"], HEROICA, "start", italic=True, bold=True)
        + text(560, 3665, "ou un pain au chocolat", 118, C["creme"], HEROICA, "start", italic=True, bold=True)
        + text(560, 3770, "+ LE BEURRE ET LA CONFITURE", 78, C["cuivre_clair"], anchor="start")
        + ligne_compo(["1 BOISSON CHAUDE", "PAIN", "BEURRE", "CONFITURE", "CROISSANT OU PAIN AU CHOCOLAT"],
                      3950, 58, C["creme"])
        + '</g>')
    L.append(
        '<g id="PRIX">'
        + ovale_prix(2480, 930, 360, 220, "3,80€", "cuivre", rot=-8)
        + pastille(2640, 3480, 600, 130, C["caramel"], "FORMULE AVEC VIENNOISERIE", 52, C["chocolat_fonce"])
        + ovale_prix(2650, 3720, 260, 150, "4,80€", "cuivre", size=170, rot=-5)
        + '</g>')
    L.append(
        '<g id="LOGO_MENTIONS">'
        + badge_fidelite(100, 4030, 480)
        + text(W - 60, H - 40, "Photos non contractuelles", 45, C["creme"], HEROICA, "end", italic=True)
        + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - La formule du matin A3")


if __name__ == "__main__":
    s = affiche()
    (HERE / "galzin-formule-matin-A3.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
