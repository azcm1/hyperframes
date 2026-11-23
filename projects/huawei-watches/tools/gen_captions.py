# Build compositions/captions.html from assets/transcript.json (script text aligned to the VO).
import json, html
P = json.load(open("assets/transcript.json", encoding="utf8"))
# lines that a big headline / chapter card / quote already writes on screen
DROP = {0, 1, 2, 3, 4, 5, 6, 14, 23, 28, 29, 15, 20, 21, 22, 30, 31, 32, 33, 34, 35, 41, 42, 43}
groups = []
for i, p in enumerate(P):
    if i in DROP: continue
    ws = p["words"]
    n = len(ws)
    k = 1 if n <= 4 else 2 if n <= 8 else 3
    size = -(-n // k)
    for j in range(0, n, size):
        groups.append(ws[j:j + size])
rows, js = [], []
for gi, g in enumerate(groups):
    s = round(g[0]["s"] - 0.06, 2)
    nxt = groups[gi + 1][0]["s"] - 0.06 if gi + 1 < len(groups) else 999
    e = round(min(g[-1]["e"] + 0.25, nxt), 2)
    spans = " ".join(f'<span id="cw{gi}-{wi}" class="cw">{html.escape(w["w"])}</span>' for wi, w in enumerate(g))
    rows.append(f'    <div id="cg{gi}" class="cg"><span class="cp">{spans}</span></div>')
    js.append(f'    G("#cg{gi}", {s}, {e}, [{", ".join(str(round(w["s"], 2)) for w in g)}]);')
out = f'''<template>
  <style>
    @font-face {{ font-family: "Tajawal"; src: url("assets/fonts/Tajawal-ExtraBold.ttf"); font-weight: 800; }}
    #root {{ position: absolute; inset: 0; direction: rtl; font-family: "Tajawal", sans-serif; }}
    .cg {{ position: absolute; left: 0; right: 0; top: 1110px; text-align: center; opacity: 0; }}
    .cp {{
      display: inline-block; max-width: 800px; padding: 14px 30px 18px; border-radius: 22px;
      background: rgba(10, 10, 14, 0.62); font-weight: 800; font-size: 50px; line-height: 1.3; color: rgba(255, 255, 255, 0.72);
    }}
    .cw {{ display: inline-block; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(rows)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // a group fades in, each word lights up white as it is spoken, then a hard kill at the end
    const G = (sel, s, e, words) => {{
      tl.fromTo(sel, {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.14, ease: "power2.out" }}, s);
      words.forEach((w, i) => {{
        tl.fromTo(`${{sel}} .cw:nth-child(${{i + 1}})`, {{ color: "rgba(255,255,255,0.72)", scale: 1 }},
          {{ color: "#ffffff", scale: 1.06, duration: 0.12, ease: "power2.out" }}, w);
        tl.to(`${{sel}} .cw:nth-child(${{i + 1}})`, {{ scale: 1, duration: 0.15 }}, w + 0.12);
      }});
      tl.to(sel, {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, e - 0.1);
      tl.set(sel, {{ opacity: 0, visibility: "hidden" }}, e);
    }};
{chr(10).join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open("compositions/captions.html", "w", encoding="utf8").write(out)
print(len(groups), "caption groups")
