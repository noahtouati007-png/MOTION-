"""Kit Galzin : couleurs, polices et éléments de la DA, pour produire des SVG modifiables dans Illustrator.

Import depuis un script de visuel :
    import sys; sys.path.insert(0, "<chemin>/galzin-da/scripts")
    from galzin_kit import C, IMPACT, HEROICA, svg, text, image, ovale_prix, plus, pastille, tirets, badge_fidelite

Lancé seul (python3 galzin_kit.py) : écrit gabarit A4, bibliothèque d'éléments et nuancier .ase dans le dossier courant.
Tous les SVG produits s'ouvrent dans Illustrator (Fichier > Ouvrir) avec textes, formes et
dégradés modifiables. Unités : 1 unité = 0,1 mm (A4 = 2100 x 2970).
"""
import base64
import re
import io
import struct
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
ASSETS = HERE.parent / "assets"

# --- Charte couleurs (relevées sur les affiches existantes) -------------------------------
C = {
    "chocolat": "#5C2E15",      # brun principal (vagues, titres)
    "chocolat_fonce": "#3B1F0E",  # contours des ovales, textes sur cuivre
    "creme": "#FDF0E2",         # fond clair
    "sable": "#EEDDC5",         # fond clair alternatif (affiche salade/wrap)
    "caramel": "#C58243",       # brun clair (bas d'affiche pizza)
    "turquoise": "#51A3A3",     # pastilles produits, ovales de prix
    "turquoise_clair": "#6CBDB5",
    "orange": "#E8721D",        # dégradé OFFRE+
    "rouge": "#E30F20",
    "cuivre_clair": "#F1C680",
    "cuivre": "#D89D58",
    "cuivre_fonce": "#8A4A1C",
    "blanc": "#FFFFFF",
}

IMPACT = "Impact"
HEROICA = "Eroika Slab"  # graisses disponibles : Normal, Bold, Bold Italic

DEFS = f"""
  <defs>
    <linearGradient id="Cuivre" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{C['cuivre_fonce']}"/>
      <stop offset="0.38" stop-color="{C['cuivre']}"/>
      <stop offset="0.55" stop-color="{C['cuivre_clair']}"/>
      <stop offset="0.78" stop-color="#C27A3D"/>
      <stop offset="1" stop-color="{C['cuivre_fonce']}"/>
    </linearGradient>
    <linearGradient id="Turquoise" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#3E8F90"/>
      <stop offset="0.5" stop-color="{C['turquoise_clair']}"/>
      <stop offset="1" stop-color="{C['turquoise']}"/>
    </linearGradient>
    <linearGradient id="OrangeRouge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{C['orange']}"/>
      <stop offset="1" stop-color="{C['rouge']}"/>
    </linearGradient>
  </defs>"""


def logo_href():
    data = base64.b64encode((ASSETS / "galzin-logo.png").read_bytes()).decode()
    return f"data:image/png;base64,{data}"


# --- Éléments réutilisables --------------------------------------------------------------
def text(x, y, txt, size, fill, font=IMPACT, anchor="middle", italic=False, bold=False, rot=0, spacing=0):
    """Texte SVG (échappé : les « & » ne cassent plus le fichier)."""
    a = (' font-style="italic"' if italic else "") + (' font-weight="bold"' if bold else "")
    a += f' letter-spacing="{spacing}"' if spacing else ""
    a += f' transform="rotate({rot} {x:.0f} {y:.0f})"' if rot else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size:.0f}" fill="{fill}"{a}>{escape(str(txt), quote=False)}</text>')


def image(path, x, y, w, h, max_px=1000, rot=0, id=None):
    """Photo PNG détourée intégrée (base64), redimensionnée à max_px pour garder un fichier léger."""
    from PIL import Image
    im = Image.open(path)
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    d = base64.b64encode(buf.getvalue()).decode()
    tr = f' transform="rotate({rot} {x + w/2:.0f} {y + h/2:.0f})"' if rot else ""
    i = f' id="{id or Path(path).stem}"'
    return (f'<image{i} x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'preserveAspectRatio="xMidYMid meet"{tr} xlink:href="data:image/png;base64,{d}"/>')


def logo(x, y, s, hd=True):
    """Logo rond Galzin (PNG) ; demander la version vectorielle pour le grand format."""
    return image(ASSETS / ("galzin-logo-hd.png" if hd else "galzin-logo.png"), x, y, s, s, 1200, id="galzin-logo")


def tirets(cx, cy, cote, color, k=1.0):
    """Trois traits décoratifs de part et d'autre d'une accroche Heroica (cote = "g" ou "d")."""
    sg = -1 if cote == "g" else 1
    return (f'<g fill="none" stroke="{color}" stroke-width="{16*k:.0f}" stroke-linecap="round">'
            f'<path d="M{cx} {cy - 40*k:.0f}l{sg*90*k:.0f} {-40*k:.0f}"/><path d="M{cx} {cy}l{sg*120*k:.0f} 0"/>'
            f'<path d="M{cx} {cy + 40*k:.0f}l{sg*90*k:.0f} {40*k:.0f}"/></g>')


def plus(x, y, s=120, color=C["chocolat"]):
    """Croix « + » épaisse (comme sur l'affiche petit-déj)."""
    t = s * 0.3
    return (f'<path fill="{color}" d="M{x - t/2} {y - s/2}h{t}v{(s - t)/2}h{(s - t)/2}v{t}'
            f'h{-(s - t)/2}v{(s - t)/2}h{-t}v{-(s - t)/2}h{-(s - t)/2}v{-t}h{(s - t)/2}z"/>')


def pastille(x, y, w, h, texte, size=150, rot=-2, sous=None):
    """Bandeau turquoise arrondi + texte Impact crème."""
    sub = ""
    if sous:
        sub = (f'<text x="{x + 70}" y="{y + h - 45}" font-family="{IMPACT}" font-size="{size * 0.55}" '
               f'fill="{C["creme"]}">{sous}</text>')
    return (f'<g transform="rotate({rot} {x + w/2} {y + h/2})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="45" fill="{C["turquoise"]}"/>'
            f'<text x="{x + 70}" y="{y + size * 0.95 + 25}" font-family="{IMPACT}" font-size="{size}" '
            f'fill="{C["creme"]}">{texte}</text>{sub}</g>')


def ovale_prix(cx, cy, rx, ry, prix, style="cuivre", size=None, rot=0):
    """Ovale de prix : cuivre (contour chocolat), turquoise ou orange-rouge."""
    size = size or ry * 1.15
    fill = {"cuivre": "url(#Cuivre)", "turquoise": "url(#Turquoise)", "rouge": "url(#OrangeRouge)"}[style]
    stroke = f' stroke="{C["chocolat_fonce"]}" stroke-width="{ry * 0.07:.0f}"' if style == "cuivre" else ""
    txt = C["blanc"] if style == "rouge" else C["chocolat_fonce"]
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"{stroke}/>'
            + (f'<text x="{cx}" y="{cy + size * 0.36:.0f}" text-anchor="middle" font-family="{HEROICA}" '
               f'font-weight="bold" font-size="{size:.0f}" fill="{txt}">{prix}</text>' if prix else "")
            + '</g>')


def badge_fidelite(x, y, w=820):
    h = w * 0.33
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h:.0f}" rx="{h/2:.0f}" fill="{C["chocolat"]}" '
            f'stroke="{C["creme"]}" stroke-width="10"/>'
            f'<circle cx="{x + h/2:.0f}" cy="{y + h/2:.0f}" r="{h/2 - 22:.0f}" fill="{C["creme"]}"/>'
            f'<text x="{x + h/2:.0f}" y="{y + h * 0.64:.0f}" text-anchor="middle" font-family="{IMPACT}" '
            f'font-size="{h * 0.4:.0f}" fill="{C["chocolat"]}">5%</text>'
            f'<text x="{x + h + 10:.0f}" y="{y + h * 0.3:.0f}" font-family="{HEROICA}" font-weight="bold" '
            f'font-size="{h * 0.17:.0f}" fill="{C["creme"]}">toujours crédités</text>'
            f'<text x="{x + h + 10:.0f}" y="{y + h * 0.5:.0f}" font-family="{HEROICA}" font-weight="bold" '
            f'font-size="{h * 0.17:.0f}" fill="{C["creme"]}">en plus sur votre</text>'
            f'<rect x="{x + h:.0f}" y="{y + h * 0.58:.0f}" width="{w - h - 50:.0f}" height="{h * 0.25:.0f}" '
            f'rx="{h * 0.12:.0f}" fill="#C27A3D"/>'
            f'<text x="{x + h + 25:.0f}" y="{y + h * 0.77:.0f}" font-family="{IMPACT}" font-size="{h * 0.18:.0f}" '
            f'fill="{C["chocolat_fonce"]}">CARTE DE FIDÉLITÉ</text></g>')


def photo(x, y, w, h, label):
    """Emplacement photo : à remplacer dans Illustrator (Fichier > Importer, détourage PNG)."""
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="30" fill="#FFFFFF" fill-opacity="0.18" '
            f'stroke="{C["caramel"]}" stroke-width="6" stroke-dasharray="30 20"/>'
            f'<text x="{x + w/2}" y="{y + h/2 + 20}" text-anchor="middle" font-family="{IMPACT}" '
            f'font-size="60" fill="{C["caramel"]}">{label}</text></g>')


def _graisses(body):
    """Eroika Slab n'existe qu'en Normal, Bold et Bold Italic : tout italique passe en Bold Italic."""
    def fix(m):
        t = m.group(0)
        if 'font-style="italic"' in t and "font-weight" not in t:
            t = t.replace('font-style="italic"', 'font-style="italic" font-weight="bold"')
        return t
    return re.sub(r'<text [^>]*font-family="' + HEROICA + r'"[^>]*>', fix, body)


def svg(w, h, body, title):
    body = _graisses(body)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w / 10}mm" height="{h / 10}mm" viewBox="0 0 {w} {h}">\n'
            f'  <title>{title}</title>{DEFS}\n{body}\n</svg>\n')


# --- Gabarit A4 ---------------------------------------------------------------------------
def gabarit():
    W, H = 2100, 2970
    layers = []
    layers.append(f'<g id="FOND"><rect width="{W}" height="{H}" fill="{C["creme"]}"/></g>')
    layers.append(
        '<g id="VAGUES">'
        # bandeau haut en vague (style « Découvrez l'OFFRE+ »)
        f'<path fill="{C["chocolat"]}" d="M0 0H{W}V300C1650 430 1150 220 600 330C350 380 150 420 0 400Z"/>'
        # grande vague basse (style petit-déj : crème en haut, chocolat en bas)
        f'<path fill="{C["chocolat"]}" d="M0 1820C450 1560 900 1700 1350 1560C1700 1450 1900 1250 {W} 1050'
        f'V{H}H0Z"/>'
        # liseré caramel le long de la vague
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="12" d="M0 1790C450 1530 900 1670 1350 1530'
        f'C1700 1420 1900 1220 {W} 1020"/>'
        '</g>')
    layers.append(
        '<g id="PHOTOS">'
        + photo(1180, 1260, 820, 970, "PHOTO PRODUIT 1")
        + photo(180, 2000, 900, 560, "PHOTO PRODUIT 2")
        + photo(1150, 2280, 820, 520, "PHOTO PRODUIT 3")
        + '</g>')
    layers.append(
        '<g id="TEXTES">'
        f'<text x="{W/2}" y="230" text-anchor="middle" font-family="{IMPACT}" font-size="190" '
        f'fill="{C["creme"]}">DÉCOUVREZ NOTRE</text>'
        f'<text x="{W/2}" y="660" text-anchor="middle" font-family="{HEROICA}" font-weight="bold" '
        f'font-size="290" fill="{C["chocolat"]}">Formule Midi</text>'
        + pastille(180, 820, 1200, 230, "Sandwich au choix", size=135)
        + plus(170, 1095, 150)
        + pastille(230, 1140, 1000, 230, "Boisson 33cl")
        + plus(170, 1415, 150)
        + pastille(230, 1460, 900, 230, "Dessert")
        + f'<text x="{W - 160}" y="1930" text-anchor="end" font-family="{HEROICA}" font-style="italic" '
        f'font-weight="bold" font-size="95" fill="{C["creme"]}">Fait maison,</text>'
        f'<text x="{W - 160}" y="2040" text-anchor="end" font-family="{HEROICA}" font-style="italic" '
        f'font-weight="bold" font-size="95" fill="{C["creme"]}">chaque matin !</text>'
        '</g>')
    layers.append('<g id="PRIX">' + ovale_prix(1700, 1010, 330, 175, "9,90€", "cuivre", rot=-4) + '</g>')
    layers.append(
        '<g id="LOGO_MENTIONS">'
        f'<image x="130" y="2560" width="300" height="300" xlink:href="{logo_href()}"/>'
        + badge_fidelite(470, 2610, 760)
        + f'<text x="{W - 60}" y="{H - 40}" text-anchor="end" font-family="{HEROICA}" font-style="italic" '
        f'font-size="42" fill="{C["creme"]}">Photos non contractuelles</text>'
        '</g>')
    return svg(W, H, "\n".join(layers), "Galzin - Gabarit affiche A4")


# --- Bibliothèque d'éléments -----------------------------------------------------------------
def bibliotheque():
    W, H = 3000, 4200
    parts = [f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']

    def titre(y, t):
        return (f'<text x="100" y="{y}" font-family="{IMPACT}" font-size="90" fill="{C["chocolat"]}">{t}</text>')

    # Nuancier
    parts.append(titre(140, "COULEURS"))
    sw = []
    for i, (name, hexa) in enumerate(C.items()):
        x = 100 + (i % 7) * 400
        y = 200 + (i // 7) * 340
        sw.append(f'<rect x="{x}" y="{y}" width="340" height="200" rx="24" fill="{hexa}" stroke="#CCCCCC" '
                  f'stroke-width="3"/><text x="{x}" y="{y + 250}" font-family="{IMPACT}" font-size="36" '
                  f'fill="{C["chocolat"]}">{name.upper()}</text><text x="{x}" y="{y + 300}" '
                  f'font-family="{HEROICA}" font-size="40" fill="{C["chocolat"]}">{hexa}</text>')
    parts.append('<g id="NUANCIER">' + "".join(sw) + '</g>')

    # Typos
    parts.append(titre(1020, "TYPOGRAPHIES"))
    parts.append(
        '<g id="TYPOS">'
        f'<text x="100" y="1210" font-family="{IMPACT}" font-size="170" fill="{C["chocolat"]}">IMPACT — TITRES</text>'
        f'<text x="100" y="1400" font-family="{HEROICA}" font-weight="bold" font-size="170" '
        f'fill="{C["chocolat"]}">Eroika Slab Bold — Accroches</text>'
        f'<text x="100" y="1520" font-family="{HEROICA}" font-style="italic" font-size="90" '
        f'fill="{C["chocolat"]}">Eroika Slab Bold Italique — slogans &amp; mentions</text>'
        '</g>')

    # Ovales de prix
    parts.append(titre(1700, "OVALES DE PRIX"))
    parts.append('<g id="PRIX">'
                 + ovale_prix(520, 1920, 380, 190, "5,50€", "cuivre")
                 + ovale_prix(1480, 1920, 380, 170, "8,20€", "turquoise")
                 + ovale_prix(2440, 1920, 380, 170, "2,90€", "rouge")
                 + '</g>')

    # Pastilles & plus
    parts.append(titre(2240, "PASTILLES PRODUITS"))
    parts.append('<g id="PASTILLES">'
                 + pastille(100, 2300, 1100, 230, "Boisson chaude", rot=-2)
                 + plus(1330, 2415, 150)
                 + pastille(1480, 2300, 1300, 300, "Croissant ou", size=140, rot=1, sous="Pain au Chocolat")
                 + '</g>')

    # Vagues
    parts.append(titre(2800, "BADGE FIDÉLITÉ &amp; LOGO")); parts.append(titre(3380, "VAGUES"))
    parts.append(
        '<g id="VAGUES">'
        f'<g id="Vague_basse"><rect x="100" y="3430" width="850" height="650" fill="{C["creme"]}"/>'
        f'<path fill="{C["chocolat"]}" d="M100 3850C300 3730 500 3800 700 3720C820 3670 900 3590 950 3560V4080H100Z"/></g>'
        f'<g id="Bandeau_haut"><rect x="1070" y="3430" width="850" height="650" fill="{C["creme"]}"/>'
        f'<path fill="{C["chocolat"]}" d="M1070 3430H1920V3550C1750 3610 1550 3520 1350 3570C1250 3595 1150 3610 1070 3605Z"/></g>'
        f'<g id="Bulle_ca"><rect x="2040" y="3430" width="850" height="650" fill="{C["creme"]}"/>'
        f'<path fill="{C["chocolat"]}" d="M2890 3530H2340C2180 3530 2120 3640 2160 3730C2200 3820 2300 3860 2420 3850'
        f'C2600 3840 2750 3900 2890 3990Z"/>'
        f'<text x="2300" y="3740" font-family="{IMPACT}" font-size="120" fill="{C["creme"]}">…À ÇA !</text></g>'
        '</g>')

    parts.append('<g id="FIDELITE">' + badge_fidelite(100, 2900, 820)
                 + f'<image x="1050" y="2870" width="320" height="320" xlink:href="{logo_href()}"/></g>')
    return svg(W, H, "\n".join(parts), "Galzin - Bibliothèque d'éléments")


# --- Nuancier Adobe (.ase) ----------------------------------------------------------------------
def ase():
    blocks = b""
    for name, hexa in C.items():
        r, g, b = (int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5))
        label = f"Galzin {name}".encode("utf-16-be") + b"\x00\x00"
        body = struct.pack(">H", len(label) // 2) + label + b"RGB " + struct.pack(">fffH", r, g, b, 0)
        blocks += struct.pack(">HI", 0x0001, len(body)) + body
    return b"ASEF" + struct.pack(">HHI", 1, 0, len(C)) + blocks


if __name__ == "__main__":
    (Path.cwd() / "galzin-gabarit-A4.svg").write_text(gabarit(), encoding="utf-8")
    (Path.cwd() / "galzin-bibliotheque.svg").write_text(bibliotheque(), encoding="utf-8")
    (Path.cwd() / "galzin-couleurs.ase").write_bytes(ase())
    print("OK")
