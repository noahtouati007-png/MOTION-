"""Étiquette d'envoi interne A5 paysage (charte Galzin) : clé USB de Noah, Fabrègues -> Malicia à Millau.

Usage : python3 build.py  ->  galzin-etiquette-envoi-millau-A5.svg (1 unité = 0,1 mm, 210 x 148 mm).
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

W, H = 2100, 1480
CH, CR, CA = C["chocolat"], C["creme"], C["caramel"]


def ligne(y, etiquette, valeur, sous=""):
    o = (text(200, y, etiquette, 62, CA, anchor="start", spacing=6)
         + text(200, y + 130, valeur, 130, CH, HEROICA, "start", bold=True))
    if sous:
        o += text(200, y + 210, sous, 60, CH, HEROICA, "start", italic=True, bold=True)
    return o


def etiquette():
    L = [f'<g id="FOND"><rect width="{W}" height="{H}" fill="{CR}"/></g>']
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{CH}" d="M0 0H{W}V250C1600 330 1000 200 520 290C300 330 120 335 0 320Z"/>'
        f'<path fill="none" stroke="{CA}" stroke-width="10" d="M0 370C120 385 300 375 520 335'
        f'C1000 245 1600 375 {W} 295"/>'
        f'<path fill="{CH}" d="M0 1360C700 1290 1400 1400 {W} 1320V{H}H0Z"/>'
        '</g>')
    L.append(
        '<g id="TEXTES">'
        + logo(60, 22, 270)
        + text(1210, 200, "ENVOI – À RETIRER", 140, CR)
        + ligne(520, "À REMETTRE À", "Malicia", "Galzin Millau")
        + ligne(880, "CONTENU", "Clé USB de Noah")
        + f'<path d="M1300 470V1220" stroke="{CA}" stroke-width="8" stroke-linecap="round"/>'
        + text(1650, 560, "EXPÉDIÉ DEPUIS", 62, CA, spacing=6)
        + text(1650, 700, "Fabrègues", 120, CH, HEROICA, bold=True)
        + f'<g transform="rotate(-4 1650 950)"><rect x="1400" y="870" width="500" height="160" rx="40" '
          f'fill="url(#OrangeRouge)"/></g>'
        + text(1650, 985, "FRAGILE", 100, CR, rot=-4)
        + text(W / 2, 1445, "Merci de remettre en main propre", 54, CR, HEROICA, italic=True, bold=True)
        + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - Étiquette envoi Millau A5")


if __name__ == "__main__":
    s = etiquette()
    (HERE / "galzin-etiquette-envoi-millau-A5.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.2f} Mo")
