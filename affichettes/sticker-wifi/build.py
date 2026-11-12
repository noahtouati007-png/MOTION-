"""Sticker « Codes Wifi » 15 x 10 cm (même DA claire que le sticker allergènes) + QR code de connexion.

Usage : python3 build.py  ->  galzin-sticker-wifi.svg (1 unité = 0,1 mm).
Le QR code connecte directement au wifi (format WIFI:, WPA). Fond perdu 2 mm ; calque DECOUPE.
"""
import sys
from pathlib import Path

import qrcode

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/galzin-da/scripts"))
from galzin_kit import C, IMPACT, HEROICA, svg, text, logo  # noqa: E402

W, H = 1500, 1000
RESEAU, MDP = "GALZIN-WIFI-GUEST", "galzin01#"
CH, CR, CA, CC, CF = C["chocolat"], C["creme"], C["caramel"], C["cuivre_clair"], C["chocolat_fonce"]


def qr(x, y, size):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(f"WIFI:T:WPA;S:{RESEAU};P:{MDP};;")
    q.make(fit=True)
    m = q.get_matrix()
    c = size / len(m)
    d = "".join(f"M{x + j * c:.2f} {y + i * c:.2f}h{c:.2f}v{c:.2f}h{-c:.2f}z"
                for i, row in enumerate(m) for j, v in enumerate(row) if v)
    p = c * 3
    return (f'<g id="QR_CODE"><rect x="{x - p:.1f}" y="{y - p:.1f}" width="{size + 2 * p:.1f}" height="{size + 2 * p:.1f}" '
            f'rx="18" fill="#FFFFFF" stroke="{CH}" stroke-width="6"/><path fill="{CF}" d="{d}"/></g>')


def wifi(cx, cy, s=1.0):
    arcs = "".join(f'<path d="M{cx - r} {cy - r * 0.15}A{r * 1.25} {r * 1.25} 0 0 1 {cx + r} {cy - r * 0.15}" '
                   f'fill="none" stroke="{CA}" stroke-width="{22 * s:.0f}" stroke-linecap="round"/>'
                   for r in (int(110 * s), int(72 * s), int(36 * s)))
    return f'<g id="picto-wifi">{arcs}<circle cx="{cx}" cy="{cy + 22 * s:.0f}" r="{16 * s:.0f}" fill="{CA}"/></g>'


def sticker():
    L = [f'<g id="FOND"><rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="{C["sable"]}"/>'
         f'<rect x="40" y="40" width="{W - 80}" height="{H - 80}" rx="30" fill="{CR}" stroke="{CH}" stroke-width="6"/>'
         f'<rect x="58" y="58" width="{W - 116}" height="{H - 116}" rx="22" fill="none" stroke="{CA}" stroke-width="3"/>'
         f'<path fill="{CH}" d="M40 800H{W - 40}V{H - 70}Q{W - 40} {H - 40} {W - 70} {H - 40}H70Q40 {H - 40} 40 {H - 70}Z"/></g>']
    L.append(
        '<g id="TEXTES">'
        + logo(130, 120, 150)
        + text(320, 230, "CODES WIFI", 120, CH, anchor="start")
        + wifi(895, 215, 0.55)
        + text(130, 400, "RÉSEAU", 54, CA, anchor="start", spacing=6)
        + text(130, 490, RESEAU, 84, CH, anchor="start")
        + text(130, 590, "MOT DE PASSE", 54, CA, anchor="start", spacing=6)
        + text(130, 680, MDP, 84, CH, anchor="start")
        + qr(1020, 180, 340)
        + text(1190, 600, "Scannez pour", 44, CH, HEROICA, italic=True, bold=True)
        + text(1190, 655, "vous connecter", 44, CH, HEROICA, italic=True, bold=True)
        + text(W / 2, 905, "Connexion offerte à notre clientèle", 52, CC, HEROICA, italic=True, bold=True)
        + '</g>')
    L.append(f'<g id="DECOUPE"><rect width="{W}" height="{H}" fill="none" stroke="#E30F20" stroke-width="3"/></g>')
    return svg(W, H, "\n".join(L), "Galzin - Sticker wifi")


if __name__ == "__main__":
    (HERE / "galzin-sticker-wifi.svg").write_text(sticker(), encoding="utf-8")
