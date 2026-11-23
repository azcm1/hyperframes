# Map aligned phrase times (source timeline) onto the trimmed edit; split into words with estimated times.
import json, re
tm = json.load(open("tools/timemap.json"))
def m(t):
    acc = 0.0
    for a, b in tm["keep"]:
        if t < a: return round(acc, 3)          # inside a removed gap: snap to the join
        if t <= b: return round(acc + t - a, 3)
        acc += b - a
    return round(acc, 3)
ph = json.load(open("tools/align_raw.json", encoding="utf8"))
# merge the two tiny closing chunks into one caption line
out = []
for p in ph:
    if out and out[-1]["text"].startswith("للأطفال") and p["text"].startswith("للشريك"):
        out[-1]["text"] += " " + p["text"]; out[-1]["end"] = p["end"]; continue
    out.append(dict(p))
for p in out:
    p["start"], p["end"] = m(p["start"]), m(p["end"])
    ws = p["text"].split()
    wt = [max(1, len(re.sub(r"[^\w]", "", w))) for w in ws]
    tot = sum(wt); t = p["start"]; p["words"] = []
    for w, k in zip(ws, wt):
        d = (p["end"] - p["start"]) * k / tot
        p["words"].append({"w": w, "s": round(t, 2), "e": round(t + d, 2)}); t += d
json.dump(out, open("assets/transcript.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
for i, p in enumerate(out): print(f"{i:2d} {p['start']:6.2f} {p['end']:6.2f}  {p['text']}")
