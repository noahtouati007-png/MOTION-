"""Affichette A5 paysage « Toilettes hors service » (charte Galzin).

Usage : python3 build.py  ->  galzin-toilettes-hors-service-A5.svg (1 unité = 0,1 mm, 210 x 148 mm).
Pictogramme 100 % vectoriel.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

W, H = 2100, 1480
CH, CR, R = C["chocolat"], C["creme"], C["rouge"]


def picto_wc(cx, cy):
    """Cuvette WC de profil + panneau d'interdiction."""
    wc = (f'<g fill="{CH}">'
          f'<rect x="{cx + 40}" y="{cy - 200}" width="90" height="190" rx="14"/>'          # réservoir
          f'<path d="M{cx - 150} {cy - 10}H{cx + 130}V{cy + 20}C{cx + 130} {cy + 110} {cx + 40} {cy + 140} '
          f'{cx - 10} {cy + 140}L{cx + 10} {cy + 210}H{cx - 110}L{cx - 80} {cy + 120}C{cx - 130} {cy + 90} '
          f'{cx - 150} {cy + 50} {cx - 150} {cy + 20}Z"/>'                                  # cuvette
          f'<rect x="{cx - 160}" y="{cy - 40}" width="300" height="34" rx="12"/></g>')       # abattant
    r, d = 300, 212
    return (wc + f'<g fill="none" stroke="{R}" stroke-width="40" stroke-linecap="round">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/><path d="M{cx - d} {cy - d}L{cx + d} {cy + d}"/></g>')


def affiche():
    L = [f'<g id="FOND"><rect width="{W}" height="{H}" fill="{CR}"/></g>']
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{CH}" d="M0 0H{W}V250C1600 330 1000 200 520 290C300 330 120 335 0 320Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="10" d="M0 370C120 385 300 375 520 335'
        f'C1000 245 1600 375 {W} 295"/>'
        f'<path fill="{CH}" d="M0 1330C700 1240 1400 1380 {W} 1280V{H}H0Z"/>'
        '</g>')
    L.append('<g id="PICTO">' + picto_wc(560, 820) + '</g>')
    L.append(
        '<g id="TEXTES">'
        + logo(60, 22, 270)
        + text(1210, 195, "À NOTRE AIMABLE CLIENTÈLE", 120, CR)
        + text(1460, 720, "TOILETTES", 250, CH)
        + f'<g transform="rotate(-3 1460 880)"><rect x="1000" y="790" width="920" height="190" rx="50" '
          f'fill="url(#OrangeRouge)"/></g>'
        + text(1460, 935, "HORS SERVICE", 150, CR, rot=-3)
        + text(1460, 1130, "Nous vous prions de nous excuser", 64, CH, HEROICA, bold=True)
        + text(1460, 1210, "pour la gêne occasionnée.", 64, CH, HEROICA, bold=True)
        + text(W / 2, 1425, "Merci de votre compréhension", 58, CR, HEROICA, italic=True, bold=True)
        + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - Toilettes hors service A5")


if __name__ == "__main__":
    s = affiche()
    (HERE / "galzin-toilettes-hors-service-A5.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.2f} Mo")
