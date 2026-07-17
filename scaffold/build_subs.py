#!/usr/bin/env python3
"""9:16 reel — PIL subtitles, applied LAST over the composite.

Sober subtitles: white Poppins-Bold, GOLD keyword (#F5A623), heavy 8-direction
black shadow so they read on BOTH the live face and the cream cards. Fixed y.
ALWAYS ON: continuous cues for the whole timeline, never suppressed, even over
the cream cards — the card states the concept, the subtitle tracks the speech.
AUTO-FIT: cues wider than MAXW scale their font down (floor 40px, baseline
unchanged) so long lines never overflow the frame.

Per-cue transparent 1080x1920 PNG, overlaid onto the composite, each gated by
its time window. This runs LAST in the pipeline (after compose.sh).
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- Config (adapt per video) -------------------------------------------------
FONTDIR = os.path.join(HERE, "assets", "fonts")   # point this at your own Poppins-Bold.ttf (or any bold font)
COMPOSITE = os.path.join(HERE, "composite.mp4")   # output of compose.sh
OUT       = os.path.join(HERE, "FINAL.mp4")
TOTAL     = 44.81                                  # base duration (output timeline)
W, H = 1080, 1920
GOLD = (245, 166, 35); WHITE = (255, 255, 255)
FS = 60
MAXW = 1000                                        # max cue width before auto-fit
Y  = 1496                                          # FIXED subtitle baseline

# (start, end, text, keyword)  — output-timeline seconds. keyword -> gold; None -> all white.
# EXAMPLE cues below — replace with your own transcript, anchored to the word
# timestamps from your ASR pass.
CUES = [
    (0.30, 1.90,  "Here's how I actually edit my reels", "reels"),
    (2.10, 3.60,  "I record on my phone", "phone"),
    (3.75, 5.20,  "and an agent builds the graphics on top", "agent"),
    # 5.4-8.0  full card (subs continue — always on)
    (8.20, 9.80,  "Word-level captions", "captions"),
    (10.00, 11.60,"camera moves on the beat", "camera"),
    (11.80, 13.40,"music and sound effects", "music"),
    # 13.6-18.0  full card (subs continue — always on)
    (18.20, 19.60,"Want the skill I use?", "skill"),
    # 19.6-22.0  CTA (subs continue — always on)
]
# -------------------------------------------------------------------------------

SUBS = os.path.join(HERE, "subs"); os.makedirs(SUBS, exist_ok=True)


def render_cue(idx, text, keyword):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # split the keyword out (case-insensitive, keep original token), color it gold
    parts = [(text, WHITE)]
    if keyword:
        low, kl = text.lower(), keyword.lower()
        i = low.find(kl)
        if i >= 0:
            parts = []
            if text[:i]: parts.append((text[:i], WHITE))
            parts.append((text[i:i+len(keyword)], GOLD))
            if text[i+len(keyword):]: parts.append((text[i+len(keyword):], WHITE))
    # AUTO-FIT: long cues scale down to stay inside MAXW (baseline unchanged)
    fs = FS
    fnt = ImageFont.truetype(os.path.join(FONTDIR, "Poppins-Bold.ttf"), fs)
    total_w = sum(d.textlength(txt, font=fnt) for txt, _ in parts)
    if total_w > MAXW:
        fs = max(40, int(FS * MAXW / total_w))
        fnt = ImageFont.truetype(os.path.join(FONTDIR, "Poppins-Bold.ttf"), fs)
        total_w = sum(d.textlength(txt, font=fnt) for txt, _ in parts)
    x = (W - total_w) / 2
    y = Y + (FS - fs) // 2
    for txt, col in parts:
        # heavy 8-direction shadow for legibility on face AND cream
        for ox, oy in [(-3,-3),(3,-3),(-3,3),(3,3),(0,4),(0,-4),(4,0),(-4,0)]:
            d.text((x+ox, y+oy), txt, font=fnt, fill=(0, 0, 0, 235))
        d.text((x, y), txt, font=fnt, fill=col + (255,))
        x += d.textlength(txt, font=fnt)
    p = os.path.join(SUBS, f"cue_{idx:02d}.png")
    img.save(p)
    return p


paths = [render_cue(i, t, k) for i, (s, e, t, k) in enumerate(CUES)]
print(f"rendered {len(paths)} cues")

# Final: composite + subs as LAST overlays (each looped, gated by enable=between)
cmd = ["ffmpeg", "-y", "-i", COMPOSITE]
for p in paths:
    cmd += ["-loop", "1", "-framerate", "30", "-t", f"{TOTAL}", "-i", p]
fc, prev = [], "[0:v]"
for i, (s, e, t, k) in enumerate(CUES):
    lab = f"[v{i}]"
    fc.append(f"{prev}[{i+1}:v]overlay=0:0:enable='between(t,{s},{e})'{lab}")
    prev = lab
cmd += ["-filter_complex", ";".join(fc), "-map", prev, "-map", "0:a",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart", OUT]
print("running final composite with subtitles...")
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stderr[-2500:] if r.returncode != 0 else f"OK -> {OUT}")
