# Synthesised music bed + SFX + voice-over mix for the BUT / ÉCHO film. Deterministic (seeded).
import numpy as np, soundfile as sf, os
SR = 48000; D = 95.5; N = int(SR * D)
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
    if t < 10.7: return 1
    if t < 12.7: return 3
    if t < 87.8: return 2 if t < 26.6 else 3
    if t < 92.2: return 0
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
x = lp(x, 0.06) * env(n, 0.01, 1.4); add(pad, x, 92.2, 0.09)
add(drm, kick, 92.2, 1.0)
mus = pad + arp + bass + drm
# riser into title slam (10.7) and outro hit
def riser(dur):
    n = int(dur * SR); w = rng.standard_normal(n); a = np.linspace(0.01, 0.5, n) ** 2
    y = np.empty(n); acc = 0.0
    for i in range(n): acc += a[i] * (w[i] - acc); y[i] = acc
    return y * np.linspace(0, 1, n) ** 2
add(mus, riser(1.6), 10.7 - 1.6, 0.5); add(mus, riser(1.4), 92.2 - 1.4, 0.4)

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
cuts = [6.6, 10.7, 12.7, 16.3, 22.7, 26.6, 29.8, 40.5, 48.9, 57.8, 65.9, 72.5, 81.1, 87.8]
for c in cuts: add(sfx, whoosh(), c - 0.32, 0.55)
for t in [10.85, 11.3, 11.75, 26.7, 64.1, 92.2]: add(sfx, boom(), t, 0.7)
add(sfx, boom(), 0.05, 0.8)
for t in [2.0, 4.3, 5.25, 7.5, 13.4, 15.0, 16.6, 18.3, 20.1, 29.1, 31.6, 32.6, 34.0, 36.2, 38.3, 42.2, 43.0, 45.9, 46.3, 46.6, 46.9,
          51.3, 52.15, 53.0, 53.85, 60.55, 61.35, 62.2, 63.05, 67.65, 69.45, 70.75, 73.55, 75.9, 77.95, 82.4, 84.4, 85.2, 85.5, 92.5]:
    add(sfx, pop(700 + (int(t * 10) % 5) * 120), t, 0.35)
for i in range(14): add(sfx, tick(), 0.15 + i / 14 * 1.2, 0.25)
for k in range(20): add(sfx, tick(), 84.5 + k / 20 * 1.1, 0.18)
for t in [1.35, 38.6, 64.3, 93.1]: add(sfx, ding(1320 if t < 90 else 990), t, 0.18)

# ---- voice
starts = [0.6, 6.7, 12.8, 16.4, 23.0, 26.9, 29.9, 40.8, 49.2, 58.1, 66.1, 72.7, 81.3, 88.0]
vox = np.zeros(N)
for i, st in enumerate(starts):
    x, sr = sf.read(os.path.join(A, "voix", f"l{i+1:02d}.wav"))
    if x.ndim > 1: x = x.mean(1)
    xi = np.interp(np.arange(int(len(x) * SR / sr)) * sr / SR, np.arange(len(x)), x)  # resample 24k→48k
    add(vox, xi, st)
vox *= 0.9 / (np.abs(vox).max() + 1e-9)
# sidechain duck from voice envelope
e = np.abs(vox); w = int(0.25 * SR); e = np.convolve(e, np.ones(w) / w, mode="same"); e = np.minimum(1, e / 0.05)
duck = 1 - 0.55 * e
mus_n = mus / (np.abs(mus).max() + 1e-9)
fade = np.ones(N); fi = int(94.0 * SR); fade[fi:] = np.linspace(1, 0, N - fi)
music = mus_n * 0.55 * duck * fade; music_nv = mus_n * 0.7 * fade
sfx_n = sfx / (np.abs(sfx).max() + 1e-9) * 0.5
def norm(x, pk=0.95): return x * (pk / (np.abs(x).max() + 1e-9))
def soft(x): return np.tanh(x * 1.2) / np.tanh(1.2)
mix = norm(soft(vox * 1.0 + music + sfx_n))
mix_nv = norm(soft(music_nv + sfx_n))
for name, x in [("voix", vox), ("musique", music_nv), ("sfx", sfx_n), ("mix", mix), ("mix-sans-voix", mix_nv)]:
    sf.write(os.path.join(A, name + ".wav"), np.stack([x, x], 1).astype(np.float32), SR, subtype="PCM_16")
print("ok")
