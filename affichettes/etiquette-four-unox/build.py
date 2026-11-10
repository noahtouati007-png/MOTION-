"""Étiquette A6 paysage « Attention » pour les fours Unox Speed (charte Galzin).

Usage : python3 build.py  ->  galzin-etiquette-four-unox-A6.svg (1 unité = 0,1 mm, 148 x 105 mm).
Pictogrammes 100 % vectoriels.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

W, H = 1480, 1050
CH, CR, R = C["chocolat"], C["creme"], C["rouge"]


def four(cx, cy, interieur=""):
    """Four vu de face : caisson, porte vitrée, poignée, bouton."""
    return (f'<g fill="none" stroke="{CH}" stroke-width="14" stroke-linejoin="round">'
            f'<rect x="{cx - 130}" y="{cy - 95}" width="260" height="190" rx="18" fill="{CR}"/>'
            f'<rect x="{cx - 105}" y="{cy - 70}" width="160" height="140" rx="10" fill="#FFFFFF"/>'
            f'<path d="M{cx + 85} {cy - 60}V{cy + 60}"/></g>{interieur}')


def interdit(cx, cy, r=150):
    d = r * 0.707
    return (f'<g fill="none" stroke="{R}" stroke-width="22" stroke-linecap="round">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/><path d="M{cx - d:.0f} {cy - d:.0f}L{cx + d:.0f} {cy + d:.0f}"/></g>')


def vide(cx, cy):
    """Four allumé à vide : ondes de chaleur dans une enceinte vide."""
    ondes = "".join(f'<path d="M{cx - 70 + i * 35} {cy + 40}c-15 -20 15 -40 0 -60s15 -40 0 -60" '
                    f'fill="none" stroke="{C["orange"]}" stroke-width="9" stroke-linecap="round"/>' for i in range(3))
    return four(cx, cy, ondes)


def objet(cx, cy):
    """Objet oublié dans le four (plaque / boîte)."""
    o = (f'<rect x="{cx - 80}" y="{cy + 5}" width="100" height="45" rx="6" fill="{C["caramel"]}" '
         f'stroke="{CH}" stroke-width="8"/>'
         f'<path d="M{cx - 70} {cy + 5}l15 -30h50l15 30" fill="{C["sable"]}" stroke="{CH}" stroke-width="8"/>')
    return four(cx, cy, o)


def etiquette():
    L = [f'<g id="FOND"><rect width="{W}" height="{H}" rx="40" fill="{CR}"/></g>']
    L.append(
        '<g id="BANDEAU">'
        f'<path fill="url(#OrangeRouge)" d="M0 40Q0 0 40 0H{W - 40}Q{W} 0 {W} 40V215C1100 265 600 185 0 240Z"/>'
        # triangle danger
        f'<path d="M160 35L265 200H55Z" fill="#FFD23F" stroke="{CH}" stroke-width="12" stroke-linejoin="round"/>'
        f'<path d="M160 85V145" stroke="{CH}" stroke-width="20" stroke-linecap="round"/>'
        f'<circle cx="160" cy="177" r="11" fill="{CH}"/>'
        + text(830, 145, "ATTENTION – FOUR UNOX SPEED", 92, CR)
        + '</g>')
    L.append('<g id="PICTOS">' + vide(340, 520) + interdit(340, 520, 175)
             + objet(1140, 520) + interdit(1140, 520, 175) + '</g>')
    L.append(
        '<g id="TEXTES">'
        + text(340, 790, "NE PAS LAISSER", 66, CH) + text(340, 865, "TOURNER À VIDE", 66, CH)
        + text(1140, 790, "NE RIEN LAISSER", 66, CH) + text(1140, 865, "À L'INTÉRIEUR", 66, CH)
        + f'<path d="M740 360V880" stroke="{C["caramel"]}" stroke-width="8" stroke-linecap="round"/>'
        + '</g>')
    L.append(
        '<g id="PIED">'
        f'<path fill="{CH}" d="M0 940C500 900 1000 960 {W} 920V{H - 40}Q{W} {H} {W - 40} {H}H40Q0 {H} 0 {H - 40}Z"/>'
        + text(W / 2, 1015, "Éteignez le four après utilisation · Vérifiez qu'il est vide", 40, CR, HEROICA,
               italic=True, bold=True)
        + '</g>')
    L.append('<g id="LOGO">' + logo(1300, 960, 80) + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - Étiquette four Unox A6")


if __name__ == "__main__":
    s = etiquette()
    (HERE / "galzin-etiquette-four-unox-A6.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.2f} Mo")
