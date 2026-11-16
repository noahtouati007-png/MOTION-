"""Sticker de table « Réservé à notre clientèle » (charte Galzin), 100 x 90 mm, coins arrondis.

Usage : python3 build.py  ->  galzin-sticker-table-clientele.svg (1 unité = 0,1 mm).
Le fond déborde de 2 mm (fond perdu) ; la forme de découpe est le calque DECOUPE (contour seul).
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, HEROICA, svg, text, logo, tirets  # noqa: E402

W, H, R = 1000, 900, 60
CH, CR, CA, CC = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"]


def sticker():
    L = [f'<g id="FOND"><rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="{CR}"/>'
         f'<path fill="{CH}" d="M-20 700C250 640 650 760 {W + 20} 670V{H + 20}H-20Z"/>'
         f'<path fill="none" stroke="{CA}" stroke-width="8" d="M-20 665C250 605 650 725 {W + 20} 635"/></g>']
    L.append(
        '<g id="TEXTES">'
        + logo(330, 50, 340)
        + text(W / 2, 500, "Réservé à", 92, CH, HEROICA, bold=True)
        + text(W / 2, 600, "notre clientèle", 92, CH, HEROICA, bold=True)
        + tirets(150, 535, "g", CA, 0.7) + tirets(850, 535, "d", CA, 0.7)
        + text(W / 2, 810, "Merci de votre compréhension", 46, CC, HEROICA, italic=True, bold=True)
        + '</g>')
    L.append(f'<g id="DECOUPE"><rect x="0" y="0" width="{W}" height="{H}" rx="{R}" fill="none" '
             f'stroke="#E30F20" stroke-width="2"/></g>')
    return svg(W, H, "\n".join(L), "Galzin - Sticker table clientèle")


if __name__ == "__main__":
    (HERE / "galzin-sticker-table-clientele.svg").write_text(sticker(), encoding="utf-8")
