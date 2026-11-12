"""PLV Aquilux 54,5 x 25 cm (dessus de meuble) : 3 pains tranchés avec prix + carte des circuits courts (charte Galzin).

Usage : python3 build.py  ->  galzin-plv-pains-circuits-courts.svg (1 unité = 0,1 mm, 5450 x 2500).
Prévoir le fond perdu demandé par l'imprimeur (souvent 3 mm) : le fond déborde déjà de 30 unités.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, image, logo, tirets, ovale_prix  # noqa: E402

W, H = 5450, 2500
CH, CR, CA, CC, CF = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"], C["chocolat_fonce"]
IMG = HERE / "images"
SPLIT = 3350  # frontière pains / circuits courts

# (nom, commune, latitude, longitude, position de l'étiquette : "g" gauche / "d" droite, décalage vertical)
FERMES = [
    ("GAEC de Buscandoles", "Flavin (12)", 44.288, 2.604, "g", -20),
    ("GAEC du Couderquet", "Sévérac-d'Aveyron (12)", 44.322, 3.072, "d", -30),
    ("EARL de la Malborie", "Auriac-Lagast (12)", 44.140, 2.580, "g", 40),
    ("GAEC des Vals", "Millau (12)", 44.098, 3.078, "d", 10),
    ("Brigitte Canivenq", "Cornus (12)", 43.904, 3.177, "d", 0),
    ("Jérôme Fontaine", "Le Bousquet-d'Orb (34)", 43.692, 3.165, "d", 0),
]
PRODUITS = [  # (photo ou None, nom ligne 1, nom ligne 2, prix)
    (None, "Pavé des Causses", "tranché", "2,90€"),
    ("pain-levain", "Demi-boule campagne", "tranchée", "3,00€"),
    ("pain-graines", "Demi-boule campagne", "graines tranchée", "3,10€"),
]


def carte(x0, y0, w, h):
    """Carte vectorielle Aveyron + Hérault (contours IGN/OSM simplifiés) et fermes."""
    import json
    import math

    def polys(f):
        g = json.load(open(IMG / f))
        geo = g.get("geometry") or g["features"][0]["geometry"]
        return geo["coordinates"] if geo["type"] == "Polygon" else [p[0] for p in geo["coordinates"]]

    av, he = polys("dep-12-aveyron.geojson"), polys("dep-34-herault.geojson")
    pts = [pt for ring in av + he for pt in ring]
    k = math.cos(math.radians(44))
    lo0, lo1, la0, la1 = 1.83, 3.62, 43.52, 44.95  # cadrage : Aveyron + nord de l'Hérault
    sc = min(w / ((lo1 - lo0) * k), h / (la1 - la0))
    ox = x0 + (w - (lo1 - lo0) * k * sc) / 2
    oy = y0 + (h - (la1 - la0) * sc) / 2

    def P(lon, lat):
        return ox + (lon - lo0) * k * sc, oy + (la1 - lat) * sc

    def path(rings):
        return "".join("M" + "L".join(f"{P(*pt)[0]:.0f} {P(*pt)[1]:.0f}" for pt in r[::2]) + "Z" for r in rings)

    o = (f'<clipPath id="clip-carte"><rect x="{x0}" y="{y0}" width="{w}" height="{h}"/></clipPath>'
         f'<g id="CARTE" clip-path="url(#clip-carte)"><path id="herault" d="{path(he)}" fill="{C["sable"]}" stroke="{CA}" stroke-width="8" '
         f'stroke-linejoin="round"/>'
         f'<path id="aveyron" d="{path(av)}" fill="#FFFFFF" stroke="{CH}" stroke-width="10" stroke-linejoin="round"/>')
    ax, ay = P(2.62, 44.78)
    hx, hy = P(2.78, 43.58)
    o += text(ax, ay, "AVEYRON (12)", 62, CA, spacing=6) + text(hx, hy, "HÉRAULT (34)", 62, CA, spacing=6)
    for nom, lieu, lat, lon, cote, dy in FERMES:
        x, y = P(lon, lat)
        anc, dx = ("end", -60) if cote == "g" else ("start", 60)
        o += (f'<g id="ferme-{lieu.split()[0].lower()}">'
              f'<circle cx="{x:.0f}" cy="{y:.0f}" r="34" fill="{C["orange"]}" stroke="{CH}" stroke-width="8"/>'
              + text(x + dx, y + dy, nom, 54, CH, HEROICA, anc, bold=True)
              + text(x + dx, y + dy + 60, lieu, 44, CA, HEROICA, anc, italic=True, bold=True) + '</g>')
    halo = '<text stroke="#FFFFFF" stroke-width="16" stroke-linejoin="round" paint-order="stroke" '
    return o.replace("<text ", halo) + '</g>'


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
        + text(4425, 260, "FAVORISER LES", 140, CH)
        + f'<rect x="3560" y="310" width="1730" height="290" rx="20" fill="{CH}"/>'
        + text(4425, 540, "CIRCUITS COURTS", 230, CR)
        + pastille(4425, 790, 1550, 150, "Origine du blé bio de nos farines", 88, CC, CF, rot=-2,
                   font=HEROICA, bold=True, italic=True)
        + carte(3520, 880, 1900, 1600)
        + '</g>')

    # --- Partie gauche : les trois pains tranchés ---
    cartes = ""
    for i, (img, l1, l2, prix) in enumerate(PRODUITS):
        x = 100 + i * 1080
        cx = x + 500
        if img:
            cartes += photo(img, x, 560, 1000, 820, rot=(-2, 0, 2)[i], cid=f"p{i}")
        else:
            cartes += (f'<g id="photo-pave"><rect x="{x}" y="560" width="1000" height="820" rx="40" fill="{CF}" '
                       f'stroke="{CR}" stroke-width="10" stroke-dasharray="40 26"/>'
                       + text(cx, 960, "PHOTO", 90, CC) + text(cx, 1060, "PAVÉ DES CAUSSES", 90, CC) + '</g>')
        cartes += (text(cx, 1510, l1, 92, CR, HEROICA, bold=True)
                   + text(cx, 1610, l2, 76, CC, HEROICA, italic=True, bold=True)
                   + ovale_prix(cx, 1880, 300, 170, prix, "cuivre", size=190, rot=(-5, 3, -4)[i]))
    L.append(
        '<g id="PAINS">'
        + logo(90, 60, 380)
        + text(1900, 270, "NOS PAINS TRANCHÉS", 230, CR)
        + text(1900, 450, "à la farine de blé bio de nos régions", 110, CC, HEROICA, italic=True, bold=True)
        + tirets(800, 415, "g", CC) + tirets(3000, 415, "d", CC)
        + cartes
        + pastille(1800, 2310, 2600, 200, "BLÉ BIO · CIRCUITS COURTS", 120, C["orange"], CR, rot=-1)
        + '</g>')
    return svg(W, H, "\n".join(L), "Galzin - PLV pains & circuits courts")


if __name__ == "__main__":
    s = plv()
    (HERE / "galzin-plv-pains-circuits-courts.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.1f} Mo")
