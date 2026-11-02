"""Génère le kit de marque Immo Décodé : logos SVG (texte vectorisé + version texte éditable),
illustrations SVG, nuancier .ase pour Illustrator, polices TTF.

Usage : python3 charte-graphique/_source/build_brand.py   (depuis la racine du dépôt)
Dépendances : pip install fonttools brotli
"""

import os
import struct

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
W2 = os.path.join(HERE, "woff2")

COLORS = {
    "nuit": ("Bleu nuit", "#1F2A44"),
    "terra": ("Terracotta", "#C8553D"),
    "sable": ("Sable", "#F2E8DC"),
    "sable_clair": ("Sable clair", "#FBF6EF"),
    "olive": ("Vert olivier", "#6B7F4E"),
}
C = {k: v[1] for k, v in COLORS.items()}


def mkdir(*p):
    d = os.path.join(OUT, *p)
    os.makedirs(d, exist_ok=True)
    return d


# ---------------------------------------------------------------- polices
FONT_FILES = {
    "Fraunces-Regular.ttf": "fraunces-latin-400-normal.woff2",
    "Fraunces-SemiBold.ttf": "fraunces-latin-600-normal.woff2",
    "Fraunces-SemiBoldItalic.ttf": "fraunces-latin-600-italic.woff2",
    "Fraunces-Bold.ttf": "fraunces-latin-700-normal.woff2",
    "Fraunces-Black.ttf": "fraunces-latin-900-normal.woff2",
    "Inter-Regular.ttf": "inter-latin-400-normal.woff2",
    "Inter-Medium.ttf": "inter-latin-500-normal.woff2",
    "Inter-Bold.ttf": "inter-latin-700-normal.woff2",
    "Inter-ExtraBold.ttf": "inter-latin-800-normal.woff2",
}


def build_fonts():
    d = mkdir("polices")
    for ttf, w in FONT_FILES.items():
        f = TTFont(os.path.join(W2, w))
        f.flavor = None
        f.save(os.path.join(d, ttf))
    for lic in ("OFL-Fraunces.txt", "OFL-Inter.txt"):
        with open(os.path.join(W2, lic), "rb") as a, open(os.path.join(d, lic), "wb") as b:
            b.write(a.read())


FR_BOLD = TTFont(os.path.join(W2, "fraunces-latin-700-normal.woff2"))
FR_BLACK = TTFont(os.path.join(W2, "fraunces-latin-900-normal.woff2"))
INTER_B = TTFont(os.path.join(W2, "inter-latin-700-normal.woff2"))


def text_width(font, text, size, tracking=0.0):
    cmap = font.getBestCmap()
    s = size / font["head"].unitsPerEm
    return sum(font["hmtx"][cmap[ord(ch)]][0] * s for ch in text) + tracking * (len(text) - 1)


def text_path(font, text, size, x, y, tracking=0.0):
    """Chemin SVG du texte, ligne de base en (x, y)."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    s = size / font["head"].unitsPerEm
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += font["hmtx"][g][0] * s + tracking
    return pen.getCommands()


def cap_height(font, size):
    return font["OS/2"].sCapHeight * size / font["head"].unitsPerEm


def svg(w, h, body, title):
    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}">\n'
        f"<title>{title}</title>\n{body}\n</svg>\n"
    )


def roof(cx, top, half_w, height, stroke, color, sw):
    return (
        f'<path id="toit" d="M{cx - half_w:.1f} {top + height:.1f} L{cx:.1f} {top:.1f} L{cx + half_w:.1f} {top + height:.1f}" '
        f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


# ---------------------------------------------------------------- logos
def logo_vertical(ink, accent, bg=None, editable=False):
    size = 220
    l1, l2 = "IMMO", "DÉCODÉ"
    w1, w2 = text_width(FR_BOLD, l1, size), text_width(FR_BOLD, l2, size)
    cap = cap_height(FR_BOLD, size)
    pad = 60
    W = max(w1, w2) + 2 * pad
    cx = W / 2
    roof_top = pad
    roof_h = 150
    b1 = roof_top + roof_h + 50 + cap
    b2 = b1 + cap + 95
    bar_y = b2 + 52
    bar_w = w2 * 0.38
    H = bar_y + 20 + pad
    parts = []
    if bg:
        parts.append(f'<rect id="fond" width="{W:.0f}" height="{H:.0f}" fill="{bg}"/>')
    parts.append(roof(cx, roof_top, w1 * 0.55, roof_h, None, accent, 26))
    if editable:
        style = f'font-family="Fraunces" font-weight="700" font-size="{size}" fill="{ink}" text-anchor="middle"'
        parts.append(f'<text id="immo" x="{cx:.1f}" y="{b1:.1f}" {style}>{l1}</text>')
        parts.append(f'<text id="decode" x="{cx:.1f}" y="{b2:.1f}" {style}>{l2}</text>')
    else:
        parts.append(f'<path id="immo" fill="{ink}" d="{text_path(FR_BOLD, l1, size, cx - w1 / 2, b1)}"/>')
        parts.append(f'<path id="decode" fill="{ink}" d="{text_path(FR_BOLD, l2, size, cx - w2 / 2, b2)}"/>')
    parts.append(f'<rect id="barre" x="{cx - bar_w / 2:.1f}" y="{bar_y:.1f}" width="{bar_w:.1f}" height="20" rx="10" fill="{accent}"/>')
    return W, H, "\n".join(parts)


def mark(x, y, s, fill, fg, accent=None):
    """Monogramme : carré arrondi, toit + « ID ». s = côté."""
    accent = accent or fg
    size = s * 0.5
    t = "ID"
    w = text_width(FR_BLACK, t, size)
    cap = cap_height(FR_BLACK, size)
    base = y + s * 0.80
    parts = [
        f'<rect id="monogramme-fond" x="{x:.1f}" y="{y:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s * 0.2:.1f}" fill="{fill}"/>',
        roof(x + s / 2, y + s * 0.17, s * 0.3, s * 0.15, None, accent, round(s * 0.06)),
        f'<path id="monogramme-id" fill="{fg}" d="{text_path(FR_BLACK, t, size, x + s / 2 - w / 2, base)}"/>',
    ]
    _ = cap
    return "\n".join(parts)


def logo_horizontal(ink, accent, mark_fill, mark_fg, bg=None):
    s = 300
    size = 150
    name = "IMMO DÉCODÉ"
    tag = "L'IMMO EN 30 SECONDES"
    wn = text_width(FR_BOLD, name, size)
    tag_size = 40
    tr = 9
    wt = text_width(INTER_B, tag, tag_size, tr)
    pad = 50
    gap = 60
    W = pad + s + gap + max(wn, wt) + pad
    H = pad + s + pad
    tx = pad + s + gap
    capn = cap_height(FR_BOLD, size)
    base_n = pad + s / 2 + capn / 2 - 20
    parts = []
    if bg:
        parts.append(f'<rect id="fond" width="{W:.0f}" height="{H:.0f}" fill="{bg}"/>')
    parts.append(mark(pad, pad, s, mark_fill, mark_fg))
    parts.append(f'<path id="nom" fill="{ink}" d="{text_path(FR_BOLD, name, size, tx, base_n)}"/>')
    parts.append(f'<path id="signature" fill="{accent}" d="{text_path(INTER_B, tag, tag_size, tx + 4, base_n + 78, tr)}"/>')
    return W, H, "\n".join(parts)


def build_logos():
    d = mkdir("logo")
    variants = {
        "logo-principal-couleur": logo_vertical(C["nuit"], C["terra"]),
        "logo-principal-sur-sable": logo_vertical(C["nuit"], C["terra"], bg=C["sable"]),
        "logo-principal-negatif": logo_vertical(C["sable_clair"], C["terra"], bg=C["nuit"]),
        "logo-principal-mono-nuit": logo_vertical(C["nuit"], C["nuit"]),
        "logo-principal-mono-blanc": logo_vertical("#FFFFFF", "#FFFFFF"),
        "logo-horizontal-couleur": logo_horizontal(C["nuit"], C["terra"], C["terra"], C["sable_clair"]),
        "logo-horizontal-negatif": logo_horizontal(C["sable_clair"], C["terra"], C["terra"], C["sable_clair"], bg=C["nuit"]),
    }
    for name, (w, h, body) in variants.items():
        with open(os.path.join(d, name + ".svg"), "w") as f:
            f.write(svg(w, h, body, "Immo Décodé — " + name))
    w, h, body = logo_vertical(C["nuit"], C["terra"], editable=True)
    with open(os.path.join(d, "logo-principal-TEXTE-EDITABLE.svg"), "w") as f:
        f.write(svg(w, h, body, "Immo Décodé — texte éditable (installer les polices du dossier polices/)"))
    for name, fill, fg in (
        ("monogramme-terracotta", C["terra"], C["sable_clair"]),
        ("monogramme-nuit", C["nuit"], C["sable_clair"]),
        ("monogramme-sable", C["sable"], C["nuit"]),
    ):
        acc = C["terra"] if fill != C["terra"] else C["sable_clair"]
        with open(os.path.join(d, name + ".svg"), "w") as f:
            f.write(svg(600, 600, mark(0, 0, 600, fill, fg, acc), "Immo Décodé — " + name))
    # Photo de profil (cercle) : même dessin, recadré rond par les réseaux
    with open(os.path.join(d, "photo-de-profil.svg"), "w") as f:
        f.write(svg(1080, 1080, f'<rect width="1080" height="1080" fill="{C["terra"]}"/>\n' + mark(140, 140, 800, C["terra"], C["sable_clair"]), "Photo de profil"))


# ---------------------------------------------------------------- illustrations
ICON_STYLE = 'fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "maison": ['<path d="M18 58 L60 22 L102 58"/>', '<path d="M30 48 V100 H90 V48"/>', '<path d="M50 100 V72 H70 V100"/>'],
    "cle": ['<circle cx="38" cy="60" r="20"/>', '<path d="M58 60 H104 M90 60 V76 M104 60 V72"/>'],
    "calculatrice": ['<rect x="28" y="14" width="64" height="92" rx="12"/>', '<rect x="40" y="26" width="40" height="18" rx="4"/>', '<path d="M42 62h8M70 62h8M42 78h8M70 78h8M42 94h8M70 94h8M56 62h8M56 94h8"/>'],
    "marteau": ['<path d="M24 26 h56 a8 8 0 0 1 8 8 v10 a8 8 0 0 1 -8 8 h-56 z"/>', '<path d="M88 34 h14"/>', '<path d="M50 52 v54"/>'],
    "appareil-photo": ['<path d="M18 40 h84 a8 8 0 0 1 8 8 v46 a8 8 0 0 1 -8 8 h-84 a8 8 0 0 1 -8 -8 v-46 a8 8 0 0 1 8 -8 z"/>', '<path d="M40 40 l8 -14 h24 l8 14"/>', '<circle cx="60" cy="71" r="18"/>'],
    "epingle": ['<path d="M60 108 C60 108 28 74 28 50 a32 32 0 0 1 64 0 c0 24 -32 58 -32 58 z"/>', '<circle cx="60" cy="50" r="11"/>'],
    "signet": ['<path d="M34 14 h52 a6 6 0 0 1 6 6 v88 l-32 -22 l-32 22 v-88 a6 6 0 0 1 6 -6 z"/>'],
    "plan": ['<rect x="14" y="18" width="92" height="84" rx="4"/>', '<path d="M14 62 H52 M70 62 H106 M60 18 V44"/>'],
    "graphique": ['<path d="M16 104 H106"/>', '<path d="M30 90 V70 M54 90 V54 M78 90 V40 M102 90 V24"/>', '<path d="M24 50 L48 36 L70 42 L100 16"/>'],
    "euro": ['<path d="M88 30 a34 34 0 1 0 0 60"/>', '<path d="M20 52 H70 M20 68 H66"/>'],
    "document": ['<path d="M30 12 h42 l20 20 v76 h-62 z"/>', '<path d="M72 12 v20 h20"/>', '<path d="M44 58 h32 M44 74 h32 M44 90 h20"/>'],
    "loupe": ['<circle cx="52" cy="52" r="30"/>', '<path d="M74 74 L104 104"/>'],
}


def build_icons():
    d = mkdir("illustrations")
    names = list(ICONS)
    for n in names:
        for cname in ("nuit", "terra"):
            body = f'<g id="{n}" {ICON_STYLE.format(c=C[cname])}>\n' + "\n".join(ICONS[n]) + "\n</g>"
            with open(os.path.join(d, f"{n}-{cname}.svg"), "w") as f:
                f.write(svg(120, 120, body, n))
    cols = 6
    cell = 200
    rows = (len(names) + cols - 1) // cols
    W, H = cols * cell + 80, rows * (cell + 50) + 80
    parts = [f'<rect width="{W}" height="{H}" fill="{C["sable"]}"/>']
    for i, n in enumerate(names):
        x = 40 + (i % cols) * cell + 40
        y = 40 + (i // cols) * (cell + 50) + 20
        parts.append(f'<g id="{n}" transform="translate({x} {y})" {ICON_STYLE.format(c=C["nuit"])}>' + "".join(ICONS[n]) + "</g>")
        lw = text_width(INTER_B, n, 22)
        parts.append(f'<path fill="{C["nuit"]}" d="{text_path(INTER_B, n, 22, x + 60 - lw / 2, y + 160)}"/>')
    with open(os.path.join(d, "planche-illustrations.svg"), "w") as f:
        f.write(svg(W, H, "\n".join(parts), "Planche des illustrations Immo Décodé"))


# ---------------------------------------------------------------- nuancier
def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def rgb_cmyk(r, g, b):
    r, g, b = r / 255, g / 255, b / 255
    k = 1 - max(r, g, b)
    if k >= 1:
        return 0, 0, 0, 100
    return tuple(round(v * 100) for v in ((1 - r - k) / (1 - k), (1 - g - k) / (1 - k), (1 - b - k) / (1 - k), k))


def build_swatches():
    d = mkdir("couleurs")
    blocks = b""
    for _k, (name, hx) in COLORS.items():
        r, g, b = (v / 255 for v in hex_rgb(hx))
        label = "Immo Décodé " + name
        nm = (label + "\0").encode("utf-16-be")
        body = struct.pack(">H", len(label) + 1) + nm + b"RGB " + struct.pack(">fff", r, g, b) + struct.pack(">H", 0)
        blocks += struct.pack(">HI", 0x0001, len(body)) + body
    with open(os.path.join(d, "immo-decode-nuancier.ase"), "wb") as f:
        f.write(b"ASEF" + struct.pack(">HHI", 1, 0, len(COLORS)) + blocks)
    lines = ["Couleurs Immo Décodé", "", "Nom | HEX | RGB | CMJN (approximatif, à valider avec l'imprimeur)"]
    for _k, (name, hx) in COLORS.items():
        r, g, b = hex_rgb(hx)
        c, m, y, k = rgb_cmyk(r, g, b)
        lines.append(f"{name} | {hx} | {r} {g} {b} | C{c} M{m} J{y} N{k}")
    with open(os.path.join(d, "couleurs.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    build_fonts()
    build_logos()
    build_icons()
    build_swatches()
    print("Kit de marque généré dans", OUT)
