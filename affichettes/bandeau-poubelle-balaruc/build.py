"""Bandeau autocollant « Poubelle – Merci » pour Balaruc (charte Galzin), 600 x 60 mm.

Usage : python3 build.py  ->  galzin-bandeau-poubelle-balaruc.svg (1 unité = 0,1 mm, 6000 x 600).
Fond perdu de 2 mm ; calque DECOUPE = contour de coupe (ne pas imprimer).
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

W, H = 6000, 600
CH, CR, CA, CC = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"]


def poubelle(cx, cy, s=1.0, col=CR):
    """Pictogramme poubelle vectoriel."""
    return (f'<g transform="translate({cx} {cy}) scale({s})" fill="{col}">'
            f'<rect x="-120" y="-150" width="240" height="40" rx="12"/>'
            f'<rect x="-45" y="-185" width="90" height="45" rx="12"/>'
            f'<path d="M-100 -95H100L82 170Q80 190 60 190H-60Q-80 190 -82 170Z"/>'
            f'<g stroke="{CH}" stroke-width="18" stroke-linecap="round">'
            f'<path d="M-45 -50V140"/><path d="M0 -50V140"/><path d="M45 -50V140"/></g></g>')


def bandeau():
    L = [f'<g id="FOND"><rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="{CH}"/>'
         f'<path d="M-20 520C1500 470 4500 570 {W + 20} 505" fill="none" stroke="{CA}" stroke-width="10"/>'
         f'<path d="M-20 80C1500 30 4500 130 {W + 20} 65" fill="none" stroke="{CA}" stroke-width="10"/></g>']
    L.append(
        '<g id="TEXTES">'
        + logo(90, 75, 450)
        + poubelle(1020, 300, 0.95)
        + text(1300, 405, "POUBELLE", 300, CR, anchor="start", spacing=20)
        + f'<circle cx="3160" cy="300" r="22" fill="{CC}"/>'
        + text(3330, 400, "Merci !", 280, CC, HEROICA, "start", italic=True, bold=True)
        + text(4330, 390, "de garder notre boutique propre", 100, CR, HEROICA, "start", italic=True, bold=True)
        + '</g>')
    L.append(f'<g id="DECOUPE"><rect width="{W}" height="{H}" rx="40" fill="none" stroke="#E30F20" '
             f'stroke-width="3"/></g>')
    return svg(W, H, "\n".join(L), "Galzin - Bandeau poubelle Balaruc")


if __name__ == "__main__":
    (HERE / "galzin-bandeau-poubelle-balaruc.svg").write_text(bandeau(), encoding="utf-8")
