"""PLV 15 x 10 cm : pas de billets de 50€ / pas de commandes de milkshakes.

Même format et même DA claire que le sticker allergènes (cadre chocolat + caramel, bandeau bas).
Usage : python3 build.py  ->  galzin-plv-billets-milkshakes.svg (1 unité = 0,1 mm).
Pictogrammes vectoriels. Fond perdu 2 mm ; calque DECOUPE = rectangle de coupe.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

W, H = 1500, 1000
CH, CR, CA, CC, R = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"], C["rouge"]


def interdit(cx, cy, r=165):
    d = r * 0.707
    return (f'<g fill="none" stroke="{R}" stroke-width="26" stroke-linecap="round">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/><path d="M{cx - d:.0f} {cy - d:.0f}L{cx + d:.0f} {cy + d:.0f}"/></g>')


def billet(cx, cy):
    return (f'<g id="picto-billet" transform="rotate(-8 {cx} {cy})">'
            f'<rect x="{cx - 150}" y="{cy - 82}" width="300" height="164" rx="18" fill="{C["sable"]}" '
            f'stroke="{CH}" stroke-width="10"/>'
            f'<circle cx="{cx - 88}" cy="{cy}" r="42" fill="none" stroke="{CA}" stroke-width="8"/>'
            + text(cx + 40, cy + 34, "50€", 96, CH, HEROICA, bold=True) + '</g>' + interdit(cx, cy))


def milkshake(cx, cy):
    return (f'<g id="picto-milkshake">'
            f'<path d="M{cx + 10} {cy - 95}L{cx + 55} {cy - 175}" stroke="{C["orange"]}" stroke-width="14" '
            f'stroke-linecap="round"/>'
            f'<path d="M{cx - 70} {cy - 70}C{cx - 80} {cy - 130} {cx - 20} {cy - 135} {cx} {cy - 115}'
            f'C{cx + 25} {cy - 140} {cx + 85} {cy - 125} {cx + 70} {cy - 70}Z" fill="#FFFFFF" stroke="{CH}" stroke-width="8"/>'
            f'<path d="M{cx - 80} {cy - 70}H{cx + 80}L{cx + 58} {cy + 120}H{cx - 58}Z" fill="{CA}" '
            f'stroke="{CH}" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="M{cx - 72} {cy - 20}H{cx + 72}" stroke="{CH}" stroke-width="8"/></g>' + interdit(cx, cy))


def plv():
    L = [f'<g id="FOND"><rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="{C["sable"]}"/>'
         f'<rect x="40" y="40" width="{W - 80}" height="{H - 80}" rx="30" fill="{CR}" stroke="{CH}" stroke-width="6"/>'
         f'<rect x="58" y="58" width="{W - 116}" height="{H - 116}" rx="22" fill="none" stroke="{CA}" stroke-width="3"/>'
         f'<path fill="{CH}" d="M40 800H{W - 40}V{H - 70}Q{W - 40} {H - 40} {W - 70} {H - 40}H70Q40 {H - 40} 40 {H - 70}Z"/></g>']
    L.append(
        '<g id="TEXTES">'
        + logo(110, 95, 130)
        + text(W / 2 + 60, 190, "À NOTRE AIMABLE CLIENTÈLE", 82, CH)
        + f'<path d="M{W/2 - 260} 225H{W/2 + 380}" stroke="{CC}" stroke-width="8" stroke-linecap="round"/>'
        + billet(400, 440) + milkshake(1100, 455)
        + text(400, 690, "PAS DE BILLETS DE 50€", 64, CH)
        + text(1100, 675, "PAS DE COMMANDE", 64, CH)
        + text(1100, 745, "DE MILKSHAKES", 64, CA)
        + f'<path d="M750 320V720" stroke="{CA}" stroke-width="6" stroke-linecap="round"/>'
        + text(W / 2, 905, "Merci de votre compréhension", 52, CC, HEROICA, italic=True, bold=True)
        + '</g>')
    L.append(f'<g id="DECOUPE"><rect width="{W}" height="{H}" fill="none" stroke="#E30F20" stroke-width="3"/></g>')
    return svg(W, H, "\n".join(L), "Galzin - PLV billets et milkshakes")


if __name__ == "__main__":
    (HERE / "galzin-plv-billets-milkshakes.svg").write_text(plv(), encoding="utf-8")
