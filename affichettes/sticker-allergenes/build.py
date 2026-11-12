"""Sticker « Tableau des allergènes » avec QR code (charte Galzin), 100 x 100 mm.

Usage : python3 build.py  ->  galzin-sticker-allergenes.svg (1 unité = 0,1 mm).
QR code vectoriel : même lien que l'ancien sticker. Fond perdu 2 mm ; calque DECOUPE = carré de coupe.
"""
import sys
from pathlib import Path

import qrcode

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

W = H = 1000
URL = "https://vqr.vc/7r3FJbVdm"  # lien de l'ancien sticker
CH, CR, CA, CC, CF = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"], C["chocolat_fonce"]


def qr(x, y, size):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(URL)
    q.make(fit=True)
    m = q.get_matrix()
    c = size / len(m)
    d = "".join(f"M{x + j * c:.2f} {y + i * c:.2f}h{c:.2f}v{c:.2f}h{-c:.2f}z"
                for i, row in enumerate(m) for j, v in enumerate(row) if v)
    pad = c * 3
    return (f'<g id="QR_CODE"><rect x="{x - pad:.1f}" y="{y - pad:.1f}" width="{size + 2 * pad:.1f}" '
            f'height="{size + 2 * pad:.1f}" rx="18" fill="#FFFFFF"/><path fill="{CF}" d="{d}"/></g>')


def sticker():
    L = [f'<g id="FOND"><rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="{CH}"/>'
         f'<path d="M-20 255C300 215 700 290 {W + 20} 235" fill="none" stroke="{CA}" stroke-width="8"/></g>']
    L.append(
        '<g id="TEXTES">'
        + logo(40, 30, 175)
        + text(605, 120, "TABLEAU DES", 92, CR)
        + text(605, 215, "ALLERGÈNES", 92, CC)
        + qr(330, 300, 340)
        + text(W / 2, 740, "Scannez pour le consulter", 46, CR, HEROICA, italic=True, bold=True)
        + f'<rect x="60" y="790" width="880" height="160" rx="45" fill="{CC}"/>'
        + text(W / 2, 858, "Disponible au format papier :", 44, CF, HEROICA, bold=True)
        + text(W / 2, 916, "adressez-vous à la vendeuse / au vendeur", 38, CF, HEROICA, bold=True)
        + '</g>')
    L.append(f'<g id="DECOUPE"><rect width="{W}" height="{H}" fill="none" stroke="#E30F20" stroke-width="3"/></g>')
    return svg(W, H, "\n".join(L), "Galzin - Sticker allergènes")


if __name__ == "__main__":
    (HERE / "galzin-sticker-allergenes.svg").write_text(sticker(), encoding="utf-8")
