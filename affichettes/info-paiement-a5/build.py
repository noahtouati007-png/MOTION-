"""Affichette A5 paysage « Moyens de paiement » (charte Galzin, voir ../_kit-galzin/CHARTE.md).

Usage : python3 build.py  ->  galzin-info-paiement-A5.svg (à ouvrir dans Illustrator).
Unités : 1 unité = 0,1 mm (A5 paysage = 2100 x 1480). Pictogrammes 100 % vectoriels.
"""
import base64
import io
import sys
from html import escape
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "_kit-galzin"))
from build import C, IMPACT, HEROICA, svg  # noqa: E402

W, H = 2100, 1480


def href(name, max_px=700):
    im = Image.open(HERE / "images" / f"{name}.png")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def text(x, y, txt, size, fill, font=IMPACT, anchor="middle", italic=False, bold=False):
    st = ' font-style="italic"' if italic else ""
    wt = ' font-weight="bold"' if bold else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size:.0f}" fill="{fill}"{st}{wt}>{escape(txt, quote=False)}</text>')


def interdit(cx, cy, r=230):
    """Panneau d'interdiction : cercle + barre rouges."""
    d = r * 0.707
    return (f'<g fill="none" stroke="{C["rouge"]}" stroke-width="34" stroke-linecap="round">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<path d="M{cx - d:.0f} {cy - d:.0f}L{cx + d:.0f} {cy + d:.0f}"/></g>')


def billet(cx, cy):
    return (f'<g id="picto-billet" transform="rotate(-8 {cx} {cy})">'
            f'<rect x="{cx - 250}" y="{cy - 135}" width="500" height="270" rx="26" fill="{C["sable"]}" '
            f'stroke="{C["chocolat"]}" stroke-width="14"/>'
            f'<circle cx="{cx - 150}" cy="{cy}" r="70" fill="none" stroke="{C["caramel"]}" stroke-width="12"/>'
            + text(cx + 60, cy + 55, "100€", 150, C["chocolat"], HEROICA, bold=True) + '</g>'
            + interdit(cx, cy))


def cheque(cx, cy):
    lignes = "".join(f'<path d="M{cx - 200} {cy + dy}H{cx + x2}"/>' for dy, x2 in ((-30, 200), (30, 60), (90, 200)))
    return (f'<g id="picto-cheque" transform="rotate(6 {cx} {cy})">'
            f'<rect x="{cx - 260}" y="{cy - 130}" width="520" height="260" rx="20" fill="{C["creme"]}" '
            f'stroke="{C["chocolat"]}" stroke-width="14"/>'
            + text(cx - 200, cy - 65, "CHÈQUE", 60, C["chocolat"], anchor="start")
            + f'<g stroke="{C["caramel"]}" stroke-width="10" stroke-linecap="round">{lignes}</g>'
            + f'<path d="M{cx + 90} {cy + 75}c30 -40 50 30 80 -10s40 20 60 0" fill="none" '
              f'stroke="{C["chocolat"]}" stroke-width="10" stroke-linecap="round"/></g>'
            + interdit(cx, cy))


def affiche():
    L = [f'<g id="FOND"><rect width="{W}" height="{H}" fill="{C["creme"]}"/></g>']
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{C["chocolat"]}" d="M0 0H{W}V290C1600 400 1000 230 520 320C300 360 120 370 0 355Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="10" d="M0 395C120 410 300 400 520 360'
        f'C1000 270 1600 440 {W} 330"/>'
        f'<path fill="{C["chocolat"]}" d="M0 1300C700 1200 1400 1350 {W} 1240V{H}H0Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="10" d="M0 1260C700 1160 1400 1310 {W} 1200"/>'
        '</g>')
    L.append(
        '<g id="TEXTES">'
        f'<image id="galzin-logo" x="60" y="25" width="310" height="310" xlink:href="{href("galzin-logo")}"/>'
        + text(1230, 200, "À NOTRE AIMABLE CLIENTÈLE", 130, C["creme"])
        + text(W / 2, 530, "Nous n'acceptons pas", 115, C["chocolat"], HEROICA, bold=True)
        + text(620, 1080, "LES BILLETS DE 100€ ET PLUS", 78, C["chocolat"])
        + text(1480, 1080, "LES CHÈQUES", 78, C["chocolat"])
        + text(W / 2, 1195, "Merci de votre compréhension.", 80, C["chocolat"], HEROICA, italic=True, bold=True)
        + text(W / 2, 1415, "CAISSE ÉQUIPÉE D'UN DÉTECTEUR DE FAUX BILLETS", 82, C["cuivre_clair"])
        + '</g>')
    def reduit(cx, cy, contenu, k=0.76):
        return f'<g transform="translate({cx} {cy}) scale({k}) translate({-cx} {-cy})">{contenu}</g>'

    L.append('<g id="PICTOS">' + reduit(620, 800, billet(620, 800)) + reduit(1480, 800, cheque(1480, 800)) + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - Info paiement A5")


if __name__ == "__main__":
    s = affiche()
    (HERE / "galzin-info-paiement-A5.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.2f} Mo")
