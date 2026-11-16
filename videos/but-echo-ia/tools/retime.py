# Retime the whole film onto the ElevenLabs voice-over durations (piecewise-linear time warp).
import re, json
order = ["l01","l02","l03","l04","l05","a1","a2","a3","a4","l06","l07","l08","l09","l10","l11","l12","l13","l14"]
old_start = [0.6,6.7,12.8,16.4,23.0,26.9,36.6,40.0,47.3,56.6,59.6,70.5,78.9,87.8,95.8,102.4,111.0,117.7]
old_dur = [5.67,3.95,3.26,6.04,3.22,8.87,2.99,6.81,8.38,2.69,10.24,7.77,8.32,7.49,6.04,8.06,5.08,4.16]
new_dur = [6.88,5.76,4.96,7.2,5.04,9.76,4.72,7.2,12.72,5.04,12.16,8.88,10.48,8.96,7.28,9.6,6.56,7.12]
OLD_D = 125.2
new_start = [0.6]
for i in range(1, len(order)):
    gap = old_start[i] - (old_start[i-1] + old_dur[i-1])
    new_start.append(round(new_start[-1] + new_dur[i-1] + max(0.15, gap - 0.35), 2))
tail = OLD_D - (old_start[-1] + old_dur[-1])
NEW_D = round(new_start[-1] + new_dur[-1] + max(2.6, tail - 0.4), 2)
A = [(0.0, 0.0)]
for i in range(len(order)):
    A += [(old_start[i], new_start[i]), (old_start[i] + old_dur[i], new_start[i] + new_dur[i])]
A.append((OLD_D, NEW_D))
def W(t):
    for (a0, b0), (a1, b1) in zip(A, A[1:]):
        if a0 <= t <= a1: return b0 + (t - a0) * (b1 - b0) / (a1 - a0)
    return t
def warp_txt(txt, lo=6.0):
    return re.sub(r'(?<![\d.\w])(\d{1,3}\.\d+)(?![\d.])', lambda m: (f"{round(W(float(m.group(1))),2):g}" if lo <= float(m.group(1)) <= OLD_D + 0.01 else m.group(1)), txt)
# index.html: script part only, plus duration attribute
p = "index.html"; s = open(p).read()
i = s.index("<script>\n      const D")
s = s[:i] + warp_txt(s[i:])
s = s.replace(f'data-duration="{OLD_D:g}"', f'data-duration="{NEW_D:g}"').replace(f"const D = {NEW_D:g};", f"const D = {NEW_D:g};")
# S1 positions inside the first line (below 6 s)
for a in ["1.35", "1.75", "2.0", "2.4", "4.3", "5.25"]:
    s = s.replace(f"}}, {a});", f"}}, {round(W(float(a)),2):g});").replace(f'", {a}, {{', f'", {round(W(float(a)),2):g}, {{')
open(p, "w").write(s)
# audio.py
p = "tools/audio.py"; s = open(p).read()
s = warp_txt(s)
s = s.replace("for t in [2.0, 4.3, 5.25,", "for t in [" + ", ".join(f"{round(W(x),2):g}" for x in (2.0, 4.3, 5.25)) + ",")
open(p, "w").write(s)
json.dump({"order": order, "start": new_start, "dur": new_dur, "D": NEW_D}, open("audio/voix-el/timing.json", "w"), indent=1)
print("D", NEW_D); print(list(zip(order, new_start)))
