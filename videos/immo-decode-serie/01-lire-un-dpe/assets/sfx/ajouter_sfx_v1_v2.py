"""Ajoute effets sonores, volets de transition, fond animé et barre de progression
aux 3 premières vidéos faites à la main (V1, V2, V2 bis). Idempotent : relançable.

Usage : python3 videos/immo-decode-serie/_sfx/ajouter_sfx_v1_v2.py
"""

import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.dirname(os.path.dirname(HERE))
LEN = {"whoosh-short": 0.57, "pop": 0.72, "click-soft": 0.37, "click": 0.37, "impact-bass-1": 2.12, "impact-bass-2": 2.59, "typing": 1.5, "ping": 1.32, "sparkle": 1.8, "key-press": 0.4}

# (projet, durée totale, débuts de scène où passe un volet, effets [(son, t, volume, durée max)])
PLAN = {
    "immo-decode-v1-bienvenue": (15, [6.4, 9.5, 12.8], [
        ("typing", 0.1, 0.22, 1.4), ("impact-bass-1", 1.4, 0.45, None), ("whoosh-short", 2.9, 0.4, None),
        ("pop", 3.35, 0.45, None), ("pop", 3.7, 0.45, None), ("pop", 4.05, 0.45, None), ("click", 4.45, 0.35, None),
        ("click-soft", 6.5, 0.4, None), ("click-soft", 7.0, 0.4, None), ("impact-bass-2", 9.8, 0.4, None),
        ("pop", 9.95, 0.45, None), ("pop", 10.6, 0.25, None), ("pop", 11.2, 0.25, None),
        ("sparkle", 12.6, 0.35, None), ("pop", 12.85, 0.45, None), ("click", 13.6, 0.3, None),
    ]),
    "immo-decode-v2-frais-notaire": (20, [3.7, 8.6, 13.5, 17.6], [
        ("impact-bass-1", 0.05, 0.4, None), ("typing", 0.0, 0.18, 0.7), ("pop", 0.65, 0.35, None), ("whoosh-short", 0.75, 0.3, None),
        ("impact-bass-2", 4.0, 0.4, None), ("pop", 4.8, 0.4, None), ("typing", 5.2, 0.22, 1.5), ("ping", 6.6, 0.35, None),
        ("pop", 9.0, 0.4, None), ("click-soft", 9.3, 0.35, None), ("pop", 9.7, 0.4, None), ("click-soft", 9.8, 0.35, None),
        ("pop", 10.1, 0.4, None), ("click-soft", 10.2, 0.35, None), ("ping", 10.6, 0.3, None),
        ("pop", 13.9, 0.45, None), ("pop", 14.5, 0.45, None), ("sparkle", 17.6, 0.35, None), ("pop", 17.85, 0.4, None),
    ]),
    "immo-decode-v2bis-rentabilite": (25, [3.4, 8.2, 12.8, 17.6, 22.3], [
        ("impact-bass-1", 0.05, 0.4, None), ("typing", 0.0, 0.18, 0.7), ("pop", 0.65, 0.35, None), ("whoosh-short", 0.7, 0.3, None),
        ("click-soft", 3.5, 0.35, None), ("pop", 4.2, 0.45, None), ("pop", 4.8, 0.45, None),
        ("pop", 8.6, 0.45, None), ("typing", 9.3, 0.22, 1.2), ("ping", 10.4, 0.35, None),
        ("pop", 13.2, 0.45, None), ("typing", 13.9, 0.2, 1.3), ("impact-bass-2", 15.1, 0.4, None),
        ("click", 18.1, 0.4, None), ("click", 18.45, 0.4, None), ("click", 18.8, 0.4, None), ("impact-bass-1", 19.7, 0.35, None),
        ("sparkle", 22.3, 0.35, None), ("pop", 22.55, 0.4, None),
    ]),
}

START, END = "<!-- sfx-auto:debut -->", "<!-- sfx-auto:fin -->"
JS_START, JS_END = "// sfx-auto:debut", "// sfx-auto:fin"

for proj, (total, wipes, cues) in PLAN.items():
    d = os.path.join(VIDEOS, proj)
    os.makedirs(os.path.join(d, "assets", "sfx"), exist_ok=True)
    for name in {c[0] for c in cues}:
        shutil.copy(os.path.join(HERE, name + ".mp3"), os.path.join(d, "assets", "sfx", name + ".mp3"))
    shutil.copy(os.path.join(HERE, "CREDITS.md"), os.path.join(d, "assets", "sfx", "CREDITS.md"))
    p = os.path.join(d, "index.html")
    s = open(p).read()
    s = re.sub(re.escape(START) + ".*?" + re.escape(END) + r"\n?", "", s, flags=re.S)
    s = re.sub(r"\s*" + re.escape(JS_START) + ".*?" + re.escape(JS_END), "", s, flags=re.S)
    s = s.replace("<style>", "<style>\n      /* sfx-auto */ #grid { inset: -120px !important; } #prog-auto { position: absolute; left: 0; top: 0; width: 1080px; height: 12px; background: #c8553d; transform-origin: 0% 50%; z-index: 30; } .wipe-auto { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; z-index: 40; } #wipeA-auto { background: #c8553d; } #wipeB-auto { background: #1f2a44; }", 1) if "/* sfx-auto */" not in s else s

    # Sons (une piste par son simultané) + volets + barre
    all_cues = list(cues) + [("whoosh-short", round(b - 0.35, 2), 0.5, None) for b in wipes]
    all_cues.sort(key=lambda c: c[1])
    lanes, tags = [], []
    for i, (name, t, vol, mx) in enumerate(all_cues):
        ln = round(min(mx or LEN[name], LEN[name], total - t), 2)
        lane = next((k for k, e in enumerate(lanes) if e <= t + 0.001), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = t + ln
        tags.append(f'      <audio id="sfx-{i + 1}" src="assets/sfx/{name}.mp3" data-start="{t}" data-duration="{ln}" data-volume="{vol}" data-track-index="{3 + lane}"></audio>')
    block = f'{START}\n      <div id="prog-auto"></div>\n      <div class="wipe-auto" id="wipeA-auto"></div>\n      <div class="wipe-auto" id="wipeB-auto"></div>\n' + "\n".join(tags) + f"\n      {END}\n"
    i = s.rfind("<script>")
    j = s.rfind("</div>", 0, i)
    s = s[:j] + block + "    " + s[j:]

    js = [JS_START, 'gsap.set(".wipe-auto", { yPercent: 100 });', f'tl.fromTo("#prog-auto", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {total}, ease: "none" }}, 0);', f'tl.fromTo("#grid", {{ x: 0, y: 0 }}, {{ x: 60, y: -120, duration: {total}, ease: "none" }}, 0);']
    for b in wipes:
        js += [
            f'tl.fromTo("#wipeA-auto", {{ yPercent: 100 }}, {{ yPercent: 0, duration: 0.3, ease: "power3.in", immediateRender: false }}, {round(b - 0.3, 2)});',
            f'tl.fromTo("#wipeA-auto", {{ yPercent: 0 }}, {{ yPercent: -100, duration: 0.3, ease: "power3.out", immediateRender: false }}, {b});',
            f'tl.fromTo("#wipeB-auto", {{ yPercent: 100 }}, {{ yPercent: 0, duration: 0.24, ease: "power3.in", immediateRender: false }}, {round(b - 0.24, 2)});',
            f'tl.fromTo("#wipeB-auto", {{ yPercent: 0 }}, {{ yPercent: -100, duration: 0.3, ease: "power3.out", immediateRender: false }}, {round(b + 0.04, 2)});',
        ]
    js.append(JS_END)
    k = s.find("      window.__timelines = window.__timelines")
    s = s[:k] + "      " + "\n      ".join(js) + "\n" + s[k:]
    open(p, "w").write(s)
    print("✓", proj, len(tags), "sons")
