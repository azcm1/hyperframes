# Replace the spoken product name (original 15.10-18.75 s) with the re-recorded take
# assets/vo/name-fix.mov. Everything else in the voice stays exactly as recorded.
import subprocess
A, B = 15.10, 18.75          # span of the old name in Hu.ad (between two quiet gaps)
NEW_IN, NEW_OUT = 0.35, 2.50  # speech inside the new take
AT = 15.65                    # new name lands as the gift box comes on screen (15.7 s)
RT_IN, RT_OUT = 18.76, 19.12  # room tone from the quiet gap right after, looped under the replaced span
GAIN_DB = -3.5                # level-match to the surrounding sentence
duck = f"volume='if(between(t,{A},{B}),0,1)':eval=frame"
new = (f"atrim={NEW_IN}:{NEW_OUT},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,"
       f"afade=t=out:st={NEW_OUT - NEW_IN - 0.06:.2f}:d=0.06,volume={GAIN_DB}dB,"
       f"aformat=sample_rates=44100:channel_layouts=stereo,adelay={int(AT * 1000)}|{int(AT * 1000)}")
n = int((RT_OUT - RT_IN) * 44100)
tone = (f"[r]atrim={RT_IN}:{RT_OUT},asetpts=PTS-STARTPTS,aloop=loop={int((B - A) / (RT_OUT - RT_IN)) + 1}:size={n},"
        f"atrim=0:{B - A:.2f},afade=t=in:d=0.03,afade=t=out:st={B - A - 0.03:.2f}:d=0.03,adelay={int(A * 1000)}|{int(A * 1000)}")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", "assets/full.mp4", "-i", "assets/vo/name-fix.mov",
                "-filter_complex", f"[0:a]asplit[o][r];[o]{duck}[a0];[1:a]{new}[a1];{tone}[a2];[a0][a1][a2]amix=inputs=3:normalize=0:duration=first[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
                "assets/full2.mp4"], check=True)
print("wrote assets/full2.mp4")
