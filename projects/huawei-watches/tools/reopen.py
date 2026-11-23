# Re-cut the opening so each shot carries its own line:
#   shot 1 (kids watch, full length)  -> «هذي الساعة تصوّر…»
#   shot 2 (D3, to 8.4 s)             -> «وهذي الساعة تنتفخ!» landing as the airbag opens (~6.2 s)
#   shot 3 (three watches flat-lay)   -> «محتار وش تهدي…» … «فيه هدية لكل واحد في العيلة»
# The voice is moved under the pictures, and the flat-lay + gift-box shots are slowed with
# motion interpolation to cover the extra 4.05 s. Everything from the box shot on keeps sync (+4.05 s).
# Input: assets/aroll.mp4 (from tools/trim.py). Output: assets/aroll2.mp4
import subprocess

SRC = "assets/aroll.mp4"
OUT = "assets/aroll2.mp4"
SHIFT = 4.05
FPS = 30
fr = lambda t: round(t * FPS)

# video: (aroll start, aroll end, output length or None for 1x)
V = [
    (0.0, 4.5333, None),               # kids watch takes a picture
    (4.5333, 8.4, None),               # D3 measures, then the airbag
    (9.5333, 15.3333, 17.55 - 8.4),    # flat-lay, 0.634x
    (15.3333, 17.9333, 17.9333 + SHIFT - 17.55),  # gift box, 0.587x
    (17.9333, None, None),             # rest of the film, in sync
]
# audio: (aroll start, aroll end, output start)
A = [
    (0.0, 2.65, 0.0),       # هذي الساعة تصوّر
    (2.70, 4.49, 4.95),     # وهذي الساعة تنتفخ
    (4.49, 7.27, 8.47),     # محتار وش تهدي اللي تحبهم؟
    (7.27, None, 7.27 + SHIFT),  # تعالوا نشوف… onward
]

f = []
vl = []
for i, (a, b, out_len) in enumerate(V):
    end = f":end_frame={fr(b)}" if b is not None else ""
    chain = f"[0:v]trim=start_frame={fr(a)}{end},setpts=PTS-STARTPTS"
    if out_len:
        factor = out_len / (b - a)
        chain += f",setpts={factor:.6f}*PTS,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
        chain += f",trim=end_frame={fr(out_len)}"
    f.append(chain + f",fps={FPS}[v{i}]")
    vl.append(f"[v{i}]")
f.append("".join(vl) + f"concat=n={len(V)}:v=1:a=0[v]")

al, cursor = [], 0.0
for i, (a, b, at) in enumerate(A):
    if at - cursor > 0.001:
        f.append(f"anullsrc=r=44100:cl=stereo,atrim=duration={at - cursor:.4f}[s{i}]")
        al.append(f"[s{i}]")
    end = f":end={b}" if b is not None else ""
    f.append(f"[0:a]atrim=start={a}{end},asetpts=PTS-STARTPTS,afade=t=in:d=0.006,aformat=sample_rates=44100:channel_layouts=stereo[a{i}]")
    al.append(f"[a{i}]")
    if b is not None:
        cursor = at + (b - a)
f.append("".join(al) + f"concat=n={len(al)}:v=0:a=1[a]")

subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", SRC, "-filter_complex", ";".join(f),
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
                "-r", str(FPS), "-g", str(FPS), "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
print("wrote", OUT)
