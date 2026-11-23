# Shorten long pauses in the voiceover edit. Writes the keep-list and a source->edit time map.
import json, subprocess, sys
SRC = "assets/source.mov"
GAPS = [(7.19,7.50),(9.33,9.81),(18.74,19.20),(22.95,23.37),(25.63,25.98),(28.93,29.28),(31.12,31.45),
        (36.47,37.02),(38.91,39.24),(43.74,44.22),(46.45,46.76),(50.53,50.86),(54.54,54.95),(56.68,56.99),
        (59.12,59.51),(61.04,61.58),(65.93,66.28),(69.80,70.16),(72.44,72.82),(74.26,74.60),(77.49,77.84),
        (79.78,80.22),(86.41,86.78),(89.36,89.70)]
KEEP_GAP = {61.04: 0.40}   # breath before the emotional line
END = 92.36
cuts = []
for a, b in GAPS:
    keep = KEEP_GAP.get(a, 0.22)
    if b - a <= keep + 0.06: continue
    pad = keep / 2
    fr = lambda x: round(x * 30) / 30   # snap to frame boundaries so the time map is exact
    cuts.append((fr(a + pad), fr(b - pad)))
keep, t = [], 0.0
for a, b in cuts:
    keep.append((t, a)); t = b
keep.append((t, round(END * 30) / 30))
json.dump({"keep": keep, "cuts": cuts}, open("tools/timemap.json", "w"), indent=1)
saved = sum(b - a for a, b in cuts)
print(f"{len(cuts)} cuts, saved {saved:.2f}s, new length {END - saved:.2f}s")
if "--render" in sys.argv:
    parts, labels = [], []
    for i, (a, b) in enumerate(keep):
        # 8 ms audio fades at every join so cuts never click
        d = b - a
        parts.append(f"[0:v]trim=start_frame={round(a*30)}:end_frame={round(b*30)},setpts=PTS-STARTPTS[v{i}];"
                     f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d-0.008:.3f}:d=0.008[a{i}];")
        labels.append(f"[v{i}][a{i}]")
    fc = "".join(parts) + "".join(labels) + f"concat=n={len(keep)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", SRC, "-filter_complex", fc,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                    "-pix_fmt", "yuv420p", "-r", "30", "-g", "30", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", "assets/aroll.mp4"], check=True)
