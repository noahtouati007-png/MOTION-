"""PLV Aquilux 54,5 x 25 cm (dessus de meuble) : pains de campagne + circuits courts (charte Galzin).

Usage : python3 build.py  ->  galzin-plv-pains-circuits-courts.svg (1 unité = 0,1 mm, 5450 x 2500).
Prévoir le fond perdu demandé par l'imprimeur (souvent 3 mm) : le fond déborde déjà de 30 unités.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, image, logo, tirets  # noqa: E402

W, H = 5450, 2500
CH, CR, CA, CC, CF = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"], C["chocolat_fonce"]
IMG = HERE / "images"
SPLIT = 3350  # frontière pains / circuits courts

FERMES = [
    ("GAEC de Buscandoles", "Flavin (12)"),
    ("GAEC du Couderquet", "Sévérac-d'Aveyron (12)"),
    ("EARL de la Malborie", "Auriac-Lagast (12)"),
    ("GAEC des Vals", "Millau (12)"),
    ("Brigitte Canivenq", "Cornus (12)"),
    ("Jérôme Fontaine", "Le Bousquet-d'Orb (34)"),
]


def photo(nom, x, y, w, h, rot=0, cid=None):
    """Photo recadrée dans un cadre arrondi avec liseré crème."""
    cid = cid or nom
    return (f'<g id="photo-{nom}" transform="rotate({rot} {x + w/2} {y + h/2})">'
            f'<clipPath id="clip-{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="40"/></clipPath>'
            f'<g clip-path="url(#clip-{cid})">'
            + image(IMG / f"{nom}.jpg", x, y, w, h, 1400, id=nom).replace("meet", "slice")
            + '</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="40" fill="none" stroke="{CR}" stroke-width="22"/></g>')


def pastille(cx, cy, w, h, txt, size, fill=CA, color=CF, rot=-4, font=IMPACT, **kw):
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect x="{cx - w/2}" y="{cy - h/2}" width="{w}" height="{h}" '
            f'rx="{h * 0.35:.0f}" fill="{fill}"/>'
            + text(cx, cy + size * 0.35, txt, size, color, font, **kw) + '</g>')


def plv():
    L = [f'<g id="FOND"><rect x="-30" y="-30" width="{W + 60}" height="{H + 60}" fill="{CH}"/></g>']

    # --- Partie droite : circuits courts (fond champ de blé + voile crème) ---
    vague = f'M{SPLIT} -30C{SPLIT - 160} 600 {SPLIT + 140} 1300 {SPLIT - 60} 2000S{SPLIT + 60} {H} {SPLIT} {H + 30}'
    L.append(
        '<g id="CIRCUITS_COURTS">'
        f'<clipPath id="clip-droite"><path d="{vague}H{W + 30}V-30Z"/></clipPath>'
        f'<path d="{vague}H{W + 30}V-30Z" fill="{CR}"/>'
        f'<path d="{vague}" fill="none" stroke="{CC}" stroke-width="22"/>'
        + text(4420, 330, "FAVORISER LES", 150, CH)
        + f'<rect x="3560" y="380" width="1730" height="290" rx="20" fill="{CH}"/>'
        + text(4425, 610, "CIRCUITS COURTS", 230, CR)
        + pastille(4425, 800, 1500, 150, "Origine du blé bio de nos farines", 88, CC, CF, rot=-2,
                   font=HEROICA, bold=True, italic=True)
        + "".join(
            f'<g id="ferme-{i}"><circle cx="3620" cy="{1035 + i * 205}" r="38" fill="{C["orange"]}" '
            f'stroke="{CH}" stroke-width="8"/>'
            + text(3710, 1030 + i * 205, nom, 80, CH, HEROICA, "start", bold=True)
            + text(3710, 1110 + i * 205, lieu, 62, CA, HEROICA, "start", italic=True, bold=True) + '</g>'
            for i, (nom, lieu) in enumerate(FERMES))
        + photo("agriculteur", 4720, 980, 600, 760, rot=3)
        + text(5020, 1900, "Nos agriculteurs", 64, CH, HEROICA, italic=True, bold=True, rot=3)
        + text(5020, 1975, "d'Aveyron & d'Hérault", 64, CH, HEROICA, italic=True, bold=True, rot=3)
        + pastille(4425, 2330, 1500, 190, "BLÉ BIO · CIRCUITS COURTS", 115, C["orange"], CR, rot=-2)
        + '</g>')

    # --- Partie gauche : les deux pains ---
    L.append(
        '<g id="PAINS">'
        + logo(90, 70, 380)
        + text(1760, 300, "NOS PAINS DE CAMPAGNE", 230, CR)
        + text(1760, 520, "à la farine de blé bio de nos régions", 120, CC, HEROICA, italic=True, bold=True)
        + tirets(580, 480, "g", CC) + tirets(2940, 480, "d", CC)
        + photo("pain-levain", 180, 700, 1450, 1150, rot=-2)
        + photo("pain-graines", 1780, 700, 1350, 1270, rot=2)
        + pastille(905, 2080, 1200, 260, "Levain", 175, CC, CF, rot=-3, font=HEROICA, bold=True)
        + pastille(2455, 2140, 1200, 260, "aux Graines", 175, CC, CF, rot=3, font=HEROICA, bold=True)
        + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - PLV pains & circuits courts")


if __name__ == "__main__":
    s = plv()
    (HERE / "galzin-plv-pains-circuits-courts.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
