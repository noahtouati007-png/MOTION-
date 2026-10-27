"""Boissons Galzin x Cafés Folliet, refaites dans la charte Galzin (voir ../_kit-galzin/CHARTE.md).

Usage : python3 build.py
Produit des SVG à ouvrir dans Illustrator : textes, formes, dégradés modifiables, photos intégrées.
Unités : 1 unité = 0,1 mm. Les ovales de prix sont livrés vides.
"""
import base64
import io
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "_kit-galzin"))
from build import C, IMPACT, HEROICA, ovale_prix, plus, svg  # noqa: E402

IMG = HERE / "images"
PRIX = ""  # prix laissés vides : l'ovale est prêt, on tape le prix dans Illustrator
_cache = {}


def href(name, max_px=900):
    if name not in _cache:
        im = Image.open(IMG / f"{name}.png")
        im.thumbnail((max_px, max_px))
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        _cache[name] = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    return _cache[name]


def image(name, x, y, w, h, max_px=900):
    return (f'<image id="{name}" x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'preserveAspectRatio="xMidYMid meet" xlink:href="{href(name, max_px)}"/>')


def text(x, y, txt, size, fill, font=IMPACT, anchor="middle", italic=False, bold=False, rot=0):
    st = ' font-style="italic"' if italic else ""
    wt = ' font-weight="bold"' if bold else ""
    tr = f' transform="rotate({rot} {x:.0f} {y:.0f})"' if rot else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size:.0f}" fill="{fill}"{st}{wt}{tr}>{txt}</text>')


def lines(x, y, rows, size, fill, lead=1.05, **kw):
    return "".join(text(x, y + i * size * lead, r, size, fill, **kw) for i, r in enumerate(rows))


def pill(cx, cy, w, h, fill, rot=-3, inner=""):
    return (f'<g transform="rotate({rot} {cx:.0f} {cy:.0f})">'
            f'<rect x="{cx - w/2:.0f}" y="{cy - h/2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{h*0.22:.0f}" '
            f'fill="{fill}"/>{inner}</g>')


def folliet(cx, y, w):
    h = w * 468 / 1812
    return image("folliet-logo-blanc", cx - w/2, y, w, h, 1812)


# --- Affiches « Nos boissons » (50x70 et carte A5) ----------------------------------------------
CHAUDES = [
    ("espresso", ["ESPRESSO"], []),
    ("decafeine", ["DÉCAFÉINÉ"], []),
    ("double-espresso", ["DOUBLE", "ESPRESSO"], []),
    ("cafe-allonge", ["CAFÉ ALLONGÉ"], []),
    ("americano", ["AMÉRICANO"], []),
    ("cafe-noisette", ["CAFÉ", "NOISETTE"], []),
    ("cafe-creme", ["CAFÉ CRÈME"], []),
    ("cappuccino", ["CAPPUCCINO"], []),
    ("cappuccino-noisette", ["CAPPUCCINO", "NOISETTE"], []),
    ("latte-macchiato", ["LATTE", "MACCHIATO"], ["supplément sirop"]),
    ("the", ["THÉ"], ["Ceylan · Fruits rouges", "Thé vert · Thé vert menthe", "Citron · Earl grey",
                      "Verveine · Verveine menthe"]),
    ("chocolat-chaud", ["CHOCOLAT", "CHAUD"], []),
]
FROIDES = [
    ("pink-paradise", ["PINK PARADISE"], ["Fruit du dragon, goyave", "& ananas"]),
    ("coco-caline", ["COCO CÂLINE"], ["Ananas & coco"]),
    ("tagada-banana", ["TAGADA BANANA"], ["Fraise & banane"]),
    ("fruits-on-the-beach", ["FRUITS ON", "THE BEACH"], ["Mangue, passion & orange"]),
    ("red-boost", ["RED BOOST"], ["Grenade, framboise", "& acérola"]),
    ("tokyo", ["TOKYO"], ["Matcha"]),
    ("seattle", ["SEATTLE"], ["Café"]),
    ("manhattan", ["MANHATTAN"], ["Chocolat"]),
    ("hawai", ["HAWAÏ"], ["Vanille"]),
]


def menu_boissons(W, H, sous_titre, items, cols, bas=None, titre_doc=""):
    """Composition dessinée sur une largeur de 5000 puis mise à l'échelle du format réel."""
    s = W / 5000
    Hd = H / s
    rows = (len(items) + cols - 1) // cols
    L = []
    L.append(f'<g id="FOND"><rect width="5000" height="{Hd:.0f}" fill="{C["creme"]}"/></g>')
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{C["chocolat"]}" d="M0 0H5000V1250C4100 1560 2900 1130 1800 1360C1100 1500 500 1520 0 1440Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="22" '
        f'd="M0 1500C500 1580 1100 1560 1800 1420C2900 1190 4100 1620 5000 1310"/>'
        f'<path fill="{C["chocolat"]}" d="M0 {Hd-620:.0f}C1400 {Hd-1000:.0f} 3100 {Hd-430:.0f} 5000 {Hd-860:.0f}'
        f'V{Hd:.0f}H0Z"/>'
        '</g>')

    # En-tête
    head = (f'<image id="galzin-logo" x="230" y="150" width="1180" height="1180" '
            f'xlink:href="{href("galzin-logo", 1200)}"/>'
            + text(3250, 860, "NOS BOISSONS", 560, C["creme"])
            + pill(3950, 1250, 1500, 400, C["turquoise"], rot=-3,
                   inner=text(3950, 1355, sous_titre, 300, C["creme"], HEROICA, italic=True, bold=True)))

    # Grille produits
    top, bottom = 1780, Hd - (1500 if bas else 1080)
    cw = 4600 / cols
    rh = (bottom - top) / rows
    maxn = max(len(n) for _, n, _ in items)
    maxd = min(2, max(len(d) for _, _, d in items))
    ph = min(cw * 0.72, rh / (1.1 + 0.19 * maxn + 0.13 * maxd))
    cells, prices = [], []
    for i, (img, nom, desc) in enumerate(items):
        cx = 200 + cw * (i % cols) + cw / 2
        y = top + rh * (i // cols)
        cy = y + ph / 2 + 20
        cells.append(f'<g id="produit-{img}">'
                     f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{ph*0.5:.0f}" fill="{C["sable"]}"/>'
                     + image(img, cx - ph * 0.5, cy - ph * 0.5, ph, ph * 0.98)
                     + lines(cx, y + ph * 1.25, nom, ph * 0.19, C["chocolat"], lead=1.0)
                     + lines(cx, y + ph * (1.22 + 0.19 * len(nom)), desc, ph * 0.105,
                             C["chocolat"], font=HEROICA, italic=True, lead=1.15)
                     + '</g>')
        prices.append(ovale_prix(cx + ph * 0.48, cy - ph * 0.3, ph * 0.3, ph * 0.16, PRIX, "cuivre", rot=-5))

    extra = ""
    if bas:
        by = Hd - 1230
        extra = pill(2500, by, 4300, 330, C["turquoise"], rot=-2,
                     inner=text(2500, by + 75, bas, 200, C["creme"]))
    L.append('<g id="PHOTOS_TEXTES">' + head + "".join(cells) + extra + '</g>')
    L.append('<g id="PRIX">' + "".join(prices) + '</g>')
    L.append('<g id="LOGO_MENTIONS">' + folliet(2500, Hd - 430, 1500)
             + text(4900, Hd - 90, "Photos non contractuelles", 85, C["creme"], HEROICA, "end", italic=True)
             + '</g>')
    body = f'<g transform="scale({s:.6f})">\n' + "\n".join(L) + '\n</g>'
    return svg(W, H, body, titre_doc)


# --- Stop-trottoir (540 x 1250 mm, fenêtre en arche comme l'original) ----------------------------
SW, SH = 5400, 12500
AX0, AX1, ATOP, ABOT = 620, 4780, 340, 11330  # fenêtre en arche
AR = (AX1 - AX0) / 2


def arche():
    return (f'M{AX0} {ATOP + AR}A{AR} {AR} 0 0 1 {AX1} {ATOP + AR}V{ABOT}H{AX0}Z')


def stop_base(contenu, titre_doc):
    L = [f'<g id="FOND"><rect width="{SW}" height="{SH}" fill="{C["chocolat"]}"/>'
         f'<path d="{arche()}" fill="{C["creme"]}"/></g>']
    L.append(contenu)
    L.append('<g id="LOGO_MENTIONS">'
             f'<image id="galzin-logo" x="{SW/2 - 1050:.0f}" y="560" width="2100" height="2100" '
             f'xlink:href="{href("galzin-logo", 1743)}"/>'
             + folliet(SW / 2, ABOT + 280, 2300)
             + text(AX1 - 80, ABOT - 90, "Photos non contractuelles", 95, C["creme"], HEROICA, "end", italic=True)
             + '</g>')
    return svg(SW, SH, "\n".join(L), titre_doc)


def clip_arche():
    return f'<clipPath id="Arche"><path d="{arche()}"/></clipPath>'


def stop_recto():
    v = (f'<g id="VAGUES" clip-path="url(#Arche)">{clip_arche()}'
         f'<path fill="{C["chocolat"]}" d="M0 5450C1400 5050 2800 5750 {SW} 5250V8350C3800 8800 2200 8100 0 8600Z"/>'
         f'<path fill="none" stroke="{C["caramel"]}" stroke-width="30" '
         f'd="M0 5380C1400 4980 2800 5680 {SW} 5180"/>'
         f'<path fill="none" stroke="{C["caramel"]}" stroke-width="30" '
         f'd="M0 8680C2200 8180 3800 8880 {SW} 8430"/></g>')
    t = '<g id="TEXTES_PHOTOS">'
    # 1. Café + croissant
    t += text(SW / 2, 3250, "CAFÉ + CROISSANT", 430, C["chocolat"])
    t += image("cafe-croissant", 900, 3450, 3000, 1750, 1200)
    # 2. 3 viennoiseries
    t += text(SW / 2, 6050, "3 VIENNOISERIES", 500, C["creme"])
    t += pill(SW / 2 + 900, 6380, 1250, 330, C["turquoise"], rot=-4,
              inner=text(SW / 2 + 900, 6475, "au choix", 250, C["creme"], HEROICA, italic=True, bold=True))
    t += image("viennoiseries", 1000, 6600, 3400, 1800, 1200)
    # 3. Sandwich / salade + boisson
    for cx, nom, img in ((1650, "SANDWICH", "sandwich-boisson"), (3750, "SALADE", "salade-boisson")):
        t += pill(cx, 9150, 1850, 360, C["turquoise"], rot=-3,
                  inner=text(cx, 9265, nom, 320, C["creme"]))
        t += text(cx, 9720, "+ BOISSON", 300, C["chocolat"])
        t += image(img, cx - 900, 9850, 1800, 1150, 900)
    t += '</g>'
    p = ('<g id="PRIX">'
         + ovale_prix(3950, 3800, 600, 320, PRIX, "cuivre", rot=-5)
         + ovale_prix(1250, 7000, 600, 320, PRIX, "turquoise", rot=4)
         + ovale_prix(2150, 10950, 430, 230, PRIX, "cuivre", rot=-4)
         + ovale_prix(4250, 10950, 430, 230, PRIX, "cuivre", rot=-4)
         + '</g>')
    return stop_base(v + t + p, "Galzin - Stop-trottoir recto")


def stop_verso():
    v = (f'<g id="VAGUES" clip-path="url(#Arche)">{clip_arche()}'
         f'<path fill="{C["chocolat"]}" d="M0 7000C1500 6550 3200 7350 {SW} 6750V{SH}H0Z"/>'
         f'<path fill="none" stroke="{C["caramel"]}" stroke-width="30" '
         f'd="M0 6920C1500 6470 3200 7270 {SW} 6670"/></g>')
    t = ('<g id="TEXTES_PHOTOS">'
         + text(SW / 2, 3500, "FORMULE", 560, C["chocolat"])
         + text(SW / 2, 4050, "Espresso", 520, C["chocolat"], HEROICA, bold=True)
         + image("formule-espresso", 900, 4300, 3600, 2300, 1200)
         + text(SW / 2, 7900, "FORMULE", 560, C["creme"])
         + text(SW / 2, 8450, "Petit-déjeuner", 470, C["creme"], HEROICA, bold=True)
         + image("formule-petit-dej", 900, 8650, 3600, 2450, 1200)
         + '</g>')
    p = ('<g id="PRIX">'
         + ovale_prix(4000, 4500, 600, 320, PRIX, "cuivre", rot=-5)
         + ovale_prix(1300, 8900, 600, 320, PRIX, "turquoise", rot=4)
         + '</g>')
    return stop_base(v + t + p, "Galzin - Stop-trottoir verso")


if __name__ == "__main__":
    out = {
        "galzin-boissons-chaudes-50x70.svg": menu_boissons(5000, 7000, "Chaudes", CHAUDES, 4,
                                                           titre_doc="Galzin - Boissons chaudes 50x70"),
        "galzin-boissons-froides-50x70.svg": menu_boissons(5000, 7000, "Froides", FROIDES, 3,
                                                           bas="CHOISISSEZ LA VERSION SMOOTHIE OU MILKSHAKE",
                                                           titre_doc="Galzin - Boissons froides 50x70"),
        "galzin-carte-boissons-chaudes-A5.svg": menu_boissons(1480, 2100, "Chaudes", CHAUDES, 4,
                                                              titre_doc="Galzin - Carte boissons chaudes A5"),
        "galzin-stop-trottoir-recto.svg": stop_recto(),
        "galzin-stop-trottoir-verso.svg": stop_verso(),
    }
    for name, content in out.items():
        (HERE / name).write_text(content, encoding="utf-8")
        print(name, f"{len(content) / 1e6:.1f} Mo")
