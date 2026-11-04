# Synthesised music bed + SFX + voice-over mix for the BUT / ÉCHO film. Deterministic (seeded).
import numpy as np, soundfile as sf, os
SR = 48000; D = 152.2; N = int(SR * D)
rng = np.random.default_rng(7)
here = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(here, "..", "audio")
t_all = np.arange(N) / SR
BPM = 120; BEAT = 60 / BPM
def note(m): return 440 * 2 ** ((m - 69) / 12)
def env(n, a=0.005, r=0.2):
    e = np.ones(n); ai = max(1, int(a * SR)); e[:ai] = np.linspace(0, 1, ai)
    e *= np.exp(-np.arange(n) / (r * SR)); return e
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if i < N and j > i: buf[i:j] += g * x[: j - i]
def lp(x, a):  # one-pole lowpass
    y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc += a * (x[i] - acc); y[i] = acc
    return y
def saw(f, n, det=0.0):
    t = np.arange(n) / SR; return 2 * ((t * f * (1 + det)) % 1) - 1

# ---- drums
kick_n = int(0.35 * SR); tk = np.arange(kick_n) / SR
kick = np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-tk * 28)) / SR) * np.exp(-tk * 9)
kick += 0.3 * np.sin(2 * np.pi * 180 * tk) * np.exp(-tk * 60)
hat = rng.standard_normal(int(0.06 * SR)); hat = np.diff(hat, prepend=0) * env(len(hat), 0.001, 0.015)
clap = rng.standard_normal(int(0.25 * SR)); clap = (clap - lp(clap, 0.12)) * env(len(clap), 0.002, 0.07)
# chords Am F C G  (bar = 4 beats = 2 s)
prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]
mus = np.zeros(N); pad = np.zeros(N); arp = np.zeros(N); bass = np.zeros(N); drm = np.zeros(N)
def sect(t):  # energy level per section
    if t < 13.43: return 1
    if t < 15.11: return 3
    if t < 140.43: return 2 if t < 68.64 else 3
    if t < 147.75: return 0
    return -1
nb = int(D / BEAT)
for b in range(nb):
    t = b * BEAT; lvl = sect(t); bar = int(t // 2) % 4; root, ch = prog[bar]
    if lvl <= -1: continue
    # pad per bar
    if b % 4 == 0:
        n = int(2.05 * SR); x = sum(saw(note(m), n, d) for m in ch for d in (-0.003, 0.003))
        x = lp(x, 0.05) * np.minimum(1, np.arange(n) / (0.3 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.3 * SR))
        add(pad, x, t, 0.05)
    if lvl >= 1:
        add(drm, kick, t, 0.9 if lvl >= 2 else 0.6)
        add(drm, hat, t + BEAT / 2, 0.18)
    if lvl >= 2 and b % 2 == 1: add(drm, clap, t, 0.35)
    if lvl >= 3: add(drm, hat, t + BEAT / 4, 0.08); add(drm, hat, t + 3 * BEAT / 4, 0.08)
    if lvl >= 1:  # bass 8ths
        for k in range(2):
            n = int(BEAT / 2 * SR * 0.9); x = lp(saw(note(root - 12), n), 0.08) * env(n, 0.004, 0.18)
            add(bass, x, t + k * BEAT / 2, 0.35 if lvl >= 2 else 0.22)
    if lvl >= 2 or (lvl == 1 and t > 2):  # pluck arp 16ths
        seq = ch + [ch[1] + 12]
        for k in range(4):
            m = seq[(b * 4 + k) % 4] + 12; n = int(0.22 * SR); tt = np.arange(n) / SR
            x = (np.sin(2 * np.pi * note(m) * tt) + 0.3 * np.sin(4 * np.pi * note(m) * tt)) * env(n, 0.002, 0.07)
            add(arp, x, t + k * BEAT / 4, 0.07)
# breakdown pad for outro already via pad; final chord + hit
n = int(3.3 * SR); x = sum(saw(note(m), n, d) for m in [57, 60, 64, 69] for d in (-0.004, 0.004))
x = lp(x, 0.06) * env(n, 0.01, 1.4); add(pad, x, 147.75, 0.09)
add(drm, kick, 147.75, 1.0)
mus = pad + arp + bass + drm
# riser into title slam (13.43) and outro hit
def riser(dur):
    n = int(dur * SR); w = rng.standard_normal(n); a = np.linspace(0.01, 0.5, n) ** 2
    y = np.empty(n); acc = 0.0
    for i in range(n): acc += a[i] * (w[i] - acc); y[i] = acc
    return y * np.linspace(0, 1, n) ** 2
add(mus, riser(1.6), 13.43 - 1.6, 0.5); add(mus, riser(1.4), 147.75 - 1.4, 0.4)

# ---- SFX
def whoosh(dur=0.55, up=True):
    n = int(dur * SR); w = rng.standard_normal(n); x = np.linspace(0, 1, n)
    a = (0.02 + 0.35 * (x if up else 1 - x)) ** 2 * 1.0
    y = np.empty(n); acc = 0.0
    for i in range(n): acc += a[i] * (w[i] - acc); y[i] = acc
    return y * np.sin(np.pi * x) ** 1.5
def boom():
    n = int(0.8 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(38 + 80 * np.exp(-tt * 12)) / SR) * np.exp(-tt * 4.5) + 0.25 * rng.standard_normal(n) * np.exp(-tt * 30)
def pop(f=900):
    n = int(0.09 * SR); tt = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.5 * np.exp(-tt * 60))) / SR) * np.exp(-tt * 40)
def tick():
    n = int(0.03 * SR); tt = np.arange(n) / SR; return np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 200)
def ding(f=1320):
    n = int(0.9 * SR); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * f * 2.01 * tt)) * np.exp(-tt * 5)
sfx = np.zeros(N)
cuts = [7.6, 13.43, 15.11, 20.26, 27.6, 32.93, 43.2, 48.19, 55.45, 68.64, 73.97, 86.35, 95.52, 106.24, 115.42, 122.89, 132.69, 140.43]
for c in cuts: add(sfx, whoosh(), c - 0.32, 0.55)
for t in [13.56, 13.93, 14.31, 45.37, 49.88, 68.71, 113.54, 147.75]: add(sfx, boom(), t, 0.7)
add(sfx, boom(), 0.05, 0.8)
for t in [2.3, 5.09, 6.24, 8.8, 16.1, 18.54, 20.54, 22.56, 24.71, 33.52, 36.49, 38.31, 40.12, 41.33, 58.42, 59.33, 60.25, 61.08, 62.6, 62.98, 63.36, 63.74, 65.03, 72.95, 76.04, 77.23, 78.89, 81.5, 68, 88.09, 89, 92.32, 76, 93.12, 93.46,
          81, 99.37, 100.44, 101.51, 109.29, 110.25, 111.26, 112.28, 117.35, 119.52, 121.08, 123.98, 126.78, 129.22, 134.18, 136.76, 137.8, 138.18, 148.01]:
    add(sfx, pop(700 + (int(t * 10) % 5) * 120), t, 0.35)
for i in range(14): add(sfx, tick(), 0.15 + i / 14 * 1.2, 0.25)
for v in range(31): add(sfx, tick(), 49.93 + v / 31 * 1.0, 0.2)
for k in range(20): add(sfx, tick(), 136.89 + k / 20 * 1.1, 0.18)
for t in [1.35, 84.35, 94, 148.54]: add(sfx, ding(1320 if t < 90 else 990), t, 0.18)

# ---- voice
import json
T = json.load(open(os.path.join(A, "voix-el", "timing.json")))
vox = np.zeros(N)
for nm, st in zip(T["order"], T["start"]):
    x, sr = sf.read(os.path.join(A, "voix-el", nm + ".wav"))
    if x.ndim > 1: x = x.mean(1)
    add(vox, np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x), st)
vox *= 0.9 / (np.abs(vox).max() + 1e-9)
# sidechain duck from voice envelope
e = np.abs(vox); w = int(0.25 * SR); e = np.convolve(e, np.ones(w) / w, mode="same"); e = np.minimum(1, e / 0.05)
duck = 1 - 0.55 * e
mus_n = mus / (np.abs(mus).max() + 1e-9)
fade = np.ones(N); fi = int(150.9 * SR); fade[fi:] = np.linspace(1, 0, N - fi)
music = mus_n * 0.55 * duck * fade; music_nv = mus_n * 0.7 * fade
sfx_n = sfx / (np.abs(sfx).max() + 1e-9) * 0.5
def norm(x, pk=0.95): return x * (pk / (np.abs(x).max() + 1e-9))
def soft(x): return np.tanh(x * 1.2) / np.tanh(1.2)
mix = norm(soft(vox * 1.0 + music + sfx_n))
mix_nv = norm(soft(music_nv + sfx_n))
for name, x in [("voix", vox), ("musique", music_nv), ("sfx", sfx_n), ("mix", mix), ("mix-sans-voix", mix_nv)]:
    sf.write(os.path.join(A, name + ".wav"), np.stack([x, x], 1).astype(np.float32), SR, subtype="PCM_16")
print("ok")
