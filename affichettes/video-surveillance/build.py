"""Panneaux vidéosurveillance (charte Galzin, voir ../_kit-galzin/CHARTE.md).

Usage : python3 build.py
  -> galzin-videosurveillance-A4.svg     (A4 paysage, mention RGPD / CNIL)
  -> galzin-videoprotection-A5.svg       (A5 paysage, Code de la sécurité intérieure)
Textes légaux repris à l'identique des panneaux existants. Pictogramme caméra 100 % vectoriel.
Dessinés sur une base 2970 x 2100 (0,1 mm), mis à l'échelle pour l'A5.
"""
import base64
import io
import sys
from html import escape
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "_kit-galzin"))
from build import C, IMPACT, HEROICA, svg  # noqa: E402

BW, BH = 2970, 2100


def href(name, max_px=700):
    im = Image.open(HERE / "images" / f"{name}.png")
    im.thumbnail((max_px, max_px))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def text(x, y, txt, size, fill, font=IMPACT, anchor="middle", italic=False, bold=False):
    st = ' font-style="italic"' if italic else ""
    wt = ' font-weight="bold"' if bold else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size:.0f}" fill="{fill}"{st}{wt}>{escape(txt, quote=False)}</text>')


def lignes(x, y, rows, size, fill, lead=1.3, **kw):
    return "".join(text(x, y + i * size * lead, r, size, fill, **kw) for i, r in enumerate(rows))


def camera(cx, cy):
    """Pictogramme caméra crème sur pastille chocolat, point d'enregistrement rouge."""
    c = C["creme"]
    return (f'<g id="picto-camera"><circle cx="{cx}" cy="{cy}" r="360" fill="{C["chocolat"]}" '
            f'stroke="{C["caramel"]}" stroke-width="18"/>'
            f'<path d="M{cx - 30} {cy - 30}V{cy + 170}H{cx - 190}" fill="none" stroke="{c}" stroke-width="44" '
            f'stroke-linejoin="round"/>'
            f'<rect x="{cx - 240}" y="{cy + 80}" width="56" height="190" rx="14" fill="{c}"/>'
            f'<g transform="translate({cx + 20} {cy - 60}) rotate(18)">'
            f'<rect x="-210" y="-85" width="360" height="160" rx="28" fill="{c}"/>'
            f'<rect x="-230" y="-125" width="340" height="44" rx="16" fill="{c}"/>'
            f'<rect x="150" y="-70" width="70" height="130" rx="16" fill="{c}"/>'
            f'<circle cx="-140" cy="0" r="20" fill="{C["rouge"]}"/></g></g>')


def base(titre1, titre2):
    L = [f'<g id="FOND"><rect width="{BW}" height="{BH}" fill="{C["creme"]}"/></g>']
    L.append(
        '<g id="VAGUES">'
        f'<path fill="{C["chocolat"]}" d="M0 0H{BW}V470C2300 600 1500 380 800 500C450 560 200 570 0 550Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="12" d="M0 600C200 620 450 610 800 555'
        f'C1500 435 2300 655 {BW} 525"/>'
        f'<path fill="{C["chocolat"]}" d="M0 1560C1000 1420 2000 1640 {BW} 1470V{BH}H0Z"/>'
        f'<path fill="none" stroke="{C["caramel"]}" stroke-width="12" d="M0 1505C1000 1365 2000 1585 {BW} 1415"/>'
        '</g>')
    L.append(f'<image id="galzin-logo" x="70" y="40" width="420" height="420" xlink:href="{href("galzin-logo")}"/>'
             + text(1720, 230, titre1, 175, C["creme"]) + text(1720, 420, titre2, 175, C["creme"]))
    return L


def panneau_rgpd():
    L = base("CE MAGASIN EST", "SOUS VIDÉO SURVEILLANCE")
    L.append('<g id="PICTO">' + camera(560, 1030) + '</g>')
    L.append(
        '<g id="TEXTES">'
        + lignes(1050, 900, ["Pour votre sécurité", "et celle de tous, nos locaux sont",
                             "placés sous vidéo surveillance."], 110, C["chocolat"], 1.25, font=HEROICA,
                 anchor="start", bold=True)
        # mentions légales (texte d'origine)
        + f'<circle cx="170" cy="1700" r="58" fill="none" stroke="{C["cuivre_clair"]}" stroke-width="10"/>'
        + text(170, 1735, "i", 95, C["cuivre_clair"], HEROICA, bold=True, italic=True)
        + lignes(270, 1690, ["Conformément au Règlement Général sur la Protection des Données",
                             "(RGPD – UE 2016/679) et à la loi Informatique et Libertés modifiée",
                             "(Loi n°78-17 du 6 janvier 1978), vous disposez d'un droit d'accès,",
                             "de rectification et d'opposition aux données vous concernant."],
                 41, C["creme"], 1.4, font=HEROICA, anchor="start")
        + f'<path d="M1600 1650V1960" stroke="{C["caramel"]}" stroke-width="6"/>'
        + lignes(1680, 1690, ["Pour exercer vos droits ou pour toute question relative",
                              "à la gestion de vos données, vous pouvez vous adresser",
                              "au responsable du traitement dans ce magasin."],
                 41, C["creme"], 1.4, font=HEROICA, anchor="start")
        + text(1680, 1950, "Pour en savoir plus : ", 41, C["creme"], HEROICA, anchor="start")
        + text(2090, 1950, "www.cnil.fr", 46, C["cuivre_clair"], HEROICA, anchor="start", bold=True)
        + '</g>')
    return svg(BW, BH, "\n".join(L), "Galzin - Vidéosurveillance A4")


def panneau_csi(W=2100, H=1480):
    s = W / BW
    L = base("SITE SOUS", "VIDÉOPROTECTION")
    L.append('<g id="PICTO">' + camera(560, 1030) + '</g>')
    L.append(
        '<g id="TEXTES">'
        + text(1050, 860, "Code de la Sécurité Intérieure", 105, C["chocolat"], HEROICA, "start", bold=True)
        + lignes(1050, 990, ["(art. L223-1 à L223-9 et L251-1 à L255-1)",
                             "Décret n°96-926 du 17 octobre 1996",
                             "modifié par la loi n°2011-267 du 14 mars 2011"],
                 80, C["chocolat"], 1.35, font=HEROICA, anchor="start")
        + text(BW / 2, 1740, "Pour toute information relative au droit d'accès à l'image, s'adresser à :",
               66, C["creme"], HEROICA, italic=True, bold=True)
        + text(BW / 2, 1900, "SERVICE VIDÉOSURVEILLANCE", 120, C["cuivre_clair"])
        + text(BW / 2, 2040, "TÉL. 05 65 74 93 84", 110, C["creme"])
        + '</g>')
    body = f'<g transform="scale({s:.6f})">' + "\n".join(L) + '</g>'
    return svg(W, H, body, "Galzin - Vidéoprotection A5")


if __name__ == "__main__":
    for name, content in (("galzin-videosurveillance-A4.svg", panneau_rgpd()),
                          ("galzin-videoprotection-A5.svg", panneau_csi())):
        (HERE / name).write_text(content, encoding="utf-8")
        print(name, f"{len(content) / 1e6:.2f} Mo")
