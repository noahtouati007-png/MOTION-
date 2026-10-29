"""Flyer A5 recto-verso « On recrute » (World Job Café Montpellier), charte Galzin simplifiée.

Usage : python3 build.py  ->  galzin-flyer-recrutement-A5.svg
Recto (groupe RECTO) et verso (groupe VERSO) côte à côte, 148 x 210 mm chacun (1 unité = 0,1 mm).
Les éléments [À COMPLÉTER] (contact, QR code) sont à remplir dans Illustrator.
"""
import base64
import io
import sys
from html import escape
from pathlib import Path

import qrcode
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "_kit-galzin"))
from build import C, IMPACT, HEROICA, svg  # noqa: E402

W, H, GAP = 1480, 2100, 120
CH, CR, CA, CC = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"]


def logo(x, y, s):
    im = Image.open(HERE / "images" / "galzin-logo.png")
    im.thumbnail((600, 600))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    d = base64.b64encode(buf.getvalue()).decode()
    return f'<image x="{x}" y="{y}" width="{s}" height="{s}" xlink:href="data:image/png;base64,{d}"/>'


def t(x, y, txt, size, fill, font=HEROICA, anchor="start", bold=False, italic=False, ls=0):
    a = (' font-weight="bold"' if bold else "") + (' font-style="italic"' if italic else "")
    a += f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" font-family="{font}" '
            f'font-size="{size:.0f}" fill="{fill}"{a}>{escape(txt, quote=False)}</text>')


def lines(x, y, rows, size, fill, lead=1.3, **kw):
    return "".join(t(x, y + i * size * lead, r, size, fill, **kw) for i, r in enumerate(rows))


def puces(x, y, rows, size, fill, lead=1.35):
    out = ""
    for i, r in enumerate(rows):
        yy = y + i * size * lead
        out += f'<circle cx="{x + 10}" cy="{yy - size * 0.32:.0f}" r="{size * 0.16:.0f}" fill="{CA}"/>'
        out += t(x + 40, yy, r, size, fill)
    return out


MAIL = "philippe@galzin.fr"
QR_URL = f"mailto:{MAIL}?subject=Candidature%20Galzin%20-%20World%20Job%20Caf%C3%A9"


def qr_vectoriel(x, y, size, data=QR_URL):
    """QR code 100 % vectoriel (un carré par module), modifiable dans Illustrator."""
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(data)
    q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    c = size / n
    d = "".join(f"M{x + j * c:.2f} {y + i * c:.2f}h{c:.2f}v{c:.2f}h{-c:.2f}z"
                for i, row in enumerate(m) for j, v in enumerate(row) if v)
    return (f'<g id="QR_CODE"><rect x="{x - c * 2:.1f}" y="{y - c * 2:.1f}" width="{size + c * 4:.1f}" '
            f'height="{size + c * 4:.1f}" fill="#FFFFFF"/><path fill="{CH}" d="{d}"/></g>')


def bandeau(titre, sous):
    return (f'<rect width="{W}" height="{H}" fill="{CR}"/>'
            f'<path fill="{CH}" d="M0 0H{W}V430C1100 520 700 380 350 450C200 480 80 490 0 480Z"/>'
            f'<path fill="none" stroke="{CA}" stroke-width="8" d="M0 520C80 530 200 520 350 490'
            f'C700 420 1100 560 {W} 470"/>'
            + logo(50, 45, 300)
            + t(890, 200, titre, 150, CR, IMPACT, "middle")
            + t(890, 330, sous, 66, CC, HEROICA, "middle", bold=True, italic=True))


def pied(txt):
    return (f'<path fill="{CH}" d="M0 1960C500 1900 1000 1990 {W} 1930V{H}H0Z"/>'
            + t(W / 2, 2055, txt, 46, CR, IMPACT, "middle", ls=4))


def recto():
    o = bandeau("ON RECRUTE !", "World Job Café · Montpellier")
    o += t(80, 680, "GALZIN, C'EST QUOI ?", 70, CH, IMPACT)
    o += lines(80, 770, ["Une maison de boulangerie-pâtisserie fondée en 1938.",
                          "Pains, viennoiseries, pâtisseries, sandwichs, pizzas",
                          "et snacking : fabriqués avec soin, chaque jour,",
                          "pour nos clients."], 46, CH, 1.4)
    # chiffre clé
    o += (f'<rect x="80" y="1010" width="{W - 160}" height="250" rx="40" fill="{CH}"/>'
          + t(290, 1190, "20", 190, CC, IMPACT, "middle")
          + lines(500, 1110, ["Une vingtaine d'établissements", "à Montpellier"], 58, CR, 1.25, bold=True))
    o += t(80, 1420, "DEUX FAÇONS DE TRAVAILLER AVEC NOUS", 58, CH, IMPACT)
    for i, (titre, rows) in enumerate((
            ("En fixe", ["Une boutique de rattachement,", "une équipe, des habitudes."]),
            ("En itinérant", ["Vous tournez entre plusieurs", "boutiques selon les besoins."]))):
        x = 80 + i * 680
        o += (f'<rect x="{x}" y="1480" width="640" height="340" rx="30" fill="{C["sable"]}"/>'
              + t(x + 40, 1580, titre, 72, CH, bold=True)
              + lines(x + 40, 1680, rows, 40, CH, 1.4))
    o += pied("PLUS DE 85 ANS DE SAVOIR-FAIRE")
    return o


def verso():
    o = bandeau("NOS POSTES", "CDI, CDD, temps partiel, étudiants...")
    jobs = (("VENDEUR / VENDEUSE", ["Accueil et conseil des clients", "Mise en place de la vitrine, réassort",
                                    "Préparation sandwichs et boissons, encaissement"]),
            ("BOULANGER / BOULANGÈRE", ["Pétrissage, façonnage, cuisson", "Pains et viennoiseries de nos recettes",
                                        "Hygiène et organisation du fournil"]),
            ("CUISINIER / CUISINIÈRE", ["Sandwichs, salades, pizzas et plats", "Mise en place et préparation snacking",
                                        "Respect des règles d'hygiène (HACCP)"]))
    y = 640
    for titre, rows in jobs:
        o += (f'<rect x="80" y="{y - 70}" width="{W - 160}" height="90" rx="22" fill="{CH}"/>'
              + t(120, y, titre, 62, CR, IMPACT)
              + puces(110, y + 95, rows, 42, CH))
        y += 360
    o += (f'<rect x="80" y="1640" width="{W - 160}" height="280" rx="30" fill="none" stroke="{CA}" '
          f'stroke-width="8"/>'
          + t(120, 1720, "Étudiant(e) ou débutant(e) ?", 52, CH, bold=True)
          + lines(120, 1775, ["Parlons de vos disponibilités.", "Contact : Philippe"], 40, CH, 1.35)
          + t(120, 1890, MAIL, 46, CA, bold=True)
          + qr_vectoriel(1180, 1670, 170)
          + t(1265, 1895, "Scannez pour postuler", 24, CH, anchor="middle", italic=True))
    o += pied("VENEZ NOUS RENCONTRER SUR NOTRE STAND !")
    return o


if __name__ == "__main__":
    body = (f'<g id="RECTO">{recto()}</g>'
            f'<g id="VERSO" transform="translate({W + GAP} 0)">{verso()}</g>')
    s = svg(W * 2 + GAP, H, body, "Galzin - Flyer recrutement A5")
    (HERE / "galzin-flyer-recrutement-A5.svg").write_text(s, encoding="utf-8")
    print(f"{len(s) / 1e6:.2f} Mo")
