"""Generate compositions/captions.html for the GTA-6 controller unboxing.

Word timings come from assets/transcript.json (whisper medium, ar); display text is
corrected by hand (spelling, merged "GTA 6", "بأسعار فلكية" confirmed with large-v3).
"""
import json, sys, html

proj = sys.argv[1]
words = json.load(open(f"{proj}/assets/transcript.json"))
words = words if isinstance(words, list) else words["words"]
T = lambda i: (words[i]["start"], words[i]["end"])
span = lambda a, b: (words[a]["start"], words[b]["end"])

def w(i, text=None, emph=False, j=None):
    s, e = span(i, j) if j is not None else T(i)
    return {"t": text or words[i]["text"], "s": s, "e": e, "x": emph}

# groups of 2-3 words (high energy), broken at sentence ends / pauses
G = [
    [w(0), w(1), w(2)],
    [w(3), w(4, "GTA 6", True, 6)],
    [w(7), w(8), w(9, "مع بعض", False, 10)],
    [w(11), w(12), w(13, "حاطين")],
    [w(14), w(15), w(16, emph=True)],
    [w(17)],
    [w(18), w(19), w(20), w(21)],
    [w(22), w(23, "هذي")],
    [w(24), w(25), w(26, "الآن")],
    [w(27, "بأسعار", False, 28), w(29, "فلكية", True)],
    [w(30), w(31, "أدري"), w(32)],
    [w(33, "وفيه"), w(34), w(35)],
    [w(36), w(37, "هذي"), w(38)],
    [w(39), w(40, "إضافات"), w(41, "وأشياء")],
    [w(42), w(43), w(44)],
    [w(45), w(46), w(47)],
    [w(48, "حقيقي؟", True)],
    [w(49), w(50)],
    [w(51), w(52)],
    [w(53), w(54)],
    [w(55), w(56)],
    [w(57), w(58), w(59)],
    [w(60), w(61)],
    [w(62), w(63)],
    [w(64), w(65), w(66, "انتو"), w(67)],
    [w(68, emph=True)],
    [w(69), w(70), w(71)],
    [w(72, "طبعًا"), w(73, "اخترت")],
    [w(74), w(75, "الأسود", True)],
    [w(76, "لأن"), w(77)],
    [w(78, "أحسه"), w(79), w(80, emph=True)],
    [w(81), w(82), w(83, "شاء الله", False, 84)],
    [w(85), w(86)],
    [w(87), w(88), w(89)],
    [w(90)],
    [w(91, "Grand", True), w(92, "Theft", True), w(93, "Auto", True)],
    [w(94, "والآن"), w(95), w(96)],
    [w(97)],
    [w(98, "الآن"), w(99), w(100)],
    [w(101), w(102)],
    [w(103), w(104), w(105, "أتوقع")],
    [w(106), w(107, "أي"), w(108)],
    [w(109, "إضافي"), w(110)],
    [w(111), w(112, "اكتبوا"), w(113)],
    [w(114, emph=True)],
    [w(115, "واش"), w(116, "رأيكم"), w(117)],
]

DUR = 56.08
groups = []
for gi, g in enumerate(G):
    s = max(0.1, g[0]["s"] - 0.08)
    e = g[-1]["e"] + 0.12
    groups.append({"id": f"cg{gi}", "s": round(s, 3), "e": round(e, 3), "w": g})
# no overlap: each group closes before the next opens
for a, b in zip(groups, groups[1:]):
    if a["e"] > b["s"] - 0.02:
        a["e"] = round(b["s"] - 0.02, 3)
    # hold through short pauses so the line doesn't blink
    elif b["s"] - a["e"] < 0.35:
        a["e"] = round(b["s"] - 0.02, 3)
groups[-1]["e"] = round(min(groups[-1]["e"] + 0.2, DUR - 0.02), 3)

def word_html(gid, k, wd):
    ltr = wd["t"].isascii()
    cls = "cw" + (" emph" if wd["x"] else "") + (" ltr" if ltr else "")
    t = html.escape(wd["t"])
    return (f'<span id="{gid}-w{k}" class="{cls}"><span class="st" aria-hidden="true" data-layout-ignore>{t}</span>'
            f'<span class="fx">{t}</span></span>')

rows = []
for g in groups:
    ws = " ".join(word_html(g["id"], k, wd) for k, wd in enumerate(g["w"]))
    allltr = all(wd["t"].isascii() for wd in g["w"])
    rows.append(
        f'      <div id="{g["id"]}" class="clip cgroup" data-start="{g["s"]}" '
        f'data-duration="{round(g["e"] - g["s"], 3)}" data-track-index="0">'
        f'<div class="cin" dir="{"ltr" if allltr else "rtl"}">{ws}</div></div>'
    )

timing = [{"id": g["id"], "s": g["s"], "e": g["e"],
           "w": [[round(wd["s"], 3), round(wd["e"], 3), wd["x"]] for wd in g["w"]]}
          for g in groups]

PALM_T = open(sys.argv[2]).read()
PALM = lambda pid: PALM_T.replace("PALMID", pid)

out = f"""<template>
  <style>
    @font-face {{
      font-family: "Lalezar";
      src: url("assets/fonts/Lalezar-Regular.ttf") format("truetype");
      font-display: block;
    }}
    #root {{
      position: absolute;
      inset: 0;
      overflow: visible;
      pointer-events: none;
    }}
    .cgroup {{
      position: absolute;
      left: 0;
      right: 0;
      top: 1100px;
      height: 170px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: visible;
    }}
    .cin {{
      display: flex;
      flex-wrap: nowrap;
      justify-content: center;
      align-items: center;
      gap: 0 22px;
      font-family: "Lalezar", sans-serif;
      font-size: 96px;
      line-height: 1.25;
      white-space: nowrap;
      filter: drop-shadow(0 9px 0 #ff3d8b) drop-shadow(0 16px 18px rgba(30, 4, 50, 0.55));
      will-change: transform;
    }}
    .cw {{
      position: relative;
      display: inline-block;
      transform-origin: 50% 70%;
    }}
    .cw.ltr {{
      font-family: "Archivo Black", sans-serif;
      font-size: 0.66em;
      margin: 0 6px;
      letter-spacing: 0.01em;
    }}
    .cw .st {{
      color: #2a0b4a;
      -webkit-text-stroke: 16px #2a0b4a;
      paint-order: stroke fill;
    }}
    .cw .fx {{
      position: absolute;
      inset: 0;
      color: #fff7ef;
      background-image: linear-gradient(180deg, #ffe08a 0%, #ffa24c 38%, #ff4f9a 72%, #c64bff 100%);
      -webkit-background-clip: text;
      background-clip: text;
    }}
    .palm {{
      position: absolute;
      top: 1022px;
      width: 150px;
      height: 260px;
      overflow: visible;
      transform-origin: 50% 100%;
    }}
    #cap-palm-r {{ right: 4px; }}
    #cap-palm-l {{ left: 4px; }}
    #cap-palm-l svg {{ transform: scaleX(-1); }}
    .palm svg {{ width: 100%; height: 100%; overflow: visible; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
    <div id="cap-palm-l" class="clip palm" data-start="0.1" data-duration="55.9" data-track-index="1"><div class="pin">{PALM("cpl")}</div></div>
    <div id="cap-palm-r" class="clip palm" data-start="0.1" data-duration="55.9" data-track-index="1"><div class="pin">{PALM("cpr")}</div></div>
{chr(10).join(rows)}
  </div>
  <script>
    (function () {{
      const G = {json.dumps(timing, ensure_ascii=False)};
      const tl = gsap.timeline({{ paused: true }});
      const fit = window.__hyperframes && window.__hyperframes.fitTextFontSize;
      const palms = ["#cap-palm-l .pin", "#cap-palm-r .pin"];
      tl.fromTo(palms, {{ scale: 0, rotation: -20 }}, {{ scale: 1, rotation: 0, duration: 0.5, ease: "back.out(2)", stagger: 0.06 }}, 0.1);
      G.forEach(function (g, gi) {{
        const el = document.querySelector("#" + g.id + " .cin");
        const text = el.textContent.replace(/\\s+/g, " ").trim();
        const n = text.length;
        let size = n <= 10 ? 116 : n <= 14 ? 106 : n <= 18 ? 94 : 82;
        el.style.fontSize = size + "px";
        // entrance: punch up from below, alternate tilt for rhythm
        const tilt = gi % 2 ? 4 : -4;
        tl.fromTo(el, {{ scale: 0.55, y: 40, rotation: tilt, opacity: 0 }},
          {{ scale: 1, y: 0, rotation: 0, opacity: 1, duration: 0.2, ease: "back.out(2.4)" }}, g.s);
        if (gi > 0) tl.fromTo(palms, {{ rotation: 0 }}, {{ immediateRender: false, rotation: gi % 2 ? 7 : -7, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }}, g.s);
        g.w.forEach(function (wd, k) {{
          const word = "#" + g.id + "-w" + k;
          const fx = word + " .fx";
          tl.set(fx, {{ webkitTextFillColor: "#fff7ef" }}, g.s);
          tl.set(fx, {{ webkitTextFillColor: "transparent" }}, Math.max(g.s, wd[0]));
          tl.fromTo(word, {{ scale: wd[2] ? 1.32 : 1.16 }}, {{ scale: 1, duration: wd[2] ? 0.3 : 0.18, ease: "power3.out" }}, Math.max(g.s, wd[0]));
          if (wd[2]) tl.fromTo(word, {{ rotation: -6 }}, {{ rotation: 0, duration: 0.3, ease: "back.out(3)" }}, Math.max(g.s, wd[0]));
        }});
        tl.to(el, {{ opacity: 0, scale: 0.9, duration: 0.1, ease: "power2.in" }}, g.e - 0.1);
        tl.set("#" + g.id, {{ opacity: 0, visibility: "hidden" }}, g.e);
      }});
      tl.to(palms, {{ scale: 0, duration: 0.25, ease: "power2.in" }}, 55.7);
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
"""
open(f"{proj}/compositions/captions.html", "w").write(out)
print(len(groups), "groups")
for g in groups:
    print(g["id"], g["s"], g["e"], " ".join(x["t"] for x in g["w"]))
