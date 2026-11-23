# Put the graphics on the presenter's original, untouched edit (assets/full.mp4 = Hu.ad with the
# picture re-encoded for seeking and the audio stream copied as-is).
# Scene times were authored on the trimmed edit (aroll.mp4); S() maps them back to the original.
import json, re
keep = json.load(open("tools/timemap.json"))["keep"]
def S(t):
    acc = 0.0
    for a, b in keep:
        if t <= acc + (b - a) + 1e-9: return round(a + (t - acc), 3)
        acc += b - a
    return round(keep[-1][1], 3)
JS = "const KEEP = " + json.dumps([[round(a, 4), round(b, 4)] for a, b in keep]) + ";\n" + \
"""    const S = (g) => { let acc = 0; for (const [a, b] of KEEP) { if (g <= acc + (b - a) + 1e-9) return a + (g - acc); acc += b - a; } return KEEP[KEEP.length - 1][1]; };"""
END = 92.36
hosts = {"kids": (13.5, 28.8), "d3": (42.3, 22.6), "gt7": (64.9, 14.9), "outro": (79.8, 8.8)}
p = "index.html"; s = open(p, encoding="utf8").read()
s = s.replace('src="assets/aroll2.mp4"', 'src="assets/full.mp4"').replace('data-duration="92.63"', f'data-duration="{END}"')
s = s.replace('data-start="0" data-duration="17.55"', f'data-start="0" data-duration="{S(13.5)}"')
for cid, (o, d) in hosts.items():
    st = S(o); du = round(min(S(o + d), END) - st, 3)
    s = re.sub(rf'(id="{cid}" class="scene"[^>]*?data-start=")[0-9.]+(" data-duration=")[0-9.]+', rf'\g<1>{st}\g<2>{du}', s, flags=re.S)
s = re.sub(r"const END = [0-9.]+;", f"const END = {END};", s)
shots = [0, 4.53, 9.9, 15.7, 18.3, 22.1, 28.3, 32.67, 35.77, 38.47, 40.37, 43.87, 57.47, 63.73, 67.63, 74.2, 79.8, 83.33]
s = re.sub(r"const shots = \[.*?\];", f"const shots = {shots};", s)
s = re.sub(r"const joins = \[.*?\];", "const joins = []; // nothing is cut: each shot just drifts in slowly", s)
# SFX: (aroll time, id, file, dur, vol) -> original timing
sfx = [(None, 3.45, "shutter", "click", 0.36, 0.18), (None, 6.0, "inflate", "whoosh", 0.57, 0.12),
       (10.3, None, "tag1", "pop", 0.72, 0.07), (10.75, None, "tag2", "pop", 0.72, 0.07), (11.2, None, "tag3", "pop", 0.72, 0.07),
       (13.55, None, "ch1", "whoosh", 0.57, 0.12), (21.0, None, "cam", "click", 0.36, 0.15), (22.6, None, "sim", "pop", 0.72, 0.07),
       (25.05, None, "video", "pop", 0.72, 0.07), (31.8, None, "alert", "notification", 1.6, 0.15), (37.65, None, "link", "ping", 1.3, 0.1),
       (43.7, None, "ch2", "whoosh", 0.57, 0.12), (46.2, None, "badge", "ping", 1.3, 0.09), (64.95, None, "ch3", "whoosh", 0.57, 0.12),
       (69.75, None, "sparkle", "sparkle", 1.8, 0.1), (74.2, None, "ready", "ping", 1.3, 0.09), (85.55, None, "end", "chime", 2.54, 0.18)]
i = s.index("      <!-- sound on the visible actions"); j = s.index("    </div>\n\n    <script>")
rows = ["      <!-- sound on the visible actions: kept soft, well under the voice -->"]; tr_end = {}
for ar, src, n, f, d, v in sfx:
    t = src if src is not None else S(ar)
    tr = 3
    while tr_end.get(tr, -1) > t: tr += 1
    tr_end[tr] = t + d
    rows.append(f'      <audio id="sfx-{n}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t}" data-duration="{d}" data-track-index="{tr}" data-volume="{v}"></audio>')
s = s[:i] + "\n".join(rows) + "\n" + s[j:]
open(p, "w", encoding="utf8").write(s)
# scene timelines: authored times go through S()
for cid, (o, d) in hosts.items():
    p = f"compositions/{cid}.html"; c = open(p, encoding="utf8").read()
    old = "const t = (g) => Math.max(0, +(g - O).toFixed(3));"
    assert old in c, p
    c = c.replace(old, JS + "\n    const SO = S(O);\n    const t = (g) => Math.max(0, +(S(g) - SO).toFixed(3));")
    open(p, "w", encoding="utf8").write(c)
print({k: (S(o), round(S(o + d) - S(o), 2)) for k, (o, d) in hosts.items()})
