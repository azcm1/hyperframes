# Align the script (tools/phrases.txt) to the voiceover by energy pauses + anchors.
import wave, math, array, re, json, sys
wav, out = sys.argv[1], sys.argv[2]
w = wave.open(wav); a = array.array('h', w.readframes(w.getnframes()))
hop = 160; db = []
for i in range(0, len(a) - hop, hop):
    s = sum(x * x for x in a[i:i + hop]) / hop; db.append(10 * math.log10(s + 1e-9) - 90.3)
TH = -36
cands = []; st = None
for i, v in enumerate(db + [0]):
    if v < TH:
        if st is None: st = i
    else:
        if st is not None and i - st >= 6: cands.append((st / 100, i / 100))
        st = None
ph = [l.strip() for l in open("tools/phrases.txt", encoding="utf8") if l.strip()]
# anchors: phrase text -> the pause that precedes it ends near this time (from the shot cuts)
ANCH = {"نبدأ بهدية الصغار:": 13.86, "فيها كاميرا تنفصل،": 19.16, "وفيها شريحة اتصال": 23.37,
        "أما اللي تنتفخ،": 44.22, "أحيانًا أحلى طريقة تقول فيها": 61.58, "وأنت؟ تستاهل هدية بعد": 67.69,
        "تعطيك مؤشر الجاهزية البدنية": 74.60, "وفيها تطبيقات كثير": 80.22, "للأطفال، للوالدين،": 84.03}
ANCH = {k: v for k, v in ANCH.items() if v}
def syl(p):
    lat = sum(len(x) for x in re.findall(r"[A-Za-z0-9]+", p))
    return len(re.findall(r"[ء-ي]", p)) + lat * 1.25
VC = [0]
for v in db: VC.append(VC[-1] + (1 if v >= TH else 0))
vb = lambda t0, t1: (VC[int(t1 * 100)] - VC[int(t0 * 100)]) / 100
s0, s1 = 0.17, 91.21
pts = [(s0, s0)] + cands + [(s1, s1)]
P, N = len(pts), len(ph)
# local rate per anchored section
bounds_idx = {}
for k, p in enumerate(ph):
    if p in ANCH:
        bounds_idx[k] = min(range(P), key=lambda j: abs(pts[j][1] - ANCH[p]))
punct = [1.0 if re.search(r"[…!؟?:،.]$", p) else 0.4 for p in ph]
INF = 1e18
dp = [[INF] * P for _ in range(N + 1)]; bk = [[-1] * P for _ in range(N + 1)]
dp[0][0] = 0
# section rates
secs = sorted(bounds_idx.items()); edges = [(0, 0)] + secs + [(N, P - 1)]
rate_of = {}
for (k0, j0), (k1, j1) in zip(edges, edges[1:]):
    r = vb(pts[j0][1], pts[j1][0]) / max(1, sum(syl(p) for p in ph[k0:k1]))
    for k in range(k0, k1): rate_of[k] = r
for k in range(1, N + 1):
    for j in range(1, P):
        if (k < N and j == P - 1) or (k == N and j != P - 1): continue
        if k in bounds_idx and j != bounds_idx[k]: continue  # phrase k (0-based) starts after point j
        best, bi = INF, -1
        for i in range(j):
            if dp[k - 1][i] >= INF: continue
            exp = syl(ph[k - 1]) * rate_of[k - 1]; got = vb(pts[i][1], pts[j][0])
            c = ((got - exp) / max(exp, 0.4)) ** 2
            if k < N: c -= 0.8 * punct[k - 1] * min(pts[j][1] - pts[j][0], 0.5)
            if dp[k - 1][i] + c < best: best, bi = dp[k - 1][i] + c, i
        dp[k][j], bk[k][j] = best, bi
j = P - 1; b = []
for k in range(N, 0, -1):
    i = bk[k][j]; b.append((pts[i][1], pts[j][0])); j = i
b.reverse()
res = [{"text": p, "start": round(x, 2), "end": round(y, 2)} for p, (x, y) in zip(ph, b)]
json.dump(res, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=1)
for o in res: print(f"{o['start']:6.2f} {o['end']:6.2f}  {o['text']}")
