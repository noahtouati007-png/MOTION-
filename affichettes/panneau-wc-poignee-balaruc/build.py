"""Panneau rond festonné « Monter la poignée pour fermer la porte des WC » — Balaruc.

Même thème que le bandeau poubelle de Balaruc (fond chocolat, liserés caramel). Diamètre 150 mm.
Usage : python3 build.py  ->  galzin-panneau-wc-poignee-balaruc.svg (1 unité = 0,1 mm).
Calque DECOUPE = contour festonné (ne pas imprimer).
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

D = 1500
CX = CY = D / 2
CH, CR, CA, CC = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"]


def feston(r, n=28, a=22):
    """Contour festonné (comme un rond de pâtisserie)."""
    pts = []
    for i in range(n * 12):
        t = 2 * math.pi * i / (n * 12)
        rr = r + a * abs(math.cos(n * t / 2))
        pts.append(f"{CX + rr * math.cos(t):.1f} {CY + rr * math.sin(t):.1f}")
    return "M" + "L".join(pts) + "Z"


def fleche_poignee(cx, cy):
    """Poignée de porte + flèche vers le haut."""
    return (f'<g id="picto-poignee">'
            f'<rect x="{cx - 26}" y="{cy - 60}" width="52" height="120" rx="20" fill="{CC}"/>'
            f'<rect x="{cx - 10}" y="{cy - 20}" width="190" height="44" rx="20" fill="{CC}" '
            f'transform="rotate(-25 {cx} {cy})"/>'
            f'<path d="M{cx + 230} {cy + 20}V{cy - 120}M{cx + 180} {cy - 70}L{cx + 230} {cy - 125}L{cx + 280} {cy - 70}" '
            f'fill="none" stroke="{CR}" stroke-width="26" stroke-linecap="round" stroke-linejoin="round"/></g>')


def panneau():
    L = [f'<g id="FOND"><path d="{feston(712)}" fill="{CH}"/>'
         f'<circle cx="{CX}" cy="{CY}" r="615" fill="none" stroke="{CA}" stroke-width="10"/></g>']
    L.append(
        '<g id="TEXTES">'
        + logo(CX - 120, 150, 240)
        + text(CX, 560, "Veuillez", 90, CC, HEROICA, italic=True, bold=True)
        + text(CX, 700, "MONTER LA POIGNÉE", 120, CR)
        + text(CX, 830, "pour fermer la porte", 86, CR, HEROICA, bold=True)
        + text(CX, 930, "des WC", 86, CR, HEROICA, bold=True)
        + fleche_poignee(CX - 120, 1130)
        + text(CX, 1320, "Merci !", 100, CC, HEROICA, italic=True, bold=True)
        + '</g>')
    L.append(f'<g id="DECOUPE"><path d="{feston(695)}" fill="none" stroke="#E30F20" stroke-width="3"/></g>')
    return svg(D, D, "\n".join(L), "Galzin - Panneau WC poignée Balaruc")


if __name__ == "__main__":
    (HERE / "galzin-panneau-wc-poignee-balaruc.svg").write_text(panneau(), encoding="utf-8")
