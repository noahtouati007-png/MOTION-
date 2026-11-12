"""Sticker « Tableau des allergènes » avec QR code (charte Galzin, variante claire), 120 x 100 mm paysage.

Usage : python3 build.py  ->  galzin-sticker-allergenes.svg (1 unité = 0,1 mm).
QR code vectoriel : même lien que l'ancien sticker. Fond perdu 2 mm ; calque DECOUPE = carré de coupe.
"""
import sys
from pathlib import Path

import qrcode

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

W, H = 1200, 1000
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
            f'height="{size + 2 * pad:.1f}" rx="18" fill="#FFFFFF" stroke="{CH}" stroke-width="6"/><path fill="{CF}" d="{d}"/></g>')


def sticker():
    L = [f'<g id="FOND"><rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="{C["sable"]}"/>'
         f'<rect x="40" y="40" width="{W - 80}" height="{H - 80}" rx="30" fill="{CR}" stroke="{CH}" stroke-width="6"/>'
         f'<rect x="58" y="58" width="{W - 116}" height="{H - 116}" rx="22" fill="none" stroke="{CA}" stroke-width="3"/>'
         f'<path fill="{CH}" d="M40 790H{W - 40}V{H - 70}Q{W - 40} {H - 40} {W - 70} {H - 40}H70Q40 {H - 40} 40 {H - 70}Z"/></g>']
    L.append(
        '<g id="TEXTES">'
        + logo(95, 95, 170)
        + text(95, 395, "TABLEAU", 120, CH, anchor="start")
        + text(95, 510, "DES", 120, CH, anchor="start")
        + text(95, 625, "ALLERGÈNES", 120, CA, anchor="start")
        + f'<path d="M100 665H560" stroke="{CC}" stroke-width="10" stroke-linecap="round"/>'
        + text(95, 735, "Scannez le QR code", 46, CH, HEROICA, "start", italic=True, bold=True)
        + qr(700, 150, 400)
        + text(W / 2, 870, "Disponible au format papier", 50, CC, HEROICA, bold=True)
        + text(W / 2, 925, "Adressez-vous à la vendeuse / au vendeur", 40, CR, HEROICA, italic=True, bold=True)
        + '</g>')
    L.append(f'<g id="DECOUPE"><rect width="{W}" height="{H}" fill="none" stroke="#E30F20" stroke-width="3"/></g>')
    return svg(W, H, "\n".join(L), "Galzin - Sticker allergènes")

if __name__ == "__main__":
    (HERE / "galzin-sticker-allergenes.svg").write_text(sticker(), encoding="utf-8")
