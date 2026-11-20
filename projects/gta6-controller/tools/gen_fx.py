"""Generate compositions/fx.html — the GTA-6-inspired motion graphics layer."""
import sys, html

proj, palm_path = sys.argv[1], sys.argv[2]
PALM_T = open(palm_path).read()
palm = lambda pid: PALM_T.replace("PALMID", pid)

def st(text, cls="", tid=None):
    """Two-layer stroked Arabic title: solid stroke layer + gradient fill layer."""
    t = html.escape(text)
    i = f' id="{tid}"' if tid else ""
    return f'<span{i} class="tt {cls}"><span class="st" aria-hidden="true" data-layout-ignore>{t}</span><span class="fx">{t}</span></span>'

STAR = '<svg viewBox="0 0 24 24"><path d="M12 1.8l3.1 6.6 7.1.9-5.2 4.9 1.3 7.1L12 17.8l-6.3 3.5 1.3-7.1L1.8 9.3l7.1-.9z"/></svg>'

stars = lambda pfx: "".join(f'<span id="{pfx}{k}" class="star">{STAR}</span>' for k in range(5))

out = f"""<template>
  <style>
    @font-face {{
      font-family: "Lalezar";
      src: url("assets/fonts/Lalezar-Regular.ttf") format("truetype");
      font-display: block;
    }}
    #root {{ position: absolute; inset: 0; overflow: visible; pointer-events: none; }}
    .fxc {{ position: absolute; left: 0; right: 0; overflow: visible; }}
    .tt {{ position: relative; display: inline-block; font-family: "Lalezar", sans-serif; line-height: 1.2; white-space: nowrap; }}
    .tt .st {{ color: #2a0b4a; -webkit-text-stroke: 0.17em #2a0b4a; paint-order: stroke fill; }}
    .tt .fx {{
      position: absolute; inset: 0;
      background-image: linear-gradient(180deg, #ffe08a 0%, #ffa24c 36%, #ff4f9a 70%, #c64bff 100%);
      -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .tt.white .fx {{ background-image: none; -webkit-text-fill-color: #fff7ef; }}
    .drop {{ filter: drop-shadow(0 10px 0 #ff3d8b) drop-shadow(0 18px 22px rgba(30, 4, 50, 0.55)); }}
    .pill {{
      display: inline-block; padding: 10px 30px 8px; border-radius: 999px;
      font-family: "Archivo Black", sans-serif; font-size: 40px; letter-spacing: 0.12em; color: #fff7ef;
      background: linear-gradient(90deg, #ff4f9a, #c64bff); border: 4px solid #2a0b4a;
      box-shadow: 0 8px 0 #2a0b4a;
    }}
    .center {{ display: flex; flex-direction: column; align-items: center; }}

    /* hook */
    #fx-hook {{ top: 215px; height: 400px; }}
    #hook-sun {{
      position: absolute; left: 50%; top: 40px; width: 360px; height: 360px; margin-left: -180px; border-radius: 50%;
      background:
        repeating-linear-gradient(180deg, transparent 0 210px, rgba(42, 11, 74, 0.0) 210px 214px),
        linear-gradient(180deg, #ffe08a 0%, #ffa24c 40%, #ff4f9a 75%, #c64bff 100%);
      -webkit-mask-image: repeating-linear-gradient(180deg, #000 0 200px, transparent 200px 212px, #000 212px 250px, transparent 250px 266px, #000 266px 296px, transparent 296px 318px, #000 318px 360px);
      opacity: 0.92;
    }}
    #hook-stack {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; }}
    #hook-title {{ font-size: 150px; }}
    .hpalm {{ position: absolute; top: 120px; width: 170px; height: 300px; transform-origin: 50% 100%; }}
    .hpalm svg {{ width: 100%; height: 100%; overflow: visible; }}
    #hook-pl {{ left: 70px; }} #hook-pl svg {{ transform: scaleX(-1); }}
    #hook-pr {{ right: 70px; }}

    /* price */
    #fx-price {{ top: 270px; height: 300px; }}
    #price-card {{ position: absolute; left: 70px; top: 0; width: 360px; transform-origin: 30% 80%; }}
    #price-tag {{
      position: relative; padding: 18px 26px 10px 54px; border-radius: 22px 28px 28px 22px;
      background: #fff7ef; border: 6px solid #2a0b4a; box-shadow: 0 10px 0 #2a0b4a; text-align: center;
    }}
    #price-tag::before {{ content: ""; position: absolute; left: 18px; top: 50%; width: 18px; height: 18px; margin-top: -9px; border-radius: 50%; background: #2a0b4a; }}
    #price-dollars {{ font-family: "Archivo Black", sans-serif; font-size: 92px; line-height: 1; color: #1fbf6a; -webkit-text-stroke: 3px #2a0b4a; letter-spacing: 0.02em; }}
    #price-word {{ font-size: 76px; margin-top: 4px; }}
    #price-arrow {{ position: absolute; left: 330px; top: -30px; width: 170px; height: 170px; overflow: visible; }}

    /* real? */
    #fx-real {{ top: 230px; height: 360px; }}
    #real-q {{ position: absolute; left: 0; right: 0; top: -20px; text-align: center; font-size: 300px; }}
    #real-stamp {{
      position: absolute; left: 50%; top: 250px; width: 520px; margin-left: -260px; text-align: center;
      font-family: "Lalezar", sans-serif; font-size: 62px; color: #fff7ef; padding: 4px 0 0;
      background: #ff3d8b; border: 6px solid #2a0b4a; border-radius: 18px; box-shadow: 0 8px 0 #2a0b4a;
    }}

    /* flash wipe */
    #fx-wipe {{ top: 0; height: 1920px; overflow: hidden; }}
    #wipe-band {{
      position: absolute; left: -400px; top: -300px; width: 1880px; height: 2520px;
      background: repeating-linear-gradient(90deg, #ffe08a 0 120px, #ffa24c 120px 240px, #ff4f9a 240px 360px, #c64bff 360px 480px, #2a0b4a 480px 520px);
      transform-origin: 50% 50%;
    }}
    #wipe-word {{ position: absolute; left: 0; right: 0; top: 840px; text-align: center; }}
    #wipe-word .tt {{ font-size: 170px; }}

    /* mission HUD */
    #fx-mission {{ top: 270px; height: 260px; }}
    #mis-box {{
      position: absolute; left: 120px; right: 140px; top: 0; padding: 18px 34px 26px; border-radius: 24px;
      background: rgba(26, 6, 46, 0.82); border: 4px solid #ff4f9a; box-shadow: 0 10px 0 rgba(42, 11, 74, 0.9);
      direction: rtl; text-align: right;
    }}
    #mis-k {{ font-family: "Archivo Black", sans-serif; font-size: 30px; letter-spacing: 0.2em; color: #ffa24c; direction: ltr; text-align: right; }}
    #mis-t {{ font-family: "Lalezar", sans-serif; font-size: 72px; line-height: 1.2; color: #fff7ef; }}
    #mis-bar {{ position: relative; height: 26px; border-radius: 13px; background: rgba(255, 255, 255, 0.16); overflow: hidden; margin-top: 10px; }}
    #mis-fill {{ position: absolute; right: 0; top: 0; bottom: 0; width: 100%; transform-origin: 100% 50%;
      background: linear-gradient(270deg, #ffe08a, #ffa24c, #ff4f9a, #c64bff); }}

    /* mission passed */
    #fx-passed {{ top: 240px; height: 380px; }}
    #pass-title {{ font-size: 150px; }}
    #pass-sub {{ font-family: "Lalezar", sans-serif; font-size: 66px; color: #1fbf6a; -webkit-text-stroke: 12px #2a0b4a; paint-order: stroke fill; margin-top: -18px; }}
    .stars {{ display: flex; gap: 14px; justify-content: center; direction: ltr; }}
    .star {{ display: inline-block; width: 64px; height: 64px; }}
    .star svg {{ width: 100%; height: 100%; overflow: visible; }}
    .star path {{ fill: #ffd23f; stroke: #2a0b4a; stroke-width: 2.2; stroke-linejoin: round; }}

    /* black colour chip */
    #fx-black {{ top: 270px; height: 260px; }}
    #blk-chip {{
      position: absolute; right: 130px; top: 0; display: flex; align-items: center; gap: 22px; direction: rtl;
      padding: 18px 26px 14px 34px; border-radius: 999px; background: #fff7ef; border: 6px solid #2a0b4a; box-shadow: 0 10px 0 #2a0b4a;
    }}
    #blk-dot {{ width: 110px; height: 110px; border-radius: 50%; border: 6px solid #2a0b4a;
      background: radial-gradient(circle at 34% 30%, #6a5a7a 0%, #1a1420 34%, #050308 70%); position: relative; overflow: hidden; }}
    #blk-shine {{ position: absolute; top: -20%; left: -60%; width: 40%; height: 140%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.75), transparent); transform: rotate(20deg); }}
    #blk-text {{ font-family: "Lalezar", sans-serif; font-size: 74px; line-height: 1.15; color: #2a0b4a; }}
    #blk-text b {{ font-weight: 400; color: #ff3d8b; }}

    /* detail viewfinder */
    #fx-frame {{ top: 0; height: 1920px; }}
    .vf {{ position: absolute; width: 130px; height: 130px; border: 0 solid #fff7ef; filter: drop-shadow(0 0 10px rgba(255, 79, 154, 0.9)); }}
    #vf-tl {{ left: 110px; top: 330px; border-top-width: 12px; border-left-width: 12px; border-top-left-radius: 26px; }}
    #vf-tr {{ right: 110px; top: 330px; border-top-width: 12px; border-right-width: 12px; border-top-right-radius: 26px; }}
    #vf-bl {{ left: 110px; top: 1040px; border-bottom-width: 12px; border-left-width: 12px; border-bottom-left-radius: 26px; }}
    #vf-br {{ right: 110px; top: 1040px; border-bottom-width: 12px; border-right-width: 12px; border-bottom-right-radius: 26px; }}
    #vf-label {{ position: absolute; left: 0; right: 0; top: 200px; text-align: center; }}
    #vf-label .pill {{ font-family: "Lalezar", sans-serif; font-size: 64px; letter-spacing: 0; padding: 6px 40px 0; }}
    #vf-rec {{ position: absolute; left: 150px; top: 380px; padding: 6px 16px 4px; border-radius: 12px; background: rgba(20, 4, 36, 0.75); font-family: "Archivo Black", sans-serif; font-size: 34px; color: #fff7ef; display: flex; align-items: center; gap: 12px; direction: ltr; }}
    #vf-dot {{ width: 26px; height: 26px; border-radius: 50%; background: #ff3d3d; box-shadow: 0 0 14px #ff3d3d; }}

    /* written on the back */
    #fx-back {{ top: 250px; height: 520px; }}
    #back-label {{ position: absolute; left: 0; right: 0; top: 0; text-align: center; }}
    #back-label .tt {{ font-size: 110px; }}
    #back-arrow {{ position: absolute; left: 50%; top: 150px; width: 180px; height: 300px; margin-left: -60px; overflow: visible; }}

    /* in-game HUD */
    #fx-game {{ top: 280px; height: 200px; }}
    #game-tag {{ position: absolute; right: 150px; top: 0; display: flex; align-items: center; gap: 16px; direction: rtl;
      padding: 12px 26px 6px; border-radius: 20px; background: rgba(26, 6, 46, 0.85); border: 4px solid #ff4f9a; }}
    #game-tag span {{ font-family: "Lalezar", sans-serif; font-size: 52px; color: #fff7ef; line-height: 1.2; }}
    #game-pad {{ width: 78px; height: 54px; }}
    #game-stars {{ position: absolute; left: 90px; top: 120px; }}
    #game-stars .star {{ width: 58px; height: 58px; }}
    #game-stars .star path {{ fill: rgba(255, 255, 255, 0.18); stroke: #fff7ef; }}
    #game-stars .on path {{ fill: #ffd23f; stroke: #2a0b4a; }}

    /* CTA */
    #fx-cta {{ top: 250px; height: 460px; }}
    #cta-bubble {{
      position: absolute; left: 140px; right: 140px; top: 0; padding: 16px 30px 26px; text-align: center; border-radius: 40px;
      background: #fff7ef; border: 7px solid #2a0b4a; box-shadow: 0 12px 0 #2a0b4a; transform-origin: 50% 120%;
    }}
    #cta-bubble::after {{ content: ""; position: absolute; left: 50%; bottom: -46px; margin-left: -30px; border: 30px solid transparent; border-top: 40px solid #2a0b4a; }}
    #cta-q {{ font-size: 130px; }}
    #cta-sub {{ font-family: "Lalezar", sans-serif; font-size: 66px; color: #2a0b4a; margin-top: -10px; }}
    #cta-sub b {{ font-weight: 400; color: #ff3d8b; }}
    #cta-arrow {{ position: absolute; left: 50%; top: 360px; width: 90px; height: 110px; margin-left: -45px; overflow: visible; }}
  </style>
  <div id="root" data-composition-id="fx" data-width="1080" data-height="1920">

    <div id="fx-hook" class="clip fxc" data-start="0" data-duration="3.4" data-track-index="0">
      <div id="hook-in" style="position:absolute;inset:0">
        <div id="hook-sun"></div>
        <div id="hook-pl" class="hpalm">{palm("hpl")}</div>
        <div id="hook-pr" class="hpalm">{palm("hpr")}</div>
        <div id="hook-stack">
          <span id="hook-pill" class="pill">UNBOXING</span>
          <div class="drop">{st("يد GTA 6", tid="hook-title")}</div>
        </div>
      </div>
    </div>

    <div id="fx-price" class="clip fxc" data-start="9.95" data-duration="2.1" data-track-index="0">
      <div id="price-card">
        <div id="price-tag"><div id="price-dollars">$$$</div><div class="drop">{st("فلكية!", tid="price-word")}</div></div>
        <svg id="price-arrow" viewBox="0 0 170 170"><path id="price-arrow-p" d="M10 150 L60 96 L92 122 L156 30" fill="none" stroke="#2a0b4a" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 150 L60 96 L92 122 L156 30" fill="none" stroke="#ff3d3d" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><path d="M120 26 L162 20 L158 62 Z" fill="#ff3d3d" stroke="#2a0b4a" stroke-width="6" stroke-linejoin="round"/></svg>
      </div>
    </div>

    <div id="fx-real" class="clip fxc" data-start="15.65" data-duration="2.05" data-track-index="0">
      <div id="real-in" style="position:absolute;inset:0">
        <div id="real-q" class="drop">{st("؟")}</div>
        <div id="real-stamp">حقيقة ولا خرافة؟</div>
      </div>
    </div>

    <div id="fx-wipe" class="clip fxc" data-start="19.3" data-duration="0.9" data-track-index="0">
      <div id="wipe-band"></div>
      <div id="wipe-word" class="drop">{st("بسم الله!", "white")}</div>
    </div>

    <div id="fx-mission" class="clip fxc" data-start="20.6" data-duration="7.6" data-track-index="0">
      <div id="mis-box">
        <div id="mis-k">MISSION</div>
        <div id="mis-t">المهمة: فك العبوة</div>
        <div id="mis-bar"><div id="mis-fill"></div></div>
      </div>
    </div>

    <div id="fx-passed" class="clip fxc center" data-start="28.25" data-duration="2.9" data-track-index="0">
      <div id="pass-in" class="center">
        <div class="drop">{st("تمت المهمة!", tid="pass-title")}</div>
        <div id="pass-sub" style="display:flex;gap:16px;justify-content:center;direction:ltr"><span style="direction:ltr;unicode-bidi:isolate">+100</span><span>هيبة</span></div>
        <div id="pass-stars" class="stars">{stars("ps")}</div>
      </div>
    </div>

    <div id="fx-black" class="clip fxc" data-start="35.75" data-duration="3.9" data-track-index="0">
      <div id="blk-chip">
        <div id="blk-dot"><div id="blk-shine"></div></div>
        <div id="blk-text">الأسود <b>الفخم</b></div>
      </div>
    </div>

    <div id="fx-frame" class="clip fxc" data-start="39.65" data-duration="3.85" data-track-index="0">
      <div id="vf-tl" class="vf"></div><div id="vf-tr" class="vf"></div>
      <div id="vf-bl" class="vf"></div><div id="vf-br" class="vf"></div>
      <div id="vf-rec"><div id="vf-dot"></div>REC</div>
      <div id="vf-label"><span id="vf-pill" class="pill">التفاصيل</span></div>
    </div>

    <div id="fx-back" class="clip fxc" data-start="43.5" data-duration="2.2" data-track-index="0">
      <div id="back-label" class="drop">{st("مكتوب من ورا!", tid="back-title")}</div>
      <svg id="back-arrow" viewBox="0 0 180 300"><path id="back-arrow-p" d="M40 10 C 140 60, 140 170, 70 260" fill="none" stroke="#2a0b4a" stroke-width="30" stroke-linecap="round"/><path d="M40 10 C 140 60, 140 170, 70 260" fill="none" stroke="#fff7ef" stroke-width="15" stroke-linecap="round"/><path d="M30 226 L68 290 L110 236 Z" fill="#fff7ef" stroke="#2a0b4a" stroke-width="7" stroke-linejoin="round"/></svg>
    </div>

    <div id="fx-game" class="clip fxc" data-start="46.6" data-duration="6.45" data-track-index="0">
      <div id="game-tag">
        <svg id="game-pad" viewBox="0 0 78 54"><path d="M16 4 H62 C72 4 77 14 77 28 C77 44 72 52 64 52 C56 52 52 40 46 40 H32 C26 40 22 52 14 52 C6 52 1 44 1 28 C1 14 6 4 16 4 Z" fill="#ff4f9a" stroke="#fff7ef" stroke-width="3"/><rect x="14" y="20" width="16" height="5" rx="2" fill="#fff7ef"/><rect x="19.5" y="14.5" width="5" height="16" rx="2" fill="#fff7ef"/><circle cx="56" cy="17" r="4" fill="#fff7ef"/><circle cx="56" cy="31" r="4" fill="#fff7ef"/><circle cx="49" cy="24" r="4" fill="#fff7ef"/><circle cx="63" cy="24" r="4" fill="#fff7ef"/></svg>
        <span>تجربة داخل اللعبة</span>
      </div>
      <div id="game-stars" class="stars">{stars("gs")}</div>
    </div>

    <div id="fx-cta" class="clip fxc" data-start="53.1" data-duration="2.98" data-track-index="0">
      <div id="cta-bubble">
        <div class="drop">{st("وش رايكم؟", tid="cta-q")}</div>
        <div id="cta-sub">اكتبوا لي <b>بالكومنتات</b></div>
      </div>
      <svg id="cta-arrow" viewBox="0 0 90 110"><path d="M45 6 V70" stroke="#2a0b4a" stroke-width="30" stroke-linecap="round"/><path d="M45 6 V70" stroke="#ffd23f" stroke-width="16" stroke-linecap="round"/><path d="M8 58 L45 104 L82 58 Z" fill="#ffd23f" stroke="#2a0b4a" stroke-width="7" stroke-linejoin="round"/></svg>
    </div>
  </div>
  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
      const IN = "back.out(2.2)";

      // HOOK — already on screen at frame 0 (thumbnail), lands with a stamp
      tl.fromTo("#hook-sun", {{ scale: 0.7, y: 40 }}, {{ scale: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0);
      tl.fromTo("#hook-title", {{ scale: 1.35, rotation: -6 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: IN }}, 0);
      tl.fromTo("#hook-pill", {{ scale: 0.8, y: 10 }}, {{ scale: 1, y: 0, duration: 0.35, ease: IN }}, 0);
      tl.fromTo(["#hook-pl", "#hook-pr"], {{ scale: 0.3, rotation: 0 }}, {{ scale: 1, duration: 0.5, ease: IN, stagger: 0.08 }}, 0.05);
      tl.fromTo("#hook-pl", {{ rotation: 0 }}, {{ immediateRender: false, rotation: -6, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, 2.0);
      tl.fromTo("#hook-pr", {{ rotation: 0 }}, {{ immediateRender: false, rotation: 6, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, 2.0);
      tl.fromTo("#hook-title", {{ scale: 1 }}, {{ immediateRender: false, scale: 1.12, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 1 }}, 2.0);
      tl.to("#hook-in", {{ y: -520, opacity: 0, duration: 0.3, ease: "power3.in" }}, 3.08);

      // PRICE — tag swings in, trend arrow draws up
      tl.fromTo("#price-card", {{ scale: 0, rotation: -25 }}, {{ scale: 1, rotation: -6, duration: 0.4, ease: IN }}, 9.95);
      tl.fromTo("#price-arrow", {{ scale: 0, x: -40, y: 40 }}, {{ scale: 1, x: 0, y: 0, duration: 0.35, ease: IN }}, 10.25);
      tl.fromTo("#price-dollars", {{ scale: 1 }}, {{ scale: 1.15, duration: 0.1, yoyo: true, repeat: 3, ease: "power1.inOut" }}, 10.68);
      tl.to("#price-card", {{ x: -560, rotation: -20, duration: 0.3, ease: "power3.in" }}, 11.72);

      // REAL? — question mark slams, stamp thuds
      tl.fromTo("#real-q", {{ scale: 2.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "power4.out" }}, 15.65);
      tl.fromTo("#real-stamp", {{ scale: 1.8, rotation: 8, opacity: 0 }}, {{ scale: 1, rotation: -4, opacity: 1, duration: 0.22, ease: "power4.out" }}, 16.2);
      tl.fromTo("#real-q", {{ rotation: 0 }}, {{ immediateRender: false, rotation: 10, duration: 0.08, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 16.56);
      tl.to("#real-in", {{ scale: 0.6, opacity: 0, duration: 0.18, ease: "power2.in" }}, 17.5);

      // WIPE — sunset stripes sweep across on "بسم الله"
      tl.fromTo("#wipe-band", {{ xPercent: 105, rotation: 18 }}, {{ xPercent: -2, duration: 0.3, ease: "power3.out" }}, 19.3);
      tl.fromTo("#wipe-word", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.22, ease: IN }}, 19.42);
      tl.to("#wipe-word", {{ scale: 1.3, opacity: 0, duration: 0.18, ease: "power2.in" }}, 19.85);
      tl.to("#wipe-band", {{ xPercent: -110, duration: 0.3, ease: "power3.in" }}, 19.88);

      // MISSION — HUD drops in, bar fills during the silent unboxing
      tl.fromTo("#mis-box", {{ y: -300 }}, {{ y: 0, duration: 0.4, ease: "power3.out" }}, 20.6);
      tl.fromTo("#mis-fill", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 7.0, ease: "none" }}, 20.9);
      tl.to("#mis-box", {{ y: -320, duration: 0.25, ease: "power3.in" }}, 27.95);

      // MISSION PASSED — "ما شاء الله"
      tl.fromTo("#pass-title", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.32, ease: "power4.out" }}, 28.25);
      tl.fromTo("#pass-sub", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.25, ease: IN }}, 28.6);
      for (let k = 0; k < 5; k++) tl.fromTo("#ps" + k, {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: IN }}, 28.8 + k * 0.1);
      tl.to("#pass-in", {{ y: -500, opacity: 0, duration: 0.3, ease: "power3.in" }}, 30.82);

      // BLACK — colour chip with a sheen
      tl.fromTo("#blk-chip", {{ x: 700 }}, {{ x: 0, duration: 0.4, ease: "power3.out" }}, 35.75);
      tl.fromTo("#blk-shine", {{ x: 0 }}, {{ x: 260, duration: 0.6, ease: "power2.inOut" }}, 36.5);
      tl.fromTo("#blk-text b", {{ scale: 1 }}, {{ scale: 1.2, duration: 0.14, yoyo: true, repeat: 1, ease: "power2.out" }}, 38.97);
      tl.fromTo("#blk-shine", {{ x: 0 }}, {{ immediateRender: false, x: 260, duration: 0.6, ease: "power2.inOut" }}, 38.9);
      tl.to("#blk-chip", {{ x: 760, duration: 0.3, ease: "power3.in" }}, 39.3);

      // DETAILS — viewfinder closes in on the controller
      tl.fromTo("#vf-tl", {{ x: -120, y: -120, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 39.65);
      tl.fromTo("#vf-tr", {{ x: 120, y: -120, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 39.65);
      tl.fromTo("#vf-bl", {{ x: -120, y: 120, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 39.65);
      tl.fromTo("#vf-br", {{ x: 120, y: 120, opacity: 0 }}, {{ x: 0, y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 39.65);
      tl.fromTo("#vf-pill", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: IN }}, 40.75);
      tl.fromTo("#vf-rec", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, 39.9);
      for (let k = 0; k < 3; k++) tl.fromTo("#vf-dot", {{ opacity: 1 }}, {{ immediateRender: k === 0, opacity: 0.15, duration: 0.4, yoyo: true, repeat: 1, ease: "sine.inOut" }}, 40.1 + k * 1.0);
      tl.to(["#vf-tl", "#vf-tr", "#vf-bl", "#vf-br", "#vf-label", "#vf-rec"], {{ opacity: 0, scale: 1.2, duration: 0.2, ease: "power2.in" }}, 43.25);

      // WRITTEN ON THE BACK
      tl.fromTo("#back-title", {{ scale: 0, rotation: 8 }}, {{ scale: 1, rotation: -3, duration: 0.32, ease: IN }}, 43.5);
      tl.fromTo("#back-arrow", {{ opacity: 0, y: -40, scale: 0.6 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.3, ease: IN }}, 43.7);
      tl.fromTo("#back-arrow", {{ y: 0 }}, {{ immediateRender: false, y: 24, duration: 0.2, yoyo: true, repeat: 3, ease: "sine.inOut" }}, 44.1);
      tl.to("#fx-back > *", {{ opacity: 0, y: -40, duration: 0.2, ease: "power2.in" }}, 45.48);

      // IN-GAME — tag slides in, wanted stars light up one per beat
      tl.fromTo("#game-tag", {{ x: 600 }}, {{ x: 0, duration: 0.4, ease: "power3.out" }}, 46.6);
      tl.fromTo("#game-stars .star", {{ scale: 0 }}, {{ scale: 1, duration: 0.25, ease: IN, stagger: 0.06 }}, 46.8);
      [47.6, 48.5, 49.5, 50.4, 51.6].forEach(function (t, k) {{
        const id = "#gs" + (4 - k);
        tl.set(id, {{ className: "star on" }}, t);
        tl.fromTo(id, {{ scale: 1.7 }}, {{ scale: 1, duration: 0.25, ease: "power3.out" }}, t);
      }});
      tl.to("#fx-game > *", {{ y: -300, duration: 0.3, ease: "power3.in" }}, 52.72);

      // CTA
      tl.fromTo("#cta-bubble", {{ scale: 0, rotation: -8 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: IN }}, 53.1);
      tl.fromTo("#cta-sub b", {{ scale: 1 }}, {{ scale: 1.18, duration: 0.14, yoyo: true, repeat: 1, ease: "power2.out" }}, 53.92);
      tl.fromTo("#cta-arrow", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: IN }}, 53.6);
      tl.fromTo("#cta-arrow", {{ y: 0 }}, {{ immediateRender: false, y: 26, duration: 0.22, yoyo: true, repeat: 7, ease: "sine.inOut" }}, 53.9);
      tl.fromTo("#cta-q", {{ rotation: 0 }}, {{ rotation: -5, duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out" }}, 54.52);

      window.__timelines["fx"] = tl;
    }})();
  </script>
</template>
"""
open(f"{proj}/compositions/fx.html", "w").write(out)
print("ok")
