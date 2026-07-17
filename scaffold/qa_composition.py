#!/usr/bin/env python3
"""Pre-render QA of a HyperFrames composition (copy into the ISOLATED scaffold dir, next to
index.html). Serves the dir over http://127.0.0.1 (file:// blocks fonts), seeks the paused GSAP
timeline at key times and screenshots each state into qa/.

Usage:  python3 qa_composition.py 2.2 7.1 13.0 22.0 ...   # explicit times (payoff moments)
        python3 qa_composition.py                          # auto: 2 probes per beat (25% / 75%)

Gotchas baked in (see SKILL.md Hard gotchas):
- `void tl.seek(t)` — seek() returns the chainable timeline; returning it to pg.evaluate hangs
  Playwright on the circular object forever.
- The renderer clips beats outside their data-start/data-duration window; a plain browser does
  NOT, so we emulate visibility per beat before each shot.
- If `window.__timelines` is undefined: syntax error in the composition (check for scaled digits
  inside dict KEY names) — fix before rendering anything.
"""
import os, subprocess, sys, time
from playwright.sync_api import sync_playwright

SC = os.path.dirname(os.path.abspath(__file__))
os.makedirs(f"{SC}/qa", exist_ok=True)
PORT = 8613
TIMES = [float(a) for a in sys.argv[1:]]

srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
                       cwd=SC, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(f"http://127.0.0.1:{PORT}/index.html")
        pg.wait_for_timeout(1500)
        if not pg.evaluate("() => !!(window.__timelines && Object.keys(window.__timelines).length)"):
            print("ERROR: timeline not registered (syntax error in the composition?)"); sys.exit(1)
        tlkey = pg.evaluate("() => Object.keys(window.__timelines)[0]")
        if not TIMES:
            beats = pg.evaluate("""() => [...document.querySelectorAll('.clip[data-start]')].map(el =>
                [parseFloat(el.dataset.start), parseFloat(el.dataset.duration)])""")
            TIMES = sorted(round(s + d * f, 2) for s, d in beats for f in (0.25, 0.75))
        for t in TIMES:
            pg.evaluate(f"() => {{ void window.__timelines['{tlkey}'].seek({t}); }}")
            pg.evaluate(f"""() => {{
                document.querySelectorAll('.clip[data-start]').forEach(el => {{
                    const s = parseFloat(el.dataset.start), d = parseFloat(el.dataset.duration);
                    el.style.visibility = ({t} >= s && {t} < s + d) ? 'visible' : 'hidden';
                }});
            }}""")
            pg.wait_for_timeout(60)
            pg.screenshot(path=f"{SC}/qa/t{str(t).replace('.', '_')}.png")
        b.close()
    print(f"QA done: {len(TIMES)} shots in {SC}/qa/ (review as contact sheets, e.g. ffmpeg hstack)")
finally:
    srv.terminate()
